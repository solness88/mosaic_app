from django.shortcuts import render,redirect
from .forms import DocumentForm
from .models import Document
import cv2
from django.conf import settings
from django.utils import timezone
import glob
from django.http import FileResponse
import os
# from pathlib import Path


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        photo = Document.objects.order_by("id").last()
        url = photo.photo
        picture_type = photo.picture_type
        if picture_type == 'black_white':
            gray(url)
        elif picture_type == 'mosaic':
            mosaic(url)
        elif picture_type == 'sepia':
            sepia(url)
        # file_name = glob.glob('./media/gallery/*')
        # print('こんにちは！')
        # print(file_name)
        photo.delete()
        return redirect('file_download')
    else:
        form = DocumentForm()
    return render(request, 'hello/model_form_upload.html', {
        'form': form
    })


def file_download(request):
    file_path = glob.glob('./media/gallery/*')
    file_name = os.path.basename(file_path[0])
    return FileResponse(open(file_path[0], "rb"), as_attachment=True, filename=file_name)


# convert into gray-color
def gray(url):
    path = settings.MEDIA_ROOT + "/" + str(url)
    img = cv2.imread(path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    output = settings.MEDIA_ROOT + "/gallery/GRAY)" + str(timezone.now()) + ".jpg"
    cv2.imwrite(output, img_gray)

# convert into mosaic
def mosaic(url):
    path = settings.MEDIA_ROOT + "/" + str(url)
    img = cv2.imread(path)
    small = cv2.resize(img, None, fx=0.1, fy=0.1)
    img_mosaic = cv2.resize(small, img.shape[:2][::-1])
    output = settings.MEDIA_ROOT + "/gallery/MOSAIC)" + str(timezone.now()) + ".jpg"
    cv2.imwrite(output, img_mosaic)

# convert into sepia
def sepia(url):
    path = settings.MEDIA_ROOT + "/" + str(url)
    img = cv2.imread(path) 
    img[:,:,(0)] = img[:,:,(0)] * 0.3
    img[:,:,(1)] = img[:,:,(1)] * 0.8
    img[:,:,(2)] = img[:,:,(2)]
    output = settings.MEDIA_ROOT + "/gallery/SEPIA)" + str(timezone.now()) + ".jpg"
    cv2.imwrite(output,img) 
