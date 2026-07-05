from django.shortcuts import render
from django.conf import settings
import os

# Create your views here.

def home(request):
    context = {
        'Username' : 'Harsh',
        'title' : 'APK_Scanner',
        'Project'  : 'APK Scanner'
    }

    if request.method == "POST":
        # Only process if the key 'apk' exists in the files
        if 'apk' in request.FILES:
            apk = request.FILES["apk"]
            
            # These lines MUST be inside the if block
            upload_folder = os.path.join(settings.MEDIA_ROOT, "uploads")
            os.makedirs(upload_folder, exist_ok=True)
            save_path = os.path.join(upload_folder, apk.name)

            with open(save_path, "wb+") as destination:
                for chunk in apk.chunks():
                    destination.write(chunk)
            
            print("APK Saved Successfully")
            print(save_path)
     
    return render(request, 'scanner/home.html', context)