from django.urls import path
from . import views
from .import api_view

urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "download/<int:apk_id>/",
        views.download_report,
        name="download_report"
    ),
    path("api/scan/",
         api_view.api_scan,
         name="api_scan"),

]