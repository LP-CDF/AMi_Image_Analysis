#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 07:21:08 2019

@author: ludovic

Taken from https://www.geeksforgeeks.org/circle-detection-using-opencv-python/
"""


import cv2
import sys
import numpy as np
from preferences import DetectCircle as pref


def usage():
    print("""
USAGE=''' ./Check_Circle_detection.py filename'''
""")


def DetectCircle(_file):  
    # Read image. 
    img = cv2.imread(_file, cv2.IMREAD_COLOR) 
      
    # Convert to grayscale. 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
      
    # Blur using 3 * 3 kernel. 
    gray_blurred = cv2.GaussianBlur(gray, (3, 3),1)
    w,h = gray.shape[1],gray.shape[0]
      
    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred,  
                       cv2.HOUGH_GRADIENT, 1, pref.minDistance , param1 = pref.param1, 
                   param2 = pref.param1, minRadius =pref.minRadius, maxRadius = pref.maxRadius) 
    
    euclidians=[]
    
    # Draw circles that are detected. 
    if detected_circles is not None: 
      
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
      
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2]
            euclidian=np.sqrt((a - w*0.5)**2+(b - h*0.5)**2)
            euclidians.append((euclidian, r))
            
            mask=np.zeros((gray.shape[0],gray.shape[1]), np.uint8)
            
            #Create mask, extract ROI and calculate mean
            cv2.circle(mask, (a,b), r+100, (255,255,255), -1)
            new_img=cv2.bitwise_and(gray, gray, mask=mask)
            # mean=cv2.mean(new_img, mask=mask)[::-1]
            # print("Mean value of circle ", mean)
            
            # Draw the circumference of the circle. 
            cv2.circle(img, (a, b), r, (0, 255, 0), 2)
      
            # Draw a small circle (of radius 1) to show the center. 
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
            
            resized_img = cv2.resize(img, (600,451), interpolation = cv2.INTER_AREA)
            resized_ROI = cv2.resize(new_img, (600,451), interpolation = cv2.INTER_AREA)
            
            cv2.imshow("Detected Circle", resized_img) 
            cv2.imshow("ROI with radius+100", resized_ROI) 
            cv2.waitKey(0)
        
    if len(euclidians)!=0:
        print("DISTANCES to image center ", euclidians, "min DISTANCE to image center", min(euclidians)[0])


if __name__ == "__main__":
    if len(sys.argv)<2:
        usage()
        sys.exit()
    filename= sys.argv[len(sys.argv)-1]
    print("File ", filename)
    DetectCircle(filename)