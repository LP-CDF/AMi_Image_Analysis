#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 09:42:40 2020

Adapted from https://gist.github.com/anonymous/1918b6fec0ab55ae681861e1e36ef754
"""

import os, sys
import csv
from pathlib import Path

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

ScreenFile={'MD_BCS_Screen':'Md1-105_BCS_Screen.csv',
            'MD_MIDAS':'Md1-107_MIDASPlus.csv',
            'MD_PACT_Premier':'Md1-36_PACT_Premier_HT.csv',
            'MD-PGA':'Md1-51_pga_screen.csv',
            'NeXtal-Ammonium_Sulfate_Suite':'NeXtal-AmSO4-Suite.csv',
            'Nextal-MBClassII': 'NeXtal-MbClass-II-Suite.csv',
            'Nextal-Classics-Suite': 'NeXtal-Classics-Suite.csv',
            'Nextal-ClassicsII-Suite': 'NeXtal-ClassicsII-Suite.csv',
            'NeXtal-PEGs-II-Suite':'NeXtal-PEGs-II-Suite.csv',
            'NeXtal-Protein-Complex-Suite':'NeXtal-Protein-Complex-Suite.csv',
            'NeXtal-Nucleix-Suite':'NeXtal-Nucleix-Suite.csv',
            'NeXtal-JCSG-Plus-Suite':'NeXtal-JCSG-Plus-Suite.csv',
            'Jena-JCSG-Plus-Plus':'Jena-JCSGPlusPlus.csv',
            'JBScreen_Classic_HTS_I':'JBScreen_Classic_HTS_I.csv',
            'JBScreen_Classic_HTS_II':'JBScreen_Classic_HTS_II.csv',
            'JBScreen_Classic_1-4':'JBScreen_Classic_1-4.csv',
            'JBScreen_Classic_5-8':'JBScreen_Classic_5-8.csv',
            'Pi-PEG_HTS':'Jena-Pi-PEG_Screen_HTS.csv',
            'HR-PEGRx_HT_screen':'HR-PEGRx_HT_screen.csv',
            'HR-SaltRx_HT_screen':'HR-SaltRx_HT_screen.csv'}

class MyTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)

    def open_sheet(self, Screen):
        app_path=os.path.abspath(os.path.dirname(sys.argv[0]))
        path=Path(app_path).joinpath("Screen_Database", ScreenFile[Screen])
        
        if Path(path).is_file():
            with open(path, newline='') as csv_file:
                my_screen = csv.reader(csv_file, delimiter=',', quotechar='"')
                self.setRowCount(0); self.setColumnCount(10)
                for row_data in my_screen:
                    row = self.rowCount()
                    self.insertRow(row)
                    if len(row_data) > 10:
                        self.setColumnCount(len(row_data))
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(stuff)
                        self.setItem(row, column, item)
            del my_screen
        else : return False
                           
        del app_path, path