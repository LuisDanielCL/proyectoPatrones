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
import caracter
import reconocerCaracter

import preproImagen


def detectarPlacas(img):
    posPosiblesPlacas = []

    height, width, numChannels = img.shape

    imgGris = np.zeros((height, width, 1), np.uint8)
    imgContraste = np.zeros((height, width, 1), np.uint8)
    imgContorno = np.zeros((height, width, 3), np.uint8)


    if main.mostrarPasos == True: 
        cv2.imshow("0", img)
        
        
        
    imgGris, imgContraste = preproImagen.grisYbinario(img)        

    if main.mostrarPasos == True: 
        cv2.imshow("Gris", imgGris)
        cv2.imshow("contrastes", imgContraste)
        

        
    caracteresPosibles = buscarPosiblesCaracteres(imgContraste)
    
    if main.mostrarPasos == True: 
        print ("Cant caraceteres posibles = " , str(len(caracteresPosibles)))   

        imgContorno = np.zeros((height, width, 3), np.uint8)

        contours = []

        for possibleChar in caracteresPosibles:
            contours.append(possibleChar.contour)
        cv2.drawContours(imgContorno, contours, -1, main.SCALAR_WHITE)
        cv2.imshow("Image con contornos", imgContorno)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    
def buscarPosiblesCaracteres(imgThresh):
    caracteresPosibles = []

    intCountOfPossibleChars = 0

    imgThreshCopy = imgThresh.copy()

    imgContorno, contornos, herencia = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  

    height, width = imgThresh.shape
    imgContours = np.zeros((height, width, 3), np.uint8)

    for i in range(0, len(contornos)): 
        if main.mostrarPasos == True: 
            cv2.drawContours(imgContours, contornos, i, main.SCALAR_WHITE)
        possibleChar = caracter.Caracter(contornos[i])
        if reconocerCaracter.checkIfPossibleChar(possibleChar):
            intCountOfPossibleChars += 1
            caracteresPosibles.append(possibleChar)


    if main.mostrarPasos == True:
        print (" Posibles caracteres = " , str(intCountOfPossibleChars)) 
        cv2.imshow("Contornos", imgContours)

    return caracteresPosibles

        
        
        