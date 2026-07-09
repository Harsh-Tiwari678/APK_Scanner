from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  #tells this is an API endpoint not a browser form 
def api_scan(request):
    return JsonResponse(
        {
     "message": "API is working"
    },
    status = 200
    )