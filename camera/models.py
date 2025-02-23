from django.db import models


class ImageCapture(models.Model):
    image = models.ImageField(upload_to='captures/')
    captured_at = models.DateTimeField(auto_now_add=True)
