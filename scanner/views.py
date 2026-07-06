from django.shortcuts import render

from .services import save_uploaded_apk , start_scan

from . services import upload_to_mobsf

from .parser import parse_scan_result

from .pdf_generator import generate_pdf


def home(request):

    context = {
        "Username": "Harsh",
        "title": "APK_Scanner",
        "Project": "APK Scanner",
    }

    if request.method == "POST":

        if "apk" in request.FILES:

            apk = request.FILES["apk"]

            apk_record = save_uploaded_apk(apk)

            upload_data = upload_to_mobsf(apk_record.file_path)
            apk_hash = upload_data["hash"]
            start_scan(apk_hash)
            report = parse_scan_result(scan_result)

            pdf_path = generate_pdf(report)

    return render(request, "scanner/home.html", context)