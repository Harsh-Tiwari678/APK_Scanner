import os

from django.shortcuts import render
from django.utils import timezone
from django.http import FileResponse, Http404

from .models import APK

from .services import (
    save_uploaded_apk,
    upload_to_mobsf,
    start_scan,
)

from .parser import parse_scan_result
from .pdf_generator import generate_pdf


def home(request):
    """
    Homepage of the APK Scanner.
    Handles APK upload, MobSF scan, PDF generation,
    and updates the database.
    """

    context = {
        "Username": "Harsh",
        "title": "APK Scanner",
        "Project": "APK Scanner",
    }

    if request.method == "POST":

        if "apk" in request.FILES:

            apk = request.FILES["apk"]

            # Save Uploaded APK

            apk_record = save_uploaded_apk(apk)

            try:

                # Update Status -> SCANNING

                apk_record.status = "SCANNING"
                apk_record.save()

                # Upload APK to MobSF

                upload_data = upload_to_mobsf(
                    apk_record.file_path
                )

                apk_hash = upload_data["hash"]

                
                # Start MobSF Scan

                scan_result = start_scan(apk_hash)

                # Parse Scan Result

                report = parse_scan_result(scan_result)

                # Generate PDF Report

                pdf_path = generate_pdf(report)

                # Update Database

                apk_record.hash = apk_hash

                apk_record.security_score = report.get(
                    "security_score"
                )

                apk_record.report_path = pdf_path

                context["apk_id"] = apk_record.id

                apk_record.status = "COMPLETED"

                apk_record.scanned_at = timezone.now()

                apk_record.save()

                context["success"] = True
                context["message"] = "APK scanned successfully."

            except Exception as e:

                apk_record.status = "FAILED"
                apk_record.save()

                print("Scan Error:", e)

                context["success"] = False
                context["message"] = str(e)

    # Show Previous Scans

    all_apks = APK.objects.all().order_by("-uploaded_at")

    context["all_apks"] = all_apks

    return render(
        request,
        "scanner/home.html",
        context
    )


def download_report(request, apk_id):
    """
    Downloads the generated PDF report.
    """

    try:
        apk = APK.objects.get(id=apk_id)

    except APK.DoesNotExist:
        raise Http404("APK not found.")

    if not apk.report_path:
        raise Http404("Report has not been generated.")

    if not os.path.exists(apk.report_path):
        raise Http404("Report file does not exist.")

    return FileResponse(
        open(apk.report_path, "rb"),
        as_attachment=True,
        filename=os.path.basename(apk.report_path),
    )