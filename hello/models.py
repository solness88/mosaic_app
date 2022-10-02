from distutils.command.upload import upload
from django.db import models

class Document(models.Model):
    photo = models.ImageField(upload_to='gallery/', default='SOME STRING')
    picture_type = models.CharField(max_length=100, default='black_white')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.photo, self.picture_type)
