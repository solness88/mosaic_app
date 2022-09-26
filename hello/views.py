from django.shortcuts import render,redirect
from .forms import DocumentForm
from .models import Document
import cv2
from django.conf import settings
from django.utils import timezone

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        photo = Document.objects.order_by("id").last()
        url = photo.photo
        print(photo.picture_type)
        if photo.picture_type == 'black_white':
            gray(url)
        if photo.picture_type == 'mosaic':
            mosaic(url)
        photo.delete()
        return redirect('upload')
    else:
        form = DocumentForm()
    return render(request, 'hello/model_form_upload.html', {
        'form': form
    })

def gray(url):
    path = settings.MEDIA_ROOT + "/" + str(url)
    img = cv2.imread(path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    output = settings.MEDIA_ROOT + "/gallery/gray" + str(timezone.now()) + ".jpg"
    cv2.imwrite(output, img_gray)
    #cv2.imshow("gray_image", img_gray)

def mosaic(url):
    path = settings.MEDIA_ROOT + "/" + str(url)
    img = cv2.imread(path)
    small = cv2.resize(img, None, fx=0.1, fy=0.1)
    img_mosaic = cv2.resize(small, img.shape[:2][::-1])
    output = settings.MEDIA_ROOT + "/gallery/gray" + str(timezone.now()) + ".jpg"
    cv2.imwrite(output, img_mosaic)
