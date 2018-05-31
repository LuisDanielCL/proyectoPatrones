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
import placas

import preproImagen

COLOR_ROJO = (0.0, 0.0, 255.0)
COLOR_BLANCO = (255.0, 255.0, 255.0)


def detectarPlacas(img):
    posPosiblesPlacas = []

    height, width, numChannels = img.shape

    imgGris = np.zeros((height, width, 1), np.uint8)
    imgContraste = np.zeros((height, width, 1), np.uint8)
    imgContorno = np.zeros((height, width, 3), np.uint8)    
    imgGris, imgContraste = preproImagen.grisYbinario(img)        
    caracteresPosibles = buscarPosiblesCaracteres(imgContraste)
    
    if main.mostrarPasos == True: 
        imgContorno = np.zeros((height, width, 3), np.uint8)

        contours = []

        for possibleChar in caracteresPosibles:
            contours.append(possibleChar.contour)
        cv2.drawContours(imgContorno, contours, -1, main.SCALAR_WHITE)
        cv2.imshow("Image con contornos", imgContorno)


    listOfListsOfMatchingCharsInScene = reconocerCaracter.listaDeListasCaracteresSimilares(caracteresPosibles)
    
    if main.mostrarPasos == True:
  
        imgContours = np.zeros((height, width, 3), np.uint8)
    
        for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
            intRandomBlue = random.randint(0, 255)
            intRandomGreen = random.randint(0, 255)
            intRandomRed = random.randint(0, 255)
    
            contours = []
    
            for matchingChar in listOfMatchingChars:
                contours.append(matchingChar.contour)

            cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
    
        cv2.imshow("3", imgContours)
    

    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:                 
        possiblePlate = sacarPlaca(img, listOfMatchingChars)    

        if possiblePlate.imgPlate is not None:                      
            posPosiblesPlacas.append(possiblePlate)                 


    if main.mostrarPasos == True: 
        cv2.imshow("0", img)
        cv2.imshow("Gris", imgGris)
        cv2.imshow("contrastes", imgContraste)
        print ("\n")
        cv2.imshow("4a", imgContours)

        for i in range(0, len(posPosiblesPlacas)):
            p2fRectPoints = cv2.boxPoints(posPosiblesPlacas[i].posPlaca)

            cv2.line(imgContours, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), COLOR_BLANCO, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), COLOR_BLANCO, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), COLOR_BLANCO, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), COLOR_BLANCO, 2)

            cv2.imshow("4a", imgContours)
            cv2.imshow(("4b"+str(i)), posPosiblesPlacas[i].imgPlate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return posPosiblesPlacas
    
def buscarPosiblesCaracteres(imgThresh):
    caracteresPosibles = []

    intCountOfPossibleChars = 0

    imgThreshCopy = imgThresh.copy()

    imgContorno, contornos, herencia = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  

    height, width = imgThresh.shape
    imgContours = np.zeros((height, width, 3), np.uint8)

    for i in range(0, len(contornos)): 
        if main.mostrarPasos == True: 
            cv2.drawContours(imgContours, contornos, i, (255.0, 255.0, 255.0))
        possibleChar = caracter.Caracter(contornos[i])
        if reconocerCaracter.checkIfPossibleChar(possibleChar):
            intCountOfPossibleChars += 1
            caracteresPosibles.append(possibleChar)


    if main.mostrarPasos == True:
        cv2.imshow("Contornos", imgContours)

    return caracteresPosibles


def sacarPlaca(imgOriginal, listaPosiblesCaracteres):
    placaPosible = placas.placas()
    # Ordena para obtener el caracter que se encuentre mas a la izquierda de la lista
    listaPosiblesCaracteres.sort(key = lambda caracterPosible: caracterPosible.intCenterX)        

    # calculate the center point of the plate
    centroX = (listaPosiblesCaracteres[0].intCenterX + listaPosiblesCaracteres[-1].intCenterX) / 2.0
    centroY = (listaPosiblesCaracteres[0].intCenterY + listaPosiblesCaracteres[-1].intCenterY) / 2.0

    centroPlaca = centroX, centroY

    # Ancho y alto de la placa
    anchoPlaca = int((listaPosiblesCaracteres[-1].intBoundingRectX + 
                         listaPosiblesCaracteres[-1].intBoundingRectWidth -
                         listaPosiblesCaracteres[0].intBoundingRectX) * 1.3)
    alturaCaracteres = 0

    for caracterPosible in listaPosiblesCaracteres:
        alturaCaracteres +=  caracterPosible.intBoundingRectHeight


    alturaPromedio = alturaCaracteres / len(listaPosiblesCaracteres)

    placaAltura = int(alturaPromedio * 1.5)

    # calcular angulo
    inclinacion = listaPosiblesCaracteres[-1].intCenterY - listaPosiblesCaracteres[0].intCenterY
    distancia = reconocerCaracter.distanciaCaracteres(listaPosiblesCaracteres[0],listaPosiblesCaracteres[-1])
    angulo = math.asin(inclinacion / distancia) * (180 / math.pi)

    # agregarPosPlaca
    placaPosible.posPlaca = ( tuple(centroPlaca), (anchoPlaca, placaAltura), angulo )

    rotationMatrix = cv2.getRotationMatrix2D(tuple(centroPlaca), angulo, 1.0)
    height, width, numChannels = imgOriginal.shape
    imgRotated = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))
    imgCropped = cv2.getRectSubPix(imgRotated, (anchoPlaca, placaAltura), tuple(centroPlaca))

    placaPosible.imgPlate = imgCropped       
    return placaPosible


    
        