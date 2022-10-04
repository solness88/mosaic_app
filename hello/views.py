from django.forms import MultipleChoiceField
from django.shortcuts import render,redirect
from mosaic_app.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL
from .forms import DocumentForm
from .models import Document
import cv2
from django.conf import settings
from django.utils import timezone
from django.http import FileResponse
import os
import random
import numpy as np
import datetime

def model_form_upload(request):

    DIR = settings.MEDIA_ROOT + "/gallery/"
    pic_amount = sum(os.path.isfile(os.path.join(DIR, name)) for name in os.listdir(DIR))
    if pic_amount > 10:
        for file in os.scandir(DIR):
            os.remove(file.path)     


    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('show_alternatives')

    else:
        form = DocumentForm()
    return render(request, 'hello/model_form_upload.html', {
        'form': form
    })

def show_alternatives(request):
    photo = Document.objects.order_by("id").last()
    url = photo.photo
    path = settings.MEDIA_ROOT + "/" + str(url)
    original_pic_name = os.path.basename(path)
    img = cv2.imread(path)

    # process original image into gray
    img_gray = gray(img)

    # process original image into mosaic
    img_mosaic = mosaic(img)

    # process original image into dotted_animation
    img_pixel = pixel_art(img, 0.5, 4)  

    # process original image into sepia
    img_sepia = sepia(img)

    # get current_time
    now = datetime.datetime.today().strftime('%Y%m%d%H%M%S')

    first_falf_path = settings.MEDIA_ROOT + "/gallery/" + now
    processed_pic_gray = first_falf_path + "【BLACKWHITE】" + original_pic_name
    processed_pic_sepia = first_falf_path + "【SEPIA】" + original_pic_name
    processed_pic_mosaic = first_falf_path + "【MOSAIC】" + original_pic_name
    processed_pic_pixel = first_falf_path + "【PIXEL】" + original_pic_name

    # imwrite processed images
    cv2.imwrite(processed_pic_gray, img_gray)
    cv2.imwrite(processed_pic_sepia, img_sepia)
    cv2.imwrite(processed_pic_mosaic, img_mosaic)
    cv2.imwrite(processed_pic_pixel, img_pixel)

    photo.delete()
    #original_pic = settings.MEDIA_URL + str(url)
    gray_pic_name = settings.MEDIA_URL + 'gallery/' + os.path.basename(processed_pic_gray)
    sepia_pic_name = settings.MEDIA_URL + 'gallery/' + os.path.basename(processed_pic_sepia)
    mosaic_pic_name = settings.MEDIA_URL + 'gallery/' + os.path.basename(processed_pic_mosaic)
    pixel_pic_name = settings.MEDIA_URL + 'gallery/' + os.path.basename(processed_pic_pixel)

    context = {
        'gray_pic_name': gray_pic_name,
        'sepia_pic_name': sepia_pic_name,
        'mosaic_pic_name': mosaic_pic_name,
        'pixel_pic_name': pixel_pic_name,
    }
    return render(request, 'hello/show_alternatives.html', context)


def gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def mosaic(img):
    small = cv2.resize(img, None, fx=0.05, fy=0.05)
    return cv2.resize(small, img.shape[:2][::-1])

# process original image into dotted_animation
def pixel_art(img, alpha=2, K=4):
    img = mosaic_blur(img, alpha)
    return sub_color(img, K)

def sub_color(src, K):
    Z = src.reshape((-1,3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    return res.reshape((src.shape))

def mosaic_blur(img, alpha):
    h, w, ch = img.shape
    img = cv2.resize(img,(int(w*alpha), int(h*alpha)))
    img = cv2.resize(img,(w, h), interpolation=cv2.INTER_NEAREST)
    return img
# until here: process original image into dotted_animation

def sepia(img):
    img[:,:,(0)] = img[:,:,(0)] * 0.3
    img[:,:,(1)] = img[:,:,(1)] * 0.8
    img[:,:,(2)] = img[:,:,(2)]
    return img
