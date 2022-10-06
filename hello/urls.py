from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings  

urlpatterns = [
    path('upload', views.model_form_upload, name='upload'),
    path('show_alternatives', views.show_alternatives, name='show_alternatives')
]
