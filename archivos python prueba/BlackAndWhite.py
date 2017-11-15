import numpy as np
import cv2
from itertools import *
from os import listdir
from os.path import isfile, join
import time
from operator import itemgetter




def guardar_imagen(img,cont):
    k='byw/imagen'+str(cont)+'.png'
    cv2.imwrite(k,img)



def cargar_imagenes():
    mypath = 'test'
    nombres = []
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    images = np.empty(len(onlyfiles), dtype=object)
    for n in range(0, len(onlyfiles)):
        images[n] = cv2.imread(join(mypath, onlyfiles[n]))
        k=onlyfiles[n].split('.')
        nombres.append(k[0])
    print(len(images))
    return images,nombres

def clear_edges(img):
    return  cv2.medianBlur(img,5)


def imagen_to_black_and_white(img,cont):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    minimo=min_colors(gray)
    im_bw=change_color(gray,minimo)
    guardar_imagen(im_bw,cont)
    return clear_edges(im_bw)

def min_colors(img):
    return img[img>-1].min()

def change_color(img,minimo):
    filas, colum = img.shape
    #print(img.shape)
    """for i in range(filas):
        for j in range(colum):
            if (img[i, j]<minimo+25):
                img[i, j]=0
            else:
                img[i,j]=255"""
    img[img < minimo + 25] = 0
    img[img > 0] = 255
    return img

def dist (x,y):
    x1,y1=x
    x2,y2=y
    return np.sqrt(pow((x1-x2), 2) + pow((y1-y2), 2))


def media(dicc):
    return np.mean(dicc)


def varianza(media,dicc):
    return np.std(dicc)


def coeficiente_varianza(media,varianza):
    return (varianza/media)



def crear_Diccionario(image,num):
    filas, colum, channels=image.shape
    diccionario = {}
    img=imagen_to_black_and_white(image,num)
    elemi1=0
    puntos=[]
    for i in product(range(0,filas),range(elemi1,colum)):
        if(img[i]==0):
            puntos.append(i)
    limite=len(puntos)
    lista=[]
    for i in range(0,limite,1):
        for j in range(i+1,limite,1):
            lista.append(dist(puntos[i],puntos[j]))

    return lista

def principal(image,cont):
    lista=crear_Diccionario(image,cont)
    med=media(lista)
    var=varianza(med,lista)
    coef=coeficiente_varianza(med,var)
    analizar(var,cont)
    return (med,var,coef)


def analizar(coeficiente,name):
    if(coeficiente >=6.5):
        print('la célula',name,'esta en telofase')


initial = time.time()
imagenes,names=cargar_imagenes()
var= []
med = []
co=[]
cont=1
for i in range(len(imagenes)):
    x,y,z=principal(imagenes[i],names[i])
    cont=cont+1
    var.append((x,names[i]))
    med.append((y,names[i]))
    co.append((z,names[i]))

k= len(names)

var=sorted(var, key=itemgetter(0))
med= sorted(med, key=itemgetter(0))
co= sorted(co, key=itemgetter(0))


print('ordenadas por varianza')
for i in range(k):
    print(var[i])

print('ordenadas por media')
for i in range(k):
    print(med[i])

print('ordenadas por coef')
for i in range(k):
    print(co[i])



End = time.time()
print('tiempo=',End-initial)
print('fin')



