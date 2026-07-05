from django.shortcuts import render

# Create your views here.

def home(request):
    context = {
        'Username' : 'Harsh',
        'title' : 'APK_Scanner',
        'Project'  : 'APK Scanner'

    }

    if request.method == "POST":
     print("Form Submitted Succesfully")
     apk = request.FILES["apk"]
     print(type(apk))
     print(apk.multiple_chunks())
     print(apk.charset)
     
    return render(request , 'scanner/home.html',context)
