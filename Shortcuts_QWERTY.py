#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 08:58:44 2019

@author: ludovic
"""
from PyQt5 import QtCore, QtGui, QtWidgets


#Shortcuts for GUI

class Shortcut():
    '''Shortcuts for the GUI'''
    _translate = QtCore.QCoreApplication.translate
    #Shortcuts for well navigation in scrollArea
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
