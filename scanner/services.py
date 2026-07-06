import os
from django.conf import settings
from .models import APK
import requests 


def save_uploaded_apk(apk):   # the work is to save the apk to database 
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


def upload_to_mobsf(apk_path):   # send apk to mobsf

    url = "http://localhost:8080/api/v1/upload" #send my request to this adresss 
    headers = {
        "X-Mobsf-Api-Key": "b541bd4227fb67f5bb49bc4158588cd5c792498452a810c237ebb1737635dbbb"
    }

    with open(apk_path, "rb") as apk_file:
        files = {
            "file": (
                os.path.basename(apk_path),
                apk_file,
                "application/vnd.android.package-archive"
            )
        }

        response = requests.post(
            url,
            headers=headers,
            files=files
        )
        
        data  =  response.json()
        return data
    

def start_scan(apk_hash):
    url = "http://localhost:8080/api/v1/scan"
    headers = {
        "X-Mobsf-Api-Key": "b541bd4227fb67f5bb49bc4158588cd5c792498452a810c237ebb1737635dbbb"
    }
    data = {

    "hash": apk_hash,

    "re_scan": 0

}
    response = requests.post(

    url,

    headers=headers,

    data=data

)
    scan_result = response.json()
    print(scan_result)
