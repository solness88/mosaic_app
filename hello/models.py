from distutils.command.upload import upload
from django.db import models

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='gallery/', default='SOME STRING')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    gray = models.ImageField(default='Not Set')

    def __str__(self):
        return self.photo
