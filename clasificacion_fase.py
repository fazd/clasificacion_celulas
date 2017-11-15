import numpy as np
from operator import itemgetter


class Clasificador:
    def __init__(self, imagen, distancias,colores):
        self.__img=imagen
        self.__dist_lista=distancias
        self.__col_lista=colores

    def dist(x, y):
        x1, y1 = x
        x2, y2 = y
        return np.sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))


    def media(self):
        return np.mean(self.__dist_lista)

    def varianza(self):
        return np.std(self.__dist_lista)


    def telofase(self,nombre):
        var = self.varianza()
        if(var>=6.5):
            print('la',nombre,'está en telofase')
            return True
        return False



    def excentricidad(self):
        distancias = sorted(self.__dist_lista)
        lim = len(self.__dist_lista)
        if (lim % 2 == 0):
            medio = lim / 2
        else:
            medio = (lim + 1) / 2

        primera = 0
        segunda = 0
        medio = int(medio)
        for i in range(medio):
            primera = primera + distancias[i]

        for i in range(medio + 1, lim, 1):
            segunda = segunda + distancias[i]
        if (primera == 0 and segunda == 0):
            return 0
        else:
            exc = primera / segunda

        return exc











