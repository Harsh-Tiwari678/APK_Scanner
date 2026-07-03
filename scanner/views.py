from django.shortcuts import render

# Create your views here.

def home(request):
    context = {
        'title' : 'APK_Scanner',
        'Project'  : 'APK Scanner'

    }
    return render(request , 'home.html',context)
