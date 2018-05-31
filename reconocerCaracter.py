# -*- coding: utf-8 -*-
"""
Created on Mon May 14 01:09:12 2018

@author: danie
"""

import cv2
import numpy as np
import math
import random

import main
import preproImagen
import caracter


#constantes para indentificar caracteres posibles
MIN_ANCHO = 2
MIN_ALTURA = 8
MIN_PROPORCION = 0.25
MAX_PROPORCION = 1.0
AREA_MINIMA = 80


# constantes para comparar caracteres
MAX_DIAGONAL = 5.0

MAX_DIF_AREA = 0.5

MAX_DIF_ANCHO = 0.8
MAX_DIF_ALTO = 0.2

MAX_DIF_ANGULO = 12.0

NUMERO_MINIMO_CARACTERES = 3



#Revisa si lo obtenido es un posible caracter
def checkIfPossibleChar(possibleChar):

    if (possibleChar.intBoundingRectArea > AREA_MINIMA and
        possibleChar.intBoundingRectWidth > MIN_ANCHO and possibleChar.intBoundingRectHeight > MIN_ALTURA and
        MIN_PROPORCION < possibleChar.fltAspectRatio and possibleChar.fltAspectRatio < MAX_PROPORCION):
        return True
    else:
        return False

def listaDeListasCaracteresSimilares(listaPosiblesCaracteres):

    listaCaracteresSimilares = []

    for posibleCaracter in listaPosiblesCaracteres:
        listOfMatchingChars = caracteresSimilares(posibleCaracter, listaPosiblesCaracteres) 
        listOfMatchingChars.append(posibleCaracter)
        
        if len(listOfMatchingChars) < NUMERO_MINIMO_CARACTERES:   
            continue                            
        listaCaracteresSimilares.append(listOfMatchingChars)     
        
        caracteresMenosActuales = []
        caracteresMenosActuales = list(set(listaPosiblesCaracteres) - set(listOfMatchingChars))

        listaRecursiva = listaDeListasCaracteresSimilares(caracteresMenosActuales)   

        for listaCaracteres in listaRecursiva: 
            listaCaracteresSimilares.append(listaCaracteres)
        break
    return listaCaracteresSimilares

def caracteresSimilares(caracterActual, listaCaracteres):

    caracteresSimilares = []

    for posibleCaracterSimilar in listaCaracteres:
        if posibleCaracterSimilar == caracterActual:
            continue                             

        difDistancia = distanciaCaracteres(caracterActual, posibleCaracterSimilar)

        difAngulo = anguloEntreCaracteres(caracterActual, posibleCaracterSimilar)

        difArea = (float(abs(posibleCaracterSimilar.intBoundingRectArea - 
                            caracterActual.intBoundingRectArea)) /
                            float(caracterActual.intBoundingRectArea))
        
        difAncho = (float(abs(posibleCaracterSimilar.intBoundingRectWidth -
                             caracterActual.intBoundingRectWidth)) /
                             float(caracterActual.intBoundingRectWidth))
        
        difAlto = (float(abs(posibleCaracterSimilar.intBoundingRectHeight -
                            caracterActual.intBoundingRectHeight)) /
                            float(caracterActual.intBoundingRectHeight))


        if (difDistancia < (caracterActual.fltDiagonalSize * MAX_DIAGONAL) and
            difAngulo < MAX_DIF_ANGULO and
            difArea < MAX_DIF_AREA and
            difAncho < MAX_DIF_ANCHO and
            difAlto < MAX_DIF_ALTO):
            caracteresSimilares.append(posibleCaracterSimilar)

    return caracteresSimilares


def distanciaCaracteres(firstChar, secondChar):
    intX = abs(firstChar.intCenterX - secondChar.intCenterX)
    intY = abs(firstChar.intCenterY - secondChar.intCenterY)
    return math.sqrt((intX ** 2) + (intY ** 2))

# Tangente con SOH CAH TOA
def anguloEntreCaracteres(firstChar, secondChar):
    fltAdj = float(abs(firstChar.intCenterX - secondChar.intCenterX))
    fltOpp = float(abs(firstChar.intCenterY - secondChar.intCenterY))

    if fltAdj != 0:                     
        angRad = math.atan(fltOpp / fltAdj)
    else:
        angRad = 1.5

    angulo = angRad * (180.0 / math.pi) 

    return angulo

