# -*- coding: utf-8 -*-
"""
Created on Fri May 11 01:03:10 2018

@author: danie
"""

import cv2
import numpy as np
import math

# CONSTANTES
FILTRO-GAUSSIANO-TAMANO = (5, 5)
BINARIZACION-PESO = 9
BINARIZACION-TAMANO = 19



def grisYbinario(img):
    imgGray = extractValue(img)

    imgGrayContrast = maximizeContrast(imgGray)
    height, width = imgGray.shape
    imgFiltro = np.zeros((height, width, 1), np.uint8) #Define el tamanno de la imagen filtro
    imgFiltro = cv2.GaussianBlur(imgGrayContrast, FILTRO-GAUSSIANO-TAMANO, 0)
    imgThresh = cv2.adaptiveThreshold(imgFiltro, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY_INV,BINARIZACION-TAMANO, BINARIZACION-PESO)

    return imgGray, imgThresh
# end function
