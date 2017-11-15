import numpy as np
import cv2
from matplotlib import pyplot as plt

class Filtros:

    def __init__(self,image):
        self.image=image



    def aplicarGaussianFilter(self, x,y,z):
        blur=cv2.GaussianBlur(self,(x,y),0)
        return blur


    def aplicarConvultionFilter(self,n):
        kernel = np.ones((5,5),np.float32)/n
        convultion= cv2.filter2D(self,-1,kernel)
        return convultion

    def aplicarSmoothingFilter(self):
        blur = cv2.blur(self, (5, 5))
        return blur

    def aplicarMediamFilter(self,n):
        mediam=cv2.medianBlur(self,5)
        return mediam

    def aplicarBilateralFilter(self):
        bilateral=cv2.bilateralFilter(self,9,75,75)
        return bilateral
