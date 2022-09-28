from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.model_form_upload, name='upload'),
    path('file_download', views.file_download, name='file_download'),
    path('download_complete', views.download_complete, name='download_complete'),
]
