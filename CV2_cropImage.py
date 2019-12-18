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
    # gray_blurred = cv2.blur(gray, (3, 3))
    gray_blurred = cv2.GaussianBlur(gray, (3, 3),1) 
    
    cropped=image[y-(r+100):y+(r+100), x-(r+100):x+(r+100)]
    # cv2.imshow("cropped", image)
    # cv2.waitKey(0)
    
    path=Path(output_dir).joinpath("cropped",well+".jpg")
    cv2.imwrite(str(path), cropped)
    print("well %s saved to %s"%(well, path))
        

def find_largest_circle(image):
    # image = cv2.resize(image,(599,450), interpolation = cv2.INTER_AREA)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray_blurred = cv2.blur(gray, (3, 3))
    gray_blurred = cv2.GaussianBlur(gray, (3, 3),1) 
    w,h = gray.shape[1],gray.shape[0]
    circles = cv2.HoughCircles(gray_blurred,  
                    cv2.HOUGH_GRADIENT, 1, 100, param1 = 50, 
                param2 = 30, minRadius = 150, maxRadius = 300)
    # print("circles ", circles)
    R = 0
    X = 0
    Y = 0
    moments=[]
    
    #Find circle with max radius closest to center of image, probably bad solution
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for pt in circles[0, :]: 
            x, y, r = pt[0], pt[1], pt[2]
            moment=np.sqrt((x - w*0.5)**2+(y - h*0.5)**2)
            moments.append(moment)
            if r>R and moment==min(moments):
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
    
    for _file in files:
        img = cv2.imread(_file, cv2.IMREAD_COLOR)
        well=os.path.splitext(os.path.basename(_file))[0]
        crop_ROI(img, directory, well)
        del img
        
