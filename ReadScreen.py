#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 09:42:40 2020

Adapted from https://gist.github.com/anonymous/1918b6fec0ab55ae681861e1e36ef754
"""

__date__ = "29-06-2022"

import os, sys
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from utils import rows, cols

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

ScreenFile={'MD_BCS_Screen':'Md1-105_BCS_Screen.xml',
            'MD_MIDAS':'Md1-107_MIDASPlus.xml',
            'MD_PACT_Premier':'Md1-36_PACT_Premier_HT.xml',
            'MD-PGA':'Md1-51_pga_screen.xml',
            'MD_MORPHEUS_FUSION':'Md1-129_Morpheus_Fusion.xml',
            'NeXtal-Ammonium_Sulfate_Suite':'NeXtal-AmSO4-Suite.xml',
            'Nextal-MBClassII': 'NeXtal-MbClass-II-Suite.xml',
            'Nextal-Classics-Suite': 'NeXtal-Classics-Suite.xml',
            'Nextal-ClassicsII-Suite': 'NeXtal-ClassicsII-Suite.xml',
            'NeXtal-PEGs-II-Suite':'NeXtal-PEGs-II-Suite.xml',
            'NeXtal-Protein-Complex-Suite':'NeXtal-Protein-Complex-Suite.xml',
            'NeXtal-Nucleix-Suite':'NeXtal-Nucleix-Suite.xml',
            'NeXtal-JCSG-Plus-Suite':'NeXtal-JCSG-Plus-Suite.xml',
            'JBScreen-JCSG-Plus-Plus':'JBScreen-JCSGPlusPlus.xml',
            'JBScreen-XP-Screen':'JBScreen_XP_screen.xml',
            'JBScreen_Classic_HTS_I':'JBScreen_Classic_HTS_I.xml',
            'JBScreen_Classic_HTS_II':'JBScreen_Classic_HTS_II.xml',
            'JBScreen_Classic_1-4':'JBScreen_Classic_1-4.csv',
            'JBScreen_Classic_5-8':'JBScreen_Classic_5-8.csv',
            'JBScreen_Pi-PEG_HTS':'JBScreen-Pi-PEG_Screen_HTS.xml',
            'HR-AdditiveScreen_HT':'HR-Additive_HT_screen.xml',
            'HR-PEGRx_HT_screen':'HR-PEGRx_HT_screen.xml',
            'HR-SaltRx_HT_screen':'HR-SaltRx_HT_screen.xml',
            'HR-Cryo_HT_screen':'HR-Cryo_HT_screen.xml'}

class MyTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)
        self.app_path=os.path.abspath(os.path.dirname(sys.argv[0]))


    def open_sheet(self, Screen):
        # app_path=os.path.abspath(os.path.dirname(sys.argv[0]))
        path=Path(self.app_path).joinpath("Screen_Database", ScreenFile[Screen])
        
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


    def open_xml(self, _screen)->str:
        '''Read a RockMaker or Dragonfly XML, _file as str, checks if Screen is
        already in database
        _screen is either a file or a screen name in ScreenFile'''

        #checking if _file is in database meaning XML is loaded from a self.action in GUI
        if _screen in ScreenFile.keys(): 
            path=Path(self.app_path).joinpath("Screen_Database", ScreenFile[_screen])
        else:
            path=Path(_screen)
        
        if Path(path).is_file():
            tree = ET.parse(path)
            root = tree.getroot()
            #Create Dictionnary of localID: ingredient name    
            DictIng={}
            for chemical in root.iter('ingredients'):
                for ingredient in chemical.iter('ingredient'):
                    localID=[]
                    for stock in ingredient.iter('stock'):
                        DictIng[stock.find('localID').text]= {'name':str(ingredient.find('name').text),'units':str(stock.find('units').text)}
        else:
            return False

        subsections=("concentration","pH") #subsections of interest
        
        #Check number of conditions
        count=0
        for conditions in root.iter('condition'):count+=1
        if count==96: lastcol,lastrow="12","H"
        elif count==48: lastcol,lastrow="6","H"
        elif count==24: lastcol,lastrow="6","D"
        else: count=False #Plate configuration not implemented
        if count!=False:
            total_wells = [row + str(col) for row in rows if rows.index(row)<=rows.index(lastrow) 
                           for col in cols if cols.index(col)<=cols.index(lastcol)]

        i=1; my_screen={}
        for conditions in root.iter('conditions'):
            for condition in conditions.iter('condition'):
                temp=[]
                if count!=False: temp.append(total_wells[i-1])
                else:temp.append(i)
                for ingredient in condition:
                    content=DictIng[ingredient.find('stockLocalID').text]['name']
                    for child in ingredient:
                        # print(child.tag, child.attrib, child.text)
                        if child.tag in subsections:
                            if child.tag=='pH':
                                content+=' '+child.tag+' '+child.text
                            else:
                                content+=' '+child.text+' '+DictIng[ingredient.find('stockLocalID').text]['units']
                    temp.append(content)
                my_screen[i]=temp; i+=1
            # for i,j in my_screen.items(): print(i,j)
                
            self.setRowCount(0); self.setColumnCount(10)
            for i,row_data in my_screen.items():
                row = self.rowCount()
                self.insertRow(row)
                if len(row_data) > 10:
                    self.setColumnCount(len(row_data))
                for column, stuff in enumerate(row_data):
                    item = QTableWidgetItem(str(stuff))
                    self.setItem(i-1, column, item)
        # else : return False
        del tree, root, my_screen, DictIng
        