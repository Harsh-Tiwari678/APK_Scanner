from django.shortcuts import render
from django.conf import settings
import os
from .models import APK  # Ensure you import your model

def home(request):
    context = {
        'Username': 'Harsh',
        'title': 'APK_Scanner',
        'Project': 'APK Scanner'
    }

    if request.method == "POST":
        if 'apk' in request.FILES:
            apk = request.FILES["apk"]
            
            # Setup path
            upload_folder = os.path.join(settings.MEDIA_ROOT, "uploads")
            os.makedirs(upload_folder, exist_ok=True)
            save_path = os.path.join(upload_folder, apk.name)

            # Save the file
            with open(save_path, "wb+") as destination:
                for chunk in apk.chunks():
                    destination.write(chunk)
            
            print(f"APK Saved Successfully at {save_path}")

            # Save metadata to database
            APK.objects.create(
                apk_name=apk.name,
                file_path=save_path,
                status="Uploaded"
            )
     
    return render(request, 'scanner/home.html', context)