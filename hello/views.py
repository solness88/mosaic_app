from django.shortcuts import render,redirect
from .forms import DocumentForm
from .models import Document
import cv2
from django.conf import settings
from django.utils import timezone
import glob
from django.http import FileResponse, HttpResponse
import os
from tempfile import TemporaryDirectory

def model_form_upload(request):


    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        # photo = Document.objects.order_by("id").last()
        # url = photo.photo
        # picture_type = photo.picture_type
        # if picture_type == 'black_white':
        #     gray(url)
        # elif picture_type == 'mosaic':
        #     mosaic(url)
        # elif picture_type == 'sepia':
        #     sepia(url)
        # photo.delete()
        return redirect('file_download')

    else:
        form = DocumentForm()
    return render(request, 'hello/model_form_upload.html', {
        'form': form
    })

#download files
def file_download(request):
    with TemporaryDirectory() as tempdir:
        photo = Document.objects.order_by("id").last()
        url = photo.photo
        picture_type = photo.picture_type
        path = settings.MEDIA_ROOT + "/" + str(url)
        img = cv2.imread(path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # output = settings.MEDIA_ROOT + "/gallery/GRAY)" + str(timezone.now()) + ".jpg"
        output = tempdir + str(timezone.now()) + ".jpg"
        cv2.imwrite(output, img_gray)
        photo.delete()
        file_name = os.path.basename(output)
        return FileResponse(open(output, "rb"), as_attachment=True, filename=file_name)

# remove file that is already downloaded
def download_complete(request):
    altered_pic_dir = './media/gallery/'
    altered_pic = os.listdir(altered_pic_dir)
    if len(altered_pic) != 0:
        for f in altered_pic:
            os.remove(os.path.join(altered_pic_dir, f))
    return render(request, 'hello/model_form_upload.html')

# convert into gray-color
def gray(request):
    photo = Document.objects.order_by("id").last()
    url = photo.photo
    picture_type = photo.picture_type
    path = settings.MEDIA_ROOT + "/" + str(url)
    img = cv2.imread(path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    output = settings.MEDIA_ROOT + "/gallery/GRAY)" + str(timezone.now()) + ".jpg"
    cv2.imwrite(output, img_gray)
    file_path = glob.glob('./media/gallery/*')
    file_name = os.path.basename(file_path[0])
    return FileResponse(open(file_path[0], "rb"), as_attachment=True, filename=file_name)

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
