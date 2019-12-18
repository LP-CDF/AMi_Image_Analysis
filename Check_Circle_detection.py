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
    gray_blurred = cv2.blur(gray, (3, 3)) 
      
    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred,  
                       cv2.HOUGH_GRADIENT, 1, 100, param1 = 50, 
                   param2 = 30, minRadius =100, maxRadius = 300) 
      
    # Draw circles that are detected. 
    if detected_circles is not None: 
      
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
      
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
      
            # Draw the circumference of the circle. 
            cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
      
            # Draw a small circle (of radius 1) to show the center. 
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3) 
            cv2.imshow("Detected Circle", img) 
            cv2.waitKey(0) 


if __name__ == "__main__":
    if len(sys.argv)<2:
        usage()
        sys.exit()
    filename= sys.argv[len(sys.argv)-1]
    print("File ", filename)
    DetectCircle(filename)
    
    # img = cv2.imread(filename, cv2.IMREAD_COLOR)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray_blurred = cv2.blur(gray, (3, 3)) 
    
    # # Set our filtering parameters 
    # # Initialize parameter setting using cv2.SimpleBlobDetector 
    # params = cv2.SimpleBlobDetector_Params() 
    
    # # Set Area filtering parameters 
    # params.filterByArea = True
    # params.minArea = 1500
    
    # # Set Circularity filtering parameters 
    # params.filterByCircularity = False
    # params.minCircularity = 0.9
      
    # # Set Convexity filtering parameters 
    # params.filterByConvexity = False
    # params.minConvexity = 0.2
          
    # # Set inertia filtering parameters 
    # params.filterByInertia = False
    # params.minInertiaRatio = 0.01
    
    
    # # Create a detector with the parameters 
    # detector = cv2.SimpleBlobDetector_create(params) 
    
    # # Detect blobs 
    # keypoints = detector.detect(gray_blurred)
    
    # # Draw blobs on our image as red circles 
    # blank = np.zeros((1, 1))  
    # blobs = cv2.drawKeypoints(img, keypoints, blank, (0, 0, 255), 
    #                           cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    # number_of_blobs = len(keypoints) 
    # text = "Number of Circular Blobs: " + str(len(keypoints)) 
    # cv2.putText(blobs, text, (20, 550), 
    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2) 
    
    # # Show blobs 
    # cv2.imshow("Filtering Circular Blobs Only", blobs) 
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows() 