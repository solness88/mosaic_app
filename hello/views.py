from django.forms import MultipleChoiceField
from django.shortcuts import render,redirect
from mosaic_app.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL
from .forms import DocumentForm
from .models import Document
import cv2, os, datetime, sys, shutil
from django.conf import settings
sys.path.append('./hello/')
import functions

def model_form_upload(request):

    # Delete old pictures from directory
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
    img_gray = functions.gray(img)

    # process original image into mosaic
    img_mosaic = functions.mosaic(img)

    # process original image into dotted_animation
    img_pixel = functions.pixel_art(img, 0.5, 4)  

    # process original image into sepia
    img_sepia = functions.sepia(img)

    # process original image into edgepreserving
    img_edgepreserving = functions.edge_preserving(img)

    # process original image into like oil-painting
    img_oilpainting = functions.oil_painting(img)

    # process original picture into detail-enhanced
    img_detailEnhanced = functions.detail_enhance(img)

    # get current_time
    now = datetime.datetime.today().strftime('%Y%m%d%H%M%S')

    first_falf_path = settings.MEDIA_ROOT + "/gallery/" + now
    processed_pic_gray = first_falf_path + "【BLACKWHITE】" + original_pic_name
    processed_pic_sepia = first_falf_path + "【SEPIA】" + original_pic_name
    processed_pic_mosaic = first_falf_path + "【MOSAIC】" + original_pic_name
    processed_pic_pixel = first_falf_path + "【PIXEL】" + original_pic_name
    processed_pic_oilpainting = first_falf_path + "【OIL】" + original_pic_name
    processed_pic_edgepreserving = first_falf_path + "【EDGE】" + original_pic_name
    processed_pic_detailEnhanced = first_falf_path + "【DETAIL】" + original_pic_name

    # imwrite processed images
    cv2.imwrite(processed_pic_gray, img_gray)
    cv2.imwrite(processed_pic_sepia, img_sepia)
    cv2.imwrite(processed_pic_mosaic, img_mosaic)
    cv2.imwrite(processed_pic_pixel, img_pixel)
    cv2.imwrite(processed_pic_oilpainting, img_oilpainting)
    cv2.imwrite(processed_pic_edgepreserving, img_edgepreserving)
    cv2.imwrite(processed_pic_detailEnhanced, img_detailEnhanced)

    shutil.copy(settings.MEDIA_ROOT + "/" + str(url), '/Users/hirokoba/workspace/mosaic_app/media/gallery/' + now + "【ORIGINAL】" + original_pic_name, )

    #original_pic_rename = os.rename(path, settings.MEDIA_URL + 'gallery/' + now + "【ORIGINAL】" + original_pic_name)
    original_pic = settings.MEDIA_URL + 'gallery/' + original_pic_name
    gray_pic_name = settings.MEDIA_URL + 'gallery/' + os.path.basename(processed_pic_gray)
    sepia_pic_name = settings.MEDIA_URL + 'gallery/' + os.path.basename(processed_pic_sepia)
    mosaic_pic_name = settings.MEDIA_URL + 'gallery/' + os.path.basename(processed_pic_mosaic)
    pixel_pic_name = settings.MEDIA_URL + 'gallery/' + os.path.basename(processed_pic_pixel)
    oilpainting_pic_name = settings.MEDIA_URL + 'gallery/' + os.path.basename(processed_pic_oilpainting)
    edgepreserving_pic_name = settings.MEDIA_URL + 'gallery/' + os.path.basename(processed_pic_edgepreserving)
    detailEnhanced_pic_name = settings.MEDIA_URL + 'gallery/' + os.path.basename(processed_pic_detailEnhanced)

    print(path)

    context = {
        'original_pic': original_pic,
        'gray_pic_name': gray_pic_name,
        'sepia_pic_name': sepia_pic_name,
        'mosaic_pic_name': mosaic_pic_name,
        'pixel_pic_name': pixel_pic_name,
        'oilpainting_pic_name': oilpainting_pic_name,
        'edgepreserving_pic_name': edgepreserving_pic_name,
        'detailEnhanced_pic_name': detailEnhanced_pic_name,
    }
    return render(request, 'hello/show_alternatives.html', context)
