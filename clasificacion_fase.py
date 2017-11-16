import numpy as np
from operator import itemgetter
import cv2

class Clasificador:
    def __init__(self, imagen,nombre, distancias,colores):
        self.__img=imagen
        self.__name=nombre
        self.__dist_lista=distancias
        self.__col_lista=colores

    def guardar_imagen(self,tipo):
        k = tipo+'/imagen' + str(self.__name) + '.png'
        cv2.imwrite(k, self.__img)

    def dist(self,x, y):
        x1, y1 = x
        x2, y2 = y
        return np.sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))

    def media(self):
        return np.mean(self.__dist_lista)

    def varianza(self):
        return np.std(self.__dist_lista)

    def telofase(self):
        var = self.varianza()
        if(var>=6.5):
            self.guardar_imagen('telofase')
            print('la',self.__name,'está en telofase')
            return True
        return False

    def find_min(self):
        min_X=1000
        min_Y=1000
        k=len(self.__col_lista)
        for i in range(k):

            x,y=self.__col_lista[i]
            if(x<min_X):
                min_X=x
            if(y<min_Y):
                min_Y=y
        return min_X,min_Y

    def find_max(self):
        max_X = -10
        max_Y = -10
        k = len(self.__col_lista)
        for i in range(k):
            x, y = self.__col_lista[i]
            if (x >max_X):
                max_X = x
            if (y > max_Y):
                max_Y = y
        return max_X,max_Y

    def find_centroid_cell(self):
        x_min,y_min=self.find_min()
        x_max,y_max=self.find_max()
        x_centroid=int((x_max+x_min)/2)
        y_centroid=int((y_max+y_min)/2)
        centroide=x_centroid,y_centroid
        #print('centroide=',centroide)
        return centroide

    def obtener_bordes(self,img,lista):
        lista=sorted(lista,key=itemgetter(1))
        __,max_y=max(lista,key=itemgetter(1))
        __,min_y=min(lista,key=itemgetter(1))
        lim=len(lista)
        copia=img
        lista_puntos=[]
        punto=-1

        ##primera linea
        for i in range(lim):
            x,y=lista[i]
            if(y==min_y):
                copia[x,y]=0
                lista_puntos.append((x,y))
            else:
                punto=i
                lista_puntos.pop()
                break

        #print(lista_puntos)

        ## ultima linea
        for i in range(lim-1,0,-1):
            x,y=lista[i]
            if(y==max_y):
                copia[x,y]=0
                lista_puntos.append((x,y))
            else:
                fin=i
                lista_puntos.append((x,y))
                copia[x,y]=0
                break
        ant = min_y
        #print(lista_puntos)

        ## el resto
        for i in range(punto,fin-1,1):
            x,y=lista[i]
            if(y!=ant):
                lista_puntos.append(lista[i-1])
                lista_puntos.append(lista[i])
                copia[x,y]=0
                copia[lista[i-1]]=0
                ant=y
            else:
                copia[x,y]=255

        return lista_puntos, copia

    def excentricidad(self):
        centroide = self.find_centroid_cell()
        byw = cv2.imread('byw/imagen' + str(self.__name) + '.png')
        bordes,bordes_img=self.obtener_bordes(byw,self.__col_lista)
        lim=len(bordes)
        dis_centro=[]
        for i in range(lim):
            punto=bordes[i]
            dis_centro.append(self.dist(centroide,punto))

        var=np.std(dis_centro)
        maximo=max(dis_centro)
        minimo=min(dis_centro)
        exce=minimo/maximo
        #print('nombre=',self.__name)
        #print('la excentricidad es',exce)
        #print('la varianza es=',var)
        bordes_img[centroide]=50
        #cv2.imshow('imagen',bordes_img)
        #cv2.waitKey(0)
        return exce,var


    def principal(self):
        sw=self.telofase()
        if(sw==False):
            exc,var=self.excentricidad()
            if (exc>0.35 and exc<0.5):
                print('la ',self.__name,'esta en anafase')
                self.guardar_imagen('anafase')

            elif(exc>=0.5 and exc<0.65):
                print('la ',self.__name,'esta en metafase')
                self.guardar_imagen('metafase')

            elif(exc>=0.65):
                print('la ',self.__name,'esta en profase')
                self.guardar_imagen('profase')

            else:
                print('la ',self.__name,'no pudo ser identificada')
                self.guardar_imagen('sin_clasificar')
