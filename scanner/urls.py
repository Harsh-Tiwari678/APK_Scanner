from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
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

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)