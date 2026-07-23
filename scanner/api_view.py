import os
import re
import io
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from .services import (
    save_uploaded_apk,
    upload_to_mobsf,
    start_scan
)

from .parser import parse_scan_result
from .pdf_generator import generate_pdf


def download_file_from_google_drive(url):
    """
    Automated API-driven download method.
    Bypasses standard web UI blocks by requesting via the public API media endpoint.
    """
    # Extract file ID from standard Google Drive URL structure
    file_id_match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
    if not file_id_match:
        raise Exception("Invalid Google Drive URL format.")
    
    file_id = file_id_match.group(1)
    
    # Public API link that streams the raw bytes directly without HTML/Login walls
    api_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(api_url, headers=headers, stream=True)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch via Drive API. Status code: {response.status_code}. Ensure link is shared as 'Anyone with the link'.")
        
    return response.content


@csrf_exempt
def api_scan(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests allowed."}, status=405)

    apk_file_stream = None
    apk_name = "InsecureShop.apk"

    # 1. Check if traditional multi-part file exists
    if request.FILES.get("apk"):
        apk_file_stream = request.FILES.get("apk")
        apk_name = apk_file_stream.name

    # 2. Check if a dynamic URL link is provided in POST JSON or Form data body instead
    else:
        file_url = None
        if request.content_type == "application/json":
            try:
                body_data = json.loads(request.body)
                file_url = body_data.get("file_url") or body_data.get("snippet")
            except json.JSONDecodeError:
                pass
        else:
            file_url = request.POST.get("file_url") or request.POST.get("snippet")

        # If a URL was captured, attempt downloading the asset stream via Public API
        if file_url:
            drive_links = re.findall(r'https://drive\.google\.com/[^\s]+', file_url)
            target_url = drive_links[0] if drive_links else file_url
            
            # Clean accidental string quotes or whitespaces
            target_url = target_url.strip().replace('"', '').replace("'", "")
            
            try:
                binary_content = download_file_from_google_drive(target_url)
                
                # Convert raw bytes into proper Django Multipart file memory handler for MobSF
                file_io = io.BytesIO(binary_content)
                apk_file_stream = InMemoryUploadedFile(
                    file_io,
                    field_name='apk',
                    name=apk_name,
                    content_type='application/vnd.android.package-archive',
                    size=len(binary_content),
                    charset=None
                )
            except Exception as download_error:
                return JsonResponse({
                    "status": "failed",
                    "error": f"Error downloading file from provided cloud link: {str(download_error)}"
                }, status=400)

    # Drop request if no valid data source loaded
    if not apk_file_stream:
        return JsonResponse({"error": "APK file or valid downloadable cloud link missing."}, status=400)

    try:
        # -----------------------------------
        # Save APK locally
        # -----------------------------------
        apk_record = save_uploaded_apk(apk_file_stream)

        # -----------------------------------
        # Upload APK to MobSF
        # -----------------------------------
        upload_data = upload_to_mobsf(apk_record.file_path)
        apk_hash = upload_data["hash"]

        # -----------------------------------
        # Start MobSF Scan
        # -----------------------------------
        scan_result = start_scan(apk_hash)

        # -----------------------------------
        # Parse Scan Result
        # -----------------------------------
        report = parse_scan_result(scan_result)

        # -----------------------------------
        # Generate PDF Report
        # -----------------------------------
        pdf_path = generate_pdf(report)

        # -----------------------------------
        # Create Public PDF URL
        # -----------------------------------
        relative_path = os.path.relpath(pdf_path, settings.MEDIA_ROOT)
        pdf_url = request.build_absolute_uri(
            settings.MEDIA_URL + relative_path.replace("\\", "/")
        )

        # -----------------------------------
        # Return JSON Response
        # -----------------------------------
        return JsonResponse({
            "status": "success",
            "apk_name": apk_name,
            "security_score": report.get("security_score"),
            "pdf_url": pdf_url
        }, status=200)

    except Exception as e:
        return JsonResponse({
            "status": "failed",
            "error": str(e)
        }, status=500)