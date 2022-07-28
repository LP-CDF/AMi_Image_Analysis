#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 09:42:40 2020

Adapted from https://gist.github.com/anonymous/1918b6fec0ab55ae681861e1e36ef754
"""

__date__ = "07-07-2022"

import os, sys
import csv
from pathlib import Path
from utils import open_XML

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

ScreenFile={'MD_BCS_Screen':'Md1-105_BCS_Screen.xml',
            'MD_MIDAS':'Md1-107_MIDASPlus.xml',
            'MD_MORPHEUS_FUSION':'Md1-129_Morpheus_Fusion.xml',
            'MD_PACT_Premier':'Md1-36_PACT_Premier_HT.xml',
            'MD-PGA':'Md1-51_pga_screen.xml',
            'NeXtal-Ammonium_Sulfate-Suite':'NeXtal-AmSO4-Suite.xml',
            'Nextal-Classics-Suite': 'NeXtal-Classics-Suite.xml',
            'Nextal-ClassicsII-Suite': 'NeXtal-ClassicsII-Suite.xml',
            'NeXtal-JCSG-Plus-Suite':'NeXtal-JCSG-Plus-Suite.xml',
            'Nextal-MbClassII-Suite': 'NeXtal-MbClass-II-Suite.xml',
            'NeXtal-Nucleix-Suite':'NeXtal-Nucleix-Suite.xml',
            'NeXtal-PEGs-II-Suite':'NeXtal-PEGs-II-Suite.xml',
            'NeXtal-Protein-Complex-Suite':'NeXtal-Protein-Complex-Suite.xml',
            'JBScreen_Classic_HTS_I':'JBScreen_Classic_HTS_I.xml',
            'JBScreen_Classic_HTS_II':'JBScreen_Classic_HTS_II.xml',
            'JBScreen_Classic_1-4':'JBScreen_Classic_1-4.csv',
            'JBScreen_Classic_5-8':'JBScreen_Classic_5-8.csv',
            'JBScreen-JCSG-Plus-Plus':'JBScreen-JCSGPlusPlus.xml',
            'JBScreen_Pi-PEG_HTS':'JBScreen-Pi-PEG_Screen_HTS.xml',
            'JBScreen-XP-Screen':'JBScreen_XP_screen.xml',
            'HR-AdditiveScreen_HT':'HR-Additive_HT_screen.xml',
            'HR-Cryo_HT_screen':'HR-Cryo_HT_screen.xml',
            'HR-PEGRx_HT_screen':'HR-PEGRx_HT_screen.xml',
            'HR-SaltRx_HT_screen':'HR-SaltRx_HT_screen.xml'
            }

class MyTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)
        self.app_path=os.path.abspath(os.path.dirname(sys.argv[0]))


    def open_sheet(self, Screen)->str:
        '''open a csv file, create a Table and returns True or False'''
        # app_path=os.path.abspath(os.path.dirname(sys.argv[0]))
        path=Path(self.app_path).joinpath("Screen_Database", ScreenFile[Screen])

        _check=Path(path).is_file()
        if _check is True:
            with open(path, newline='') as csv_file:
                screen = csv.reader(csv_file, delimiter=',', quotechar='"')
                self.setRowCount(0); self.setColumnCount(10)
                for row_data in screen:
                    row = self.rowCount()
                    self.insertRow(row)
                    if len(row_data) > 10:
                        self.setColumnCount(len(row_data))
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(stuff)
                        self.setItem(row, column, item)
        return _check


    def open_xml(self, _screen)->str:
        '''Read a RockMaker or Dragonfly XML, _file as str, checks if Screen is
        already in database
        _screen is either a file or a screen name in ScreenFile'''

        #checking if _file is in database meaning XML is loaded from a self.action in GUI
        if _screen in ScreenFile.keys():
            path=Path(self.app_path).joinpath("Screen_Database", ScreenFile[_screen])
        else:
            path=Path(_screen)

        screen=open_XML(path)
        self.setRowCount(0); self.setColumnCount(10)
        for i,row_data in screen.items():
            row = self.rowCount()
            self.insertRow(row)
            if len(row_data) > 10:
                self.setColumnCount(len(row_data))
            for column, stuff in enumerate(row_data):
                item = QTableWidgetItem(str(stuff))
                self.setItem(i-1, column, item)
        return screen
        # del screen
        