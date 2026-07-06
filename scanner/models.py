from django.db import models


class APK(models.Model):

    apk_name = models.CharField(max_length=255)

    file_path = models.CharField(max_length=500)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=50)

    def __str__(self):
        return self.apk_name