#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:46:09 2019

@author: ludovic pecqueur

usage:
    Execute this script in the directory containing the images to crop
    this will create a directory cropped.
    start the script by typing:
    python3 autocrop.py
    
    Function is now called within GUI.
    Can still be used as standalone script
"""

import os
import re
from pathlib import Path
import cv2
import numpy as np
from preferences import DetectCircle as pref


_nsre = re.compile('([0-9]+)') #used to sort alphanumerics

def natural_sort_key(s):
     return [int(text) if text.isdigit() else text.lower()
             for text in re.split(_nsre, s)] 


def crop_ROI(image, output_dir, well):
    x, y, r = find_best_circle(image)
    if x==0 or y==0: #If No circle was detected 
        print("CROPPED image for well %s is empty, NOT SAVED"%well)
        return False
    r=r+20
    Ymax, Xmax =image.shape[0], image.shape[1]
    if y-r<0:ymin=0
    else:ymin=y-r
    if y+r>Ymax:ymax=Ymax
    else:ymax=y+r
    if x-r<0:xmin=0
    else:xmin=x-r
    if x+r>Xmax:xmax=Xmax
    else: xmax=x+r
    cropped=image[ymin:ymax, xmin:xmax]
    # cropped=image[y-r:y+r, x-r:x+r]
    # print("CROPPED image size well %s "%well, cropped.shape, "r=", r)
    
    path=Path(output_dir).joinpath("cropped",well+".jpg")
    
    #Only save images with bytes otherwise print error message
    if cropped.shape[0] != 0 and  cropped.shape[1] != 0:
        cv2.imwrite(str(path), cropped)
        # print("well %s saved to %s"%(well, path))
    else:
        print("CROPPED image for well %s is empty, NOT SAVED"%well)
        return False
        

def find_best_circle(image):
    '''this is an overkill function title'''
    # image = cv2.resize(image,(599,450), interpolation = cv2.INTER_AREA)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray_blurred = cv2.blur(gray, (3, 3))
    gray_blurred = cv2.GaussianBlur(gray, (3, 3),1)
    w,h = gray.shape[1],gray.shape[0]
    # circles = cv2.HoughCircles(gray_blurred,  
    #                 cv2.HOUGH_GRADIENT, 1, pref.minDistance, param1 = pref.param1, 
    #             param2 = pref.param2, minRadius = pref.minRadius, maxRadius = pref.maxRadius)
    
    #Try to enhance edges
    smooth = cv2.addWeighted(gray_blurred,1.5,gray,-0.5,0)
    circles = cv2.HoughCircles(smooth,  
                cv2.HOUGH_GRADIENT, 1, pref.minDistance, param1 = pref.param1, 
            param2 = pref.param2, minRadius = pref.minRadius, maxRadius = pref.maxRadius)

    R, X, Y = 0, 0, 0
    euclidians=[]
    
    #Find detected circle with max radius closest to center of image, temporary bad solution
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for pt in circles[0, :]:
            x, y, r = pt[0], pt[1], pt[2]
            euclidian=np.sqrt((x - w*0.5)**2+(y - h*0.5)**2)
            euclidians.append((euclidian,r,x,y))
        for i in euclidians:
            if r>R and i[0]==min(euclidians)[0]:
                R = int(i[1])
                X = int(i[2])
                Y = int(i[3])
    # if circles is not None:
    #     print("DISTANCES to image center for %s"%well, euclidians, "MIN distance to image center", min(euclidians))
    del euclidians
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
    
    errors, error_list = 0, []
    for _file in files:
        img = cv2.imread(_file, cv2.IMREAD_COLOR)
        well=os.path.splitext(os.path.basename(_file))[0]
        output=crop_ROI(img, directory, well)
        if output is False:
            errors +=1
            error_list.append(os.path.basename(_file))
        del img, output
    
    log=Path(directory).joinpath("cropped","autocrop.log")
    with open(log, 'w') as f:
        if errors!=0:
            f.write("File(s) that could not be processed correctly \n")
            for err in error_list: f.write(err+"\n")
        else:
            f.write("All Files could be processed.")
    
    print('''
%s file(s) were not processed.
For more information check log file %s

You can use the tool Check_Circle_detection.py filename to check
and modify detection parameters.
'''%(errors, log))
