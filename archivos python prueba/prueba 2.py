import numpy as np
import cv2
from skimage import data, exposure, img_as_float
from matplotlib import pyplot as plt
from skimage.exposure._adapthist import equalize_adapthist


def showImage(image,name):
    cv2.imshow(name,image)
    cv2.waitKey(0)


def aplicarLaplacian(image):

    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    laplacian = cv2.Laplacian(thresh, cv2.CV_64F)
    cv2.imshow('blanco y negro', laplacian)
    cv2.waitKey(0)
    return laplacian


def aplicarFiltro(image):
    filter=cv2.medianBlur(image,5)
    showImage(filter,'hola')
    return filter


def find_cells(img):
    adaptada= equalize_adapthist(img)
    showImage(adaptada,'name')
    th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                cv2.THRESH_BINARY, 11, 2)
    showImage(th,'con trhesh')
    h, w = th.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Floodfill from point (0, 0)
    floodfill=cv2.floodFill(th, mask, (0, 0), 255);

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(floodfill)

    # Combine the two images to get the foreground.
    im_out = th | im_floodfill_inv




img = cv2.imread('descarga.jpg',0)
find_cells(img)



"""filter=aplicarFiltro(img)
showImage(filter,'hola')
laplacian=aplicarLaplacian(filter)
showImage(laplacian,'goll')"""""
