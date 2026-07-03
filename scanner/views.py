from django.shortcuts import render

# Create your views here.

def home(request):
    context = {
        'Username' : 'Harsh',
        'title' : 'APK_Scanner',
        'Project'  : 'APK Scanner'

    }
    return render(request , 'scanner/home.html',context)
