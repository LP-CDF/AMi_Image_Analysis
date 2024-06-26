#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 09:05:49 2020

@author: ludovic

You can edit this file if you want to modify the shortcuts,
change the circle detection parameters, change colors, scoreclass...

Check_Circle_detection.py, autocrop.py and main program use
the values stored in this file.
"""

from PyQt5 import QtCore

#Keyboard Layout
keyboard_layout="azerty"

USESCORECLASS = True # True or False

MAX_CPU=None #set to desired integer if needed ie MAX_CPU="8" (keep the "")

#Dictionnary used to update color of labelVisuClassif
ClassificationColor={
    "Clear":{"background":"white", "text":"black", "Qcolor":"#ffffff"},
    "Precipitate":{"background":"red", "text":"white","Qcolor":"#ff0000"},
    "Crystal":{"background":"green", "text":"white","Qcolor":"#00ff00"},
    "PhaseSep":{"background":"orange", "text":"black","Qcolor":"#ff7f00"},
    "Other":{"background":"magenta", "text":"white","Qcolor":"#ff00ff"},
    "Unknown":{"background":"yellow", "text":"black","Qcolor":"#ffff00"}
    }

#autoMARCO acceptance probability criterium
autoMARCO_threshold=0.60

#Define score classes. Edit to your need but Order is IMPORTANT !!!
scoreclass=['heavy prec',
            'clear',
            'phase sep',
            'granular prec',
            'crystalline prec',
            'spherulites',
            'micro-crystals',
            'multiple crystals',
            'small crystals',
            '3D crystal']

#Order in database_well_fields is IMPORTANT
database_well_fields=['Target','Plate','date','well', 'subwell', 
                      'reservoir', 'position','Classification', 
                      'Human Score', 'Notes']

class Shortcut():
    '''Shortcuts for the GUI'''
    #Shortcuts for well navigation in scrollArea
    if keyboard_layout=="qwerty":
        MoveUp=QtCore.Qt.Key_W
        MoveDown=QtCore.Qt.Key_S
        MoveLeft=QtCore.Qt.Key_A
        MoveRight=QtCore.Qt.Key_D
    elif keyboard_layout=="azerty":
        MoveUp=QtCore.Qt.Key_Z
        MoveDown=QtCore.Qt.Key_S
        MoveLeft=QtCore.Qt.Key_Q
        MoveRight=QtCore.Qt.Key_D
    else:
        MoveUp=QtCore.Qt.Key_W
        MoveDown=QtCore.Qt.Key_S
        MoveLeft=QtCore.Qt.Key_A
        MoveRight=QtCore.Qt.Key_D
    
    #Shortcut to assign classes: New layout
    Clear=QtCore.Qt.Key_Y
    Crystal=QtCore.Qt.Key_I
    Precipitate=QtCore.Qt.Key_U
    PhaseSep=QtCore.Qt.Key_O
    Other=QtCore.Qt.Key_P    
    
    #Shortcut to assign classes: Old Layout
    # Clear=QtCore.Qt.Key_K
    # Crystal=QtCore.Qt.Key_C
    # Precipitate=QtCore.Qt.Key_P
    # PhaseSep=QtCore.Qt.Key_B
    # Other=QtCore.Qt.Key_O

    
class DetectCircle():
    '''parameters for circle detection used in autocrop.py
       and Check_Circle_detection.py'''
    param1=60
    param2=25
    minDistance=800
    minRadius=250
    maxRadius=400
