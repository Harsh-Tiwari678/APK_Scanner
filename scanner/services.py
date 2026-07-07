import os
import requests

from django.conf import settings
from .models import APK

import json



# MobSF Configuration


MOBSF_URL = "http://localhost:8080"
API_KEY = settings.MOBSF_API_KEY



# Save  the Uploaded APK


def save_uploaded_apk(apk):
    """
    Save the uploaded APK into media/uploads/
    and create an initial database record.
    """

    upload_folder = os.path.join(settings.MEDIA_ROOT, "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    save_path = os.path.join(upload_folder, apk.name)

    with open(save_path, "wb+") as destination:
        for chunk in apk.chunks():
            destination.write(chunk)

    apk_record = APK.objects.create(
        apk_name=apk.name,
        file_path=save_path,
        status="UPLOADED"
    )

    return apk_record



# Upload APK To the  MobSF


def upload_to_mobsf(apk_path):
    """
    Upload an APK to MobSF.

    Returns:
        Dictionary containing file_name, hash, scan_type, etc.
    """

    url = f"{MOBSF_URL}/api/v1/upload"

    headers = {
        "X-Mobsf-Api-Key": API_KEY
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

    response.raise_for_status()

    upload_result = response.json()

    

    return upload_result



# Start  the Static Scan

def start_scan(apk_hash):
    """
    Start the MobSF static scan.

    Returns:
        Complete MobSF JSON report.
    """

    url = f"{MOBSF_URL}/api/v1/scan"

    headers = {
        "X-Mobsf-Api-Key": API_KEY
    }

    payload = {
        "hash": apk_hash,
        "re_scan": 0
    }

    response = requests.post(
        url,
        headers=headers,
        data=payload
    )

    response.raise_for_status()

    scan_result = response.json()


    return scan_result