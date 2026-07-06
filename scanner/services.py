import os
import requests

from django.conf import settings
from .models import APK


# -------------------------------------------------
# MobSF Configuration
# -------------------------------------------------

MOBSF_URL = "http://localhost:8080"

API_KEY = "YOUR_MOBSF_API_KEY"


# -------------------------------------------------
# Save Uploaded APK
# -------------------------------------------------

def save_uploaded_apk(apk):
    """
    Saves the uploaded APK inside media/uploads/
    and creates the initial database record.
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


# -------------------------------------------------
# Upload APK to MobSF
# -------------------------------------------------

def upload_to_mobsf(apk_path):
    """
    Uploads the APK to MobSF.
    Returns:
        {
            "hash": "...",
            "file_name": "...",
            ...
        }
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

    return response.json()


# -------------------------------------------------
# Start Scan
# -------------------------------------------------

def start_scan(apk_hash):
    """
    Starts the MobSF Static Scan.

    Returns the complete JSON report.
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

    return response.json()