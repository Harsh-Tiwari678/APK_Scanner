from django.shortcuts import render

from .services import save_uploaded_apk , start_scan

from . services import upload_to_mobsf


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

    return render(request, "scanner/home.html", context)