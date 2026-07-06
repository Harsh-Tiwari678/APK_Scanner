from django.shortcuts import render

from .services import save_uploaded_apk


def home(request):

    context = {
        "Username": "Harsh",
        "title": "APK_Scanner",
        "Project": "APK Scanner",
    }

    if request.method == "POST":

        if "apk" in request.FILES:

            apk = request.FILES["apk"]

            save_uploaded_apk(apk)

    return render(request, "scanner/home.html", context)