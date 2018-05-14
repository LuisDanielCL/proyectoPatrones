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
    imgGray = valorImg(img) #convierte a escala grises

    imgGrayContrast = maxContraste(imgGray)
    height, width = imgGray.shape
    imgFiltro = np.zeros((height, width, 1), np.uint8)
    imgFiltro = cv2.GaussianBlur(imgGrayContrast, FILTRO_GAUSSIANO_TAMANO, 0)
    #se usa el adaptativo porque facilita cuando existen variaciones de luz
    imgThresh = cv2.adaptiveThreshold(imgFiltro, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY_INV,BINARIZACION_TAMANO, BINARIZACION_PESO)

    return imgGray, imgThresh

    

def maxContraste(img):

    alto, largo = img.shape
    imgTopHat = np.zeros((alto, largo, 1), np.uint8)
    imgBlackHat = np.zeros((alto, largo, 1), np.uint8)
    #crea array de (3x3) con valor 1
    estructura = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    imgTopHat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, estructura)
    imgBlackHat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, estructura)
    imgTopHat = cv2.add(img, imgTopHat)
    imgTopBlackHat = cv2.subtract(imgTopHat, imgBlackHat)

    return imgTopBlackHat





def valorImg(img):
    alto, largo, canales = img.shape
    imgHSV = np.zeros((alto, largo, 3), np.uint8)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgHue, imgSaturation, imgValue = cv2.split(imgHSV)
    return imgValue



