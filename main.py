# -*- coding: utf-8 -*-
"""
Created on Thu May 10 18:19:40 2018

@author: danie
"""
import cv2

import ReconocerPlaca

mostrarPasos = False


def main():
    imgOriginalScene  = cv2.imread("1.png")            

    if imgOriginalScene is None:                          
        print ("\nError: imagen no fue leida\n\n")                             
        return                                              


if __name__ == "__main__":
    main()


