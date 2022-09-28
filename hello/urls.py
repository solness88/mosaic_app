from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.model_form_upload, name='upload'),
    path('gray', views.gray, name='gray'),
    path('sepia', views.sepia, name='sepia'),
    path('mosaic', views.mosaic, name='mosaic'),
]
