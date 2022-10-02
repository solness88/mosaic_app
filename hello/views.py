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
from tempfile import TemporaryDirectory
import random

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('show_alternatives')
        # photo = Document.objects.order_by("id").last()
        # url = photo.photo
        # picture_type = photo.picture_type
        # if picture_type == 'black_white':
        #     return redirect('gray')
        # elif picture_type == 'mosaic':
        #     return redirect('mosaic')
        # elif picture_type == 'sepia':
        #     return redirect('sepia')

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
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # process original image into mosaic
    small = cv2.resize(img, None, fx=0.05, fy=0.05)
    img_mosaic = cv2.resize(small, img.shape[:2][::-1])

    # process original image into sepia
    img_sepia = img
    img_sepia[:,:,(0)] = img_sepia[:,:,(0)] * 0.3
    img_sepia[:,:,(1)] = img_sepia[:,:,(1)] * 0.8
    img_sepia[:,:,(2)] = img_sepia[:,:,(2)]




    random_num = random.randint(1000000000, 9999999999)
    processed_pic_gray = settings.MEDIA_ROOT + "/gallery/【BLACKWHITE】" + original_pic_name + str(random_num) + ".jpg"
    processed_pic_sepia = settings.MEDIA_ROOT + "/gallery/【SEPIA】" + original_pic_name + str(random_num) + ".jpg"
    processed_pic_mosaic = settings.MEDIA_ROOT + "/gallery/【MOSAIC】" + original_pic_name + str(random_num) + ".jpg"

    # imwrite processed images
    cv2.imwrite(processed_pic_gray, img_gray)
    cv2.imwrite(processed_pic_sepia, img_sepia)
    cv2.imwrite(processed_pic_mosaic, img_mosaic)

    photo.delete()
    #original_pic = settings.MEDIA_URL + str(url)
    gray_pic_name = settings.MEDIA_URL + 'gallery/' + os.path.basename(processed_pic_gray)
    sepia_pic_name = settings.MEDIA_URL + 'gallery/' + os.path.basename(processed_pic_sepia)
    mosaic_pic_name = settings.MEDIA_URL + 'gallery/' + os.path.basename(processed_pic_mosaic)

    context = {
        'gray_pic_name': gray_pic_name,
        'sepia_pic_name': sepia_pic_name,
        'mosaic_pic_name': mosaic_pic_name,
        #'original_pic': original_pic,
    }
    return render(request, 'hello/show_alternatives.html', context)


#download files
# def gray(request):
#     with TemporaryDirectory() as tempdir:
#         photo = Document.objects.order_by("id").last()
#         url = photo.photo
#         path = settings.MEDIA_ROOT + "/" + str(url)
#         img = cv2.imread(path)
#         img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         output = tempdir + "BLACKWHITE】" + str(timezone.now()) + ".jpg"
#         cv2.imwrite(output, img_gray)
#         photo.delete()
#         file_name = os.path.basename(output)
#         return FileResponse(open(output, "rb"), as_attachment=True, filename=file_name)

# convert into mosaic
# def mosaic(request):
#     with TemporaryDirectory() as tempdir:
#         photo = Document.objects.order_by("id").last()
#         url = photo.photo
#         path = settings.MEDIA_ROOT + "/" + str(url)
#         img = cv2.imread(path)
#         small = cv2.resize(img, None, fx=0.1, fy=0.1)
#         img_mosaic = cv2.resize(small, img.shape[:2][::-1])
#         output = tempdir + "MOSAIC】" + str(timezone.now()) + ".jpg"
#         cv2.imwrite(output, img_mosaic)
#         photo.delete()
#         file_name = os.path.basename(output)
# def sepia(request):
#     with TemporaryDirectory() as tempdir:
#         photo = Document.objects.order_by("id").last()
#         url = photo.photo
#         path = settings.MEDIA_ROOT + "/" + str(url)
#         img = cv2.imread(path)
#         img[:,:,(0)] = img[:,:,(0)] * 0.3
#         img[:,:,(1)] = img[:,:,(1)] * 0.8
#         img[:,:,(2)] = img[:,:,(2)]
#         output = tempdir + "SEPIA】" + str(timezone.now()) + ".jpg"
#         cv2.imwrite(output,img) 
#         photo.delete()
#         file_name = os.path.basename(output)
#         return FileResponse(open(output, "rb"), as_attachment=True, filename=file_name)
