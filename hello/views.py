from django.shortcuts import render,redirect
from .forms import DocumentForm
from .models import Document
import cv2
from django.conf import settings
from django.utils import timezone
from django.http import FileResponse
import os
from tempfile import TemporaryDirectory

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        photo = Document.objects.order_by("id").last()
        url = photo.photo
        picture_type = photo.picture_type
        if picture_type == 'black_white':
            return redirect('gray')
        elif picture_type == 'mosaic':
            return redirect('mosaic')
        elif picture_type == 'sepia':
            return redirect('sepia')

    else:
        form = DocumentForm()
    return render(request, 'hello/model_form_upload.html', {
        'form': form
    })

#download files
def gray(request):
    with TemporaryDirectory() as tempdir:
        photo = Document.objects.order_by("id").last()
        url = photo.photo
        path = settings.MEDIA_ROOT + "/" + str(url)
        img = cv2.imread(path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        output = tempdir + "BLACKWHITE】" + str(timezone.now()) + ".jpg"
        cv2.imwrite(output, img_gray)
        photo.delete()
        file_name = os.path.basename(output)
        return FileResponse(open(output, "rb"), as_attachment=True, filename=file_name)

# convert into mosaic
def mosaic(url):
    with TemporaryDirectory() as tempdir:
        photo = Document.objects.order_by("id").last()
        url = photo.photo
        path = settings.MEDIA_ROOT + "/" + str(url)
        img = cv2.imread(path)
        small = cv2.resize(img, None, fx=0.1, fy=0.1)
        img_mosaic = cv2.resize(small, img.shape[:2][::-1])
        output = tempdir + "MOSAIC】" + str(timezone.now()) + ".jpg"
        cv2.imwrite(output, img_mosaic)
        photo.delete()
        file_name = os.path.basename(output)
        return FileResponse(open(output, "rb"), as_attachment=True, filename=file_name)

# convert into sepia
def sepia(request):
    with TemporaryDirectory() as tempdir:
        photo = Document.objects.order_by("id").last()
        url = photo.photo
        path = settings.MEDIA_ROOT + "/" + str(url)
        img = cv2.imread(path)
        img[:,:,(0)] = img[:,:,(0)] * 0.3
        img[:,:,(1)] = img[:,:,(1)] * 0.8
        img[:,:,(2)] = img[:,:,(2)]
        output = tempdir + "SEPIA】" + str(timezone.now()) + ".jpg"
        cv2.imwrite(output,img) 
        photo.delete()
        file_name = os.path.basename(output)
        return FileResponse(open(output, "rb"), as_attachment=True, filename=file_name)
