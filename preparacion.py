import numpy as np
import cv2
import errno
import os
import shutil
import time


from itertools import *
from os import listdir
from os.path import isfile, join
from operator import itemgetter
from clasificacion_fase import Clasificador


def crear_directorios(name):
    k="/"+name
    if os.path.exists(k):
        shutil.rmtree(os.getcwd() + k)
    try:
        os.makedirs(os.getcwd() + k)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def guardar_imagen(img, cont):
    k = 'byw/imagen'+str(cont)+'.png'
    cv2.imwrite(k, img)


def cargar_imagenes():
    mypath = 'test5'
    nombres = []
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    images = np.empty(len(onlyfiles), dtype=object)
    for n in range(0, len(onlyfiles)):
        img = cv2.imread(join(mypath, onlyfiles[n]))
        images[n] = img
        k = onlyfiles[n].split('.')
        nombres.append(k[0])

    print('numero de imagenes=', len(images))
    return images, nombres


def guardar_gris(img, cont, ruta):
    k = ruta+'/imagen' + str(cont) + '.png'
    cv2.imwrite(k, img)


def imagen_to_black_and_white(img,cont):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    guardar_gris(gray, cont, 'gris')
    sw = var_colores(gray, cont)
    minimo, punto = min_colors(gray)
    im_bw = change_color(gray, minimo)
    return clear_edges(im_bw), punto, sw


def clear_edges(img):
    return cv2.medianBlur(img, 5)


def change_color(img, minimo):
    img[img < minimo + 30] = 0
    img[img > 0] = 255
    return img


def dist(x, y):
    x1, y1 = x
    x2, y2 = y
    return np.sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))


def min_colors(img):
    minimo = img[img>-1].min()
    m, n = img.shape
    indice = (0, 0)
    for i in range(m):
        for j in range(n):
            if img[i, j] == minimo:
                indice = (i, j)
    #print(indice)

    return minimo, indice


def fill_holes(img):
    kernel = np.ones((2, 2), np.uint8)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return closing


def crear_Diccionario(image, num):
    filas, colum, channels = image.shape
    img, punto, sw = imagen_to_black_and_white(image, num)
    lista = []
    puntos = []
    if sw is True:
        img = fill_holes(img)
        guardar_imagen(img, num)
        elemi1 = 0
        for i in product(range(0, filas), range(elemi1, colum)):
            if img[i] == 0:
                puntos.append(i)
        limite = len(puntos)
        for i in range(0, limite, 1):
            lista.append(dist(puntos[i], punto))

    return lista, puntos, sw


def var_colores(img, name):
    var = np.std(img)
    #print('name=',name, 'var=',var)
    if var < 40:
        guardar_gris(img, name, 'malas')
        return False
    else:
        guardar_gris(img, name, 'buenas')
        return True


def principal(image, nombre):
    dista, colores, sw = crear_Diccionario(image, nombre)
    if len(colores) > 10 and sw is True:
        classifier = Clasificador(image, nombre, dista, colores)
        med = classifier.media()
        var = classifier.varianza()
        fase = classifier.principal()
        return med, var, fase
    else:
        #print('name=',nombre,'princ no entro')
        return -1, -1, -1


def show_phases(lista, malas):
    print('resultados')
    print('numero de celulas en profase:', lista[1])
    print('numero de celulas en metafase:', lista[2])
    print('numero de celulas en anafase:', lista[3])
    print('numero de celulas en telofase:', lista[4])
    print('numero de celulas sin clasificar', (lista[0]+malas))


def main():
    initial = time.time()
    imagenes, names = cargar_imagenes()
    crear_directorios('byw')
    crear_directorios('gris')
    crear_directorios('malas')
    crear_directorios('buenas')
    crear_directorios('profase')
    crear_directorios('metafase')
    crear_directorios('anafase')
    crear_directorios('telofase')
    crear_directorios('sin_clasificar')
    var = []
    med = []
    fases_vec = [0, 0, 0, 0, 0]
    cont = 0
    malas = 0
    lenIma = len(imagenes)
    for i in range(lenIma):
        media, varianza, fase = principal(imagenes[i], names[i])
        if media == -1 and varianza == -1:
            malas = malas+1
        else:
            fases_vec[fase] = fases_vec[fase]+1
            cont = cont+1
            var.append((varianza, names[i]))
            med.append((media, names[i]))
    print('malas=', malas)
    show_phases(fases_vec, malas)
    var = sorted(var, key=itemgetter(0))
    med = sorted(med, key=itemgetter(0))
    k = len(var)
    """""
    print('ordenadas por varianza')
    for i in range(k):
        print(var[i])
        
    print('ordenadas por media')
    for i in range(k):
        print(med[i])
    
    """""
    end = time.time()
    print('tiempo=', end-initial)
    print('fin')


main()
