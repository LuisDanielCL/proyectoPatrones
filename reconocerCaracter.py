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


MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0

MIN_PIXEL_AREA = 80

MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8

def checkIfPossibleChar(possibleChar):

    if (possibleChar.intBoundingRectArea > MIN_PIXEL_AREA and
        possibleChar.intBoundingRectWidth > MIN_PIXEL_WIDTH and possibleChar.intBoundingRectHeight > MIN_PIXEL_HEIGHT and
        MIN_ASPECT_RATIO < possibleChar.fltAspectRatio and possibleChar.fltAspectRatio < MAX_ASPECT_RATIO):
        return True
    else:
        return False
    # end if
# end function
