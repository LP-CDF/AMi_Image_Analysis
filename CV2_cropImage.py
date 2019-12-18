#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:46:09 2019

@author: ludovic
"""

import os
import re
from pathlib import Path
import cv2 
import numpy as np


_nsre = re.compile('([0-9]+)') #used to sort alphanumerics

def natural_sort_key(s):
     return [int(text) if text.isdigit() else text.lower()
             for text in re.split(_nsre, s)] 

def crop_ROI(image, output_dir, well):
    x, y, r = find_largest_circle(image)
    # print("R, X, Y ", r, x, y)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3)) 
    # image = cv2.resize(image,(599,450), interpolation = cv2.INTER_AREA)
    # mask = np.zeros((599, 450, 3), dtype=np.uint8)
    # cv2.circle(image, (x, y), r, (255, 255, 255), -1, 2, 0)
    # out = (image*mask) - 255
    # white = mask - 255
    
    cropped=image[y-300:y+300, x-300:x+300]
    # cv2.imshow("cropped", image)
    # cv2.waitKey(0)
    
    path=Path(output_dir).joinpath("cropped",well+".jpg")
    cv2.imwrite(str(path), cropped)
    print("well %s saved to %s"%(well, path))
        

def find_largest_circle(image):
    # image = cv2.resize(image,(599,450), interpolation = cv2.INTER_AREA)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3)) 
    circles = cv2.HoughCircles(gray_blurred,  
                    cv2.HOUGH_GRADIENT, 1, 100, param1 = 50, 
                param2 = 30, minRadius = 150, maxRadius = 300)
    # print("circles ", circles)
    R = 0
    X = 0
    Y = 0

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for pt in circles[0, :]: 
            x, y, r = pt[0], pt[1], pt[2]
            if r>R:
                R = int(r)
                X = int(x)
                Y = int(y)
    # print("Rmax, X, Y ", R, X, Y)
    return X,Y,R

if __name__ == "__main__":
    Ext=[".tif",".tiff",".TIFF",".jpg", ".jpeg",".JPG",".JPEG",".png",".PNG"]
    directory = os.getcwd()
    print("directory ", directory)
    files, well_images= [],[]
    
    try:
        os.mkdir('cropped')
    except OSError:
            print ("Creation of the directory %s failed" % 'cropped')
    else:
            print ("Successfully created the directory %s " % 'cropped')
    
    for file in os.listdir(directory):
        if os.path.splitext(file)[1] in Ext:
            files.append(os.path.join(directory, file))    
    
    files.sort(key=natural_sort_key)
    
    for file in files:
        img = cv2.imread(file, cv2.IMREAD_COLOR)
        well=os.path.splitext(os.path.basename(file))[0]
        # print("WELL", well)
        crop_ROI(img, directory, well)
        del img
        