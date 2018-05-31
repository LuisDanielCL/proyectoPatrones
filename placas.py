# -*- coding: utf-8 -*-
"""
Created on Sun May 27 14:01:54 2018

@author: danie
"""


import cv2
import numpy as np

class placas:


    def __init__(self):
        #sin usar
        self.imgPlate = None
        self.imgGrayscale = None
        self.imgThresh = None
        self.strChars = ""
        #en uso
        self.posPlaca = None


