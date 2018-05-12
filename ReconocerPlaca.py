# -*- coding: utf-8 -*-
"""
Created on Fri May 11 01:00:51 2018

@author: danie
"""

import cv2
import numpy as np
import math
import main
import random


import preproImagen


def detectarPlacas(img):
    posPosiblesPlacas = []

    height, width, numChannels = img.shape

    imgGris = np.zeros((height, width, 1), np.uint8)
    imgBinaria = np.zeros((height, width, 1), np.uint8)
    imgContorno = np.zeros((height, width, 3), np.uint8)

    cv2.destroyAllWindows()

    if main.mostrarPasos == True: 
        cv2.imshow("0", img)
        
        
        
    imgGris, imgBinaria = preproImagen.grisYbinario(img)         # preprocess to get grayscale and threshold images

    if main.mostrarPasos == True: # show steps #######################################################
        cv2.imshow("1a", imgGris)
        cv2.imshow("1b", imgBinaria)
        
    cv2.waitKey(0)
    cv2.destroyAllWindows()
        
        
        
        
        
        