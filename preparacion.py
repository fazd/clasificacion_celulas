import numpy as np
import cv2
from itertools import *
from os import listdir
from os.path import isfile, join
import time
from operator import itemgetter
from clasificacion_fase import Clasificador


def guardar_imagen(img,cont):
    k='byw/imagen'+str(cont)+'.png'
    cv2.imwrite(k,img)

def cargar_imagenes():
    mypath = 'test3'
    nombres = []
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    images = np.empty(len(onlyfiles), dtype=object)
    for n in range(0, len(onlyfiles)):
        img=cv2.imread(join(mypath, onlyfiles[n]))
        images[n] = img
        k=onlyfiles[n].split('.')
        nombres.append(k[0])

    print(len(images))
    return images,nombres


def guardar_gris(img,cont,ruta):
    k = ruta+'/imagen' + str(cont) + '.png'
    cv2.imwrite(k, img)

def imagen_to_black_and_white(img,cont):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    guardar_gris(gray,cont,'gris')
    var_colores(gray,cont)
    minimo,punto=min_colors(gray)
    im_bw=change_color(gray,minimo)
    return clear_edges(im_bw),punto

def clear_edges(img):
    return  cv2.medianBlur(img,5)

def change_color(img,minimo):
    img[img < minimo + 27] = 0
    img[img > 0] = 255
    return img

def dist(x, y):
    x1, y1 = x
    x2, y2 = y
    return np.sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))

def min_colors(img):
    minimo=img[img>-1].min()
    m,n=img.shape
    indice=(0,0)
    for i in range(m):
        for j in range(n):
            if (img[i,j]==minimo):
                indice=(i,j)
    #print(indice)

    return minimo,indice

def fill_holes(img):
    kernel = np.ones((2, 2), np.uint8)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return closing

def crear_Diccionario(image,num):
    filas, colum, channels=image.shape
    img,punto=imagen_to_black_and_white(image,num)
    img=fill_holes(img)
    guardar_imagen(img,num)
    elemi1=0
    puntos=[]
    for i in product(range(0,filas),range(elemi1,colum)):
        if(img[i]==0):
            puntos.append(i)
    limite=len(puntos)
    lista=[]
    for i in range(0,limite,1):
        lista.append(dist(puntos[i],punto))
    return lista,puntos

def var_colores(img,name):
    var=np.std(img)
    print('name=',name, 'var=',var)
    if(var<40):
        guardar_gris(img,name,'malas')
    else:
        guardar_gris(img,name,'buenas')





def principal(image,nombre):
    dista,colores=crear_Diccionario(image,nombre)
    if(len(colores)>10):

        classifier = Clasificador(image,dista,colores)
        med=classifier.media()
        var=classifier.varianza()
        excentricidad=classifier.excentricidad()
        estado=classifier.telofase(nombre)

        return (med,var,excentricidad)
    else:
        return (-1,-1,-1)




def main ():
    initial = time.time()
    imagenes,names=cargar_imagenes()
    var= []
    med = []
    excentricidad=[]
    cont =0
    malas=0
    lenIma=len(imagenes)
    for i in range(lenIma):
        media,varianza,exce=principal(imagenes[i],names[i])
        if(media==-1 and varianza==-1 and exce==-1):
            malas=malas+1
        else:
            cont=cont+1
            var.append((varianza,names[i]))
            med.append((media,names[i]))
            excentricidad.append((exce,names[i]))
    print('malas=',malas)
    var=sorted(var, key=itemgetter(0))
    med= sorted(med, key=itemgetter(0))
    excentricidad= sorted(excentricidad, key=itemgetter(0   ))
    k = len(var)
    """print('las excentricidaes son celulas')
    for i in range(cont):
        print(excentricidad[i])
    """
    """""
    print('ordenadas por varianza')
    for i in range(k):
        print(var[i])
        
    print('ordenadas por media')
    for i in range(k):
        print(med[i])
    
    """""

    End = time.time()
    print('tiempo=',End-initial)
    print('fin')

main()
