from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .services import (
    save_uploaded_apk,
    upload_to_mobsf,
    start_scan
)

from .parser import parse_scan_result
from .pdf_generator import generate_pdf


@csrf_exempt
def api_scan(request):

    # -----------------------------------
    # Allow only POST requests
    # -----------------------------------

    if request.method != "POST":

        return JsonResponse(
            {
                "error": "Only POST requests allowed."
            },
            status=405
        )

    # -----------------------------------
    # Get APK file
    # -----------------------------------

    apk = request.FILES.get("apk")

    if not apk:

        return JsonResponse(
            {
                "error": "APK file missing."
            },
            status=400
        )

    try:

        # -----------------------------------
        # Save APK locally
        # -----------------------------------

        apk_record = save_uploaded_apk(apk)

        # -----------------------------------
        # Upload to MobSF
        # -----------------------------------

        upload_data = upload_to_mobsf(
            apk_record.file_path
        )

        apk_hash = upload_data["hash"]

        # -----------------------------------
        # Start Scan
        # -----------------------------------

        scan_result = start_scan(apk_hash)

        # -----------------------------------
        # Parse Report
        # -----------------------------------

        report = parse_scan_result(
            scan_result
        )

        # -----------------------------------
        # Generate PDF
        # -----------------------------------

        pdf_path = generate_pdf(
            report
        )

        return JsonResponse(
            {
                "status": "success",
                "apk_name": apk.name,
                "security_score": report.get(
                    "security_score"
                ),
                "pdf_path": pdf_path
            },
            status=200
        )

    except Exception as e:

        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )