from django.db import models


class APK(models.Model):

    STATUS_CHOICES = [
        ("UPLOADED", "Uploaded"),
        ("SCANNING", "Scanning"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    apk_name = models.CharField(max_length=255)

    file_path = models.CharField(max_length=500)

    hash = models.CharField(
        max_length=64,
        blank=True
    )

    security_score = models.IntegerField(
        null=True,
        blank=True
    )

    report_path = models.CharField(
        max_length=500,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="UPLOADED"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    scanned_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.apk_name