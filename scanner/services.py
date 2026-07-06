import os

from django.conf import settings

from .models import APK


def save_uploaded_apk(apk):

    upload_folder = os.path.join(settings.MEDIA_ROOT, "uploads")

    os.makedirs(upload_folder, exist_ok=True)

    save_path = os.path.join(upload_folder, apk.name)

    with open(save_path, "wb+") as destination:

        for chunk in apk.chunks():

            destination.write(chunk)

    apk_record = APK.objects.create(

        apk_name=apk.name,

        file_path=save_path,

        status="Uploaded"

    )

    return apk_record