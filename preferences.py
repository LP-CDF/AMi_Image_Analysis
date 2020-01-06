#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 09:05:49 2020

@author: ludovic

You can edit this file if you want to modify the shortcuts
"""

from PyQt5 import QtCore

keyboard_layout="qwerty"
# keyboard_layout="azerty"

class Shortcut():
    '''Shortcuts for the GUI'''
    # _translate = QtCore.QCoreApplication.translate
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
    
    #Shortcut to assign classes
    Clear=QtCore.Qt.Key_K
    Crystal=QtCore.Qt.Key_C
    Precipitate=QtCore.Qt.Key_P
    PhaseSep=QtCore.Qt.Key_B
    Other=QtCore.Qt.Key_O
    
class DetectCircle():
    '''parameters for circle detection'''
    param1=35
    param2=25
    minDistance=100
    minRadius=100
    maxRadius=300