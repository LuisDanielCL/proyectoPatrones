# -*- coding: utf-8 -*-
"""
Created on Fri May 11 01:03:10 2018

@author: danie
"""

import cv2
import numpy as np
import math

# CONSTANTES
FILTRO_GAUSSIANO_TAMANO = (5, 5)
BINARIZACION_PESO = 9
BINARIZACION_TAMANO = 19



def grisYbinario(img):
    imgGray = valorImg(img)

    imgGrayContrast = maxContraste(imgGray)
    height, width = imgGray.shape
    imgFiltro = np.zeros((height, width, 1), np.uint8) #Define el tamanno de la imagen filtro
    imgFiltro = cv2.GaussianBlur(imgGrayContrast, FILTRO_GAUSSIANO_TAMANO, 0)
    imgThresh = cv2.adaptiveThreshold(imgFiltro, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY_INV,BINARIZACION_TAMANO, BINARIZACION_PESO)

    return imgGray, imgThresh
# end function
    

def maxContraste(imgGrayscale):

    height, width = imgGrayscale.shape

    imgTopHat = np.zeros((height, width, 1), np.uint8)
    imgBlackHat = np.zeros((height, width, 1), np.uint8)

    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    imgTopHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement)

    imgGrayscalePlusTopHat = cv2.add(imgGrayscale, imgTopHat)
    imgGrayscalePlusTopHatMinusBlackHat = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

    return imgGrayscalePlusTopHatMinusBlackHat
# end function





def valorImg(img):
    height, width, numChannels = img.shape

    imgHSV = np.zeros((height, width, 3), np.uint8)

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    imgHue, imgSaturation, imgValue = cv2.split(imgHSV)

    return imgValue
# end function


