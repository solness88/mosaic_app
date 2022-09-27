from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.model_form_upload, name='upload'),
    path('file_download', views.file_download, name='file_download'),
]
