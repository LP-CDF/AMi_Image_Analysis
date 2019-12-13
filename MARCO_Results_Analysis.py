#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 08:31:47 2019

@author: ludovic
"""

import re
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QFont, QColor

from AutoMARCO_Grid import Ui_Dialog

class MARCO_Results(QtWidgets.QDialog, Ui_Dialog):
    ''' autoMARCO_data must be a list containing the data from auto_MARCO.log '''
    def __init__(self, parent=None):
        super(MARCO_Results, self).__init__(parent)
        ui = Ui_Dialog()
        self.setupUi(self)
    

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.paint_MARCO_Results(qp)
        qp.end()

        

    def paint_MARCO_Results(self, qp):
        ''' adapted from https://github.com/dakota0064/Fluorescent_Robotic_Imager '''

        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        wells = ['a', 'b', 'c']

        total_wells = [row + str(col) for row in rows for col in cols]

        def well_to_coordinates(well):
            row = int(ord(well[0])) - 65
            column = int(('').join(re.findall(r'\d+',well))) - 1

            x1 = 80 + (column * 80)
            dx = 60
            y1 = (80 + row * 80)
            dy = 60
            return x1, y1, dx, dy
        
        for row in rows:
            row_int = int(ord(row)) - 65
            y1 = 120 + row_int * 80
            qp.setFont(QFont("Courier New", 20))
            qp.drawText(40, y1,row)  

        for col in cols:
            col_int = int(col) - 1
            x1 = 90 + (col_int * 80)
            qp.setFont(QFont("Courier New", 20))
            qp.drawText(x1, 40, col)  

        for well in total_wells:
            coordinates = well_to_coordinates(well)
            qp.setBrush(QColor(255, 255, 255))
            qp.drawRect(coordinates[0], coordinates[1], coordinates[2], coordinates[3])
        
        
        for line in self.autoMARCO_data:
            if self.subwell!="" and self.subwell in line[0][-1]:
                well=line[0]
                coordinates = well_to_coordinates(well)
                #Crystal
                qp.setBrush(QColor(0, 255, 0))
                qp.drawRect(coordinates[0]+4, coordinates[1], 10, coordinates[3]*float(line[1]))
                #Other
                qp.setBrush(QColor(255, 0, 255))
                qp.drawRect(coordinates[0]+18, coordinates[1], 10, coordinates[3]*float(line[2]))
                #Precipitate
                qp.setBrush(QColor(255, 0, 0))
                qp.drawRect(coordinates[0]+32, coordinates[1], 10, coordinates[3]*float(line[3]))
                #Clear
                qp.setBrush(QColor(0, 0, 0))
                qp.drawRect(coordinates[0]+46, coordinates[1], 10, coordinates[3]*float(line[4]))
            elif self.subwell=="" and line[0][-1] not in wells:
                well=line[0]
                coordinates = well_to_coordinates(well)
                #Crystal
                qp.setBrush(QColor(0, 255, 0))
                qp.drawRect(coordinates[0]+4, coordinates[1], 10, coordinates[3]*float(line[1]))
                #Other
                qp.setBrush(QColor(255, 0, 255))
                qp.drawRect(coordinates[0]+18, coordinates[1], 10, coordinates[3]*float(line[2]))
                #Precipitate
                qp.setBrush(QColor(255, 0, 0))
                qp.drawRect(coordinates[0]+32, coordinates[1], 10, coordinates[3]*float(line[3]))
                #Clear
                qp.setBrush(QColor(0, 0, 0))
                qp.drawRect(coordinates[0]+46, coordinates[1], 10, coordinates[3]*float(line[4]))              
            else:
                continue

