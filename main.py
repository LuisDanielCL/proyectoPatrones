# -*- coding: utf-8 -*-
"""
Created on Thu May 10 18:19:40 2018

@author: danie
"""
import cv2

import ReconocerPlaca

SCALAR_WHITE = (255.0, 255.0, 255.0)


mostrarPasos = True


def main():
    img  = cv2.imread("carro2.jpg")            

    if img is None:                          
        print ("\nError: imagen no fue leida\n\n")                             
        return           
    
    ReconocerPlaca.detectarPlacas(img)


if __name__ == "__main__":
    main()


