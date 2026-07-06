import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.conf import settings

def generate_pdf(report):
    report_folder = os.path.join(
    settings.MEDIA_ROOT,
    "reports"
)
    os.makedirs(
    report_folder,
    exist_ok=True
)