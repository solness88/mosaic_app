import cv2
import numpy as np
import copy

# process original image into gray
def gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# process original image into mosaic
def mosaic(img):
    small = cv2.resize(img, None, fx=0.1, fy=0.1)
    return cv2.resize(small, img.shape[:2][::-1])

# process original image into dotted_animation


def pixel_art(img, alpha=2, K=4):
    gamma = 2
    gamma_cvt = np.zeros((256,1),dtype = 'uint8')
    for i in range(256):
        gamma_cvt[i][0] = 255*(float(i)/255)**(1.0/gamma)
    gamma_img = cv2.LUT(img,gamma_cvt)
    pixel_art_img = mosaic_blur(gamma_img, alpha)
    return sub_color(pixel_art_img, K)

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

# sepia color
def sepia(img):
    img_sepia = copy.copy(img)
    img_sepia[:,:,(0)] = img_sepia[:,:,(0)] * 0.3
    img_sepia[:,:,(1)] = img_sepia[:,:,(1)] * 0.8
    img_sepia[:,:,(2)] = img_sepia[:,:,(2)]
    return img_sepia

# edge-preserving effect
def edge_preserving(img):
    edge_preserving = cv2.edgePreservingFilter(img, flags=1, sigma_s=70, sigma_r=0.6)
    return edge_preserving

# oil-painting effect
def oil_painting(img):
    oil_painting = cv2.xphoto.oilPainting(img, 3, 1)
    return oil_painting

def detail_enhance(img):
    return cv2.detailEnhance(img, sigma_s=10, sigma_r=0.15)

def water_color(img):
    gamma = 1.5
    gamma_cvt = np.zeros((256,1),dtype = 'uint8')
    for i in range(256):
        gamma_cvt[i][0] = 255*(float(i)/255)**(1.0/gamma)
    img_gamma = cv2.LUT(img,gamma_cvt)
    return cv2.stylization(img_gamma, sigma_s=60, sigma_r=0.6)
