#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 13:57:18 2019

@author: ludovic
"""

from gui import Ui_MainWindow
import os
import sys
import datetime
import re
import csv
import math
from pathlib import Path
import multiprocessing
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtWidgets import (QTableWidgetItem, QFileDialog, QSplashScreen,
                             QMessageBox, QGridLayout, QStyleFactory,
                             QProgressDialog, QInputDialog, QLineEdit)
from utils import (ensure_directory, initProject, _RAWIMAGES, Ext,rows,
                   cols, open_XML, utilViewer)
from shutil import copyfile
import pdf_writer
import HeatMap_Grid
from MARCO_Results_Analysis import MARCO_Results
import PlateOverview
import StatisticsDialog
from tools import Merge_Zstack
import ReadScreen
import ExternalViewer
import preferences as pref
import subprocess

QtWidgets.QApplication.setAttribute(
    QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
QtWidgets.QApplication.setAttribute(
    QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons
QtWidgets.QApplication.setAttribute(
    QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

__version__ = "1.2.5"
__author__ = "Ludovic Pecqueur (ludovic.pecqueur \at college-de-france.fr)"
__date__ = "19-12-2022"
__license__ = "New BSD http://www.opensource.org/licenses/bsd-license.php"


#Dictionnary used to update color of labelVisuClassif. Definition in preferences.py
ClassificationColor = pref.ClassificationColor


def Citation():
    print(f'''
Program written by
Ludovic Pecqueur
Laboratoire de Chimie des Processus Biologiques
Collège de France.

Please acknowledge the use of this program and give
the following link:
https://github.com/LP-CDF/AMi_Image_Analysis  
  
licence: %s
2019-{datetime.date.today().year}
''' % __license__)


class ViewerModule(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        # print("self.app_path ", self.app_path)
        self.SplashScreen(2000)
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.setWindowTitle(f"LCPB AMi Image Analysis version {__version__}")

        self._nsre = re.compile('([0-9]+)')  # used to sort alphanumerics

        content_widget = QtWidgets.QWidget()
        self.scrollAreaPlate.setWidget(content_widget)
        self._lay = QGridLayout(content_widget)

        timeline_widget = QtWidgets.QWidget()
        self.scrollArea_Timeline.setWidget(timeline_widget)
        self._timlay = QGridLayout(timeline_widget)

        self.os = sys.platform  # Name of the OS
        self.files = []  # Full path of Z-stacked images
        self.well_images = []  # Only names of well images
        self.reservoirs = []  # Only names of unique well
        self.directory = str
        self.rootDir = str  # Full path where folders at different times are
        self.imageDir = str  # Full path where images at a given time are
        self.project = str  # Name of the project
        self.target = str  # Name of the protein within the project
        self.plate = str  # Name of the plate
        self.date = str  # Date of images
        # self.timed = str  # Time of images
        self.prepdate = str  # Date of plate preparation
        self.classifications = {}  # Dictionnary in memory containing well:classif
        self.scores = {} # Dictionnary in memory containing well:score
        self.WellHasNotes = {}  # Dictionnary in memory containing well:True/False
        self.previousWell = None
        self.currentWell = None
        self.currentButtonIndex = None
        self.VisiblesIdx = []  # list in memory with index of visible well widgets
        self.InitialNotes = None
        self.InitialClassif = None
        self.InitialScore = None
        # Name of the directory containing individual Z-focus images
        self.rawimages = _RAWIMAGES
        self.TimelineInspector = None
        self.MARCO = None  # Automated_Marco Predictor object
        self.Predicter = None  # Automated_Marco predicter
        self.DatabaseDict=dict()
        self.currentScreen=None
        self.pixmap=None
        self.ScreenTable=None
        self.StatisticsWindow=None
        self.idx=None
        self.prep_date_path=None
        self.current_image=None
        self.imageP=None    #Image in Project Viewer
        self.pixmapP=None   #Image in Project Viewer

        #If using the QGraphics view, use open_image
        #If not comment the next five lines and use
        #function LoadWellImage
        self.ImageViewer=utilViewer(self.ImageViewer_1)
                
        #Project Tab
        self.ProjectInspector = utilViewer(self.ImageViewer_2)

        #To see all autoMARCO results windows create a dict subwell:object
        self.MARCO_window = {}
        #To see all Plates windows create a dict subwell:object
        self.PLATE_window = {}
        #Create a dict with all crystallization cocktails
        self.CreateScreenDictDatabase()
        
        #Populate comboBoxes
        self.comboBoxScreen.addItem(None)
        for _key,_value in self.DatabaseDict.items():
            self.comboBoxScreen.addItem(_key)
        self.comboBoxScore.addItem(None)

        if pref.USESCORECLASS is True:
            for _i in range(1,len(pref.scoreclass)+1):
                self.comboBoxScore.addItem(str(_i) + str(f' ({pref.scoreclass[_i-1]})'))
        else:
            for _i in range(1,11):
                self.comboBoxScore.addItem(str(_i))
                
        #Enable, disable GUI items
        self.openFile.setEnabled(False)
        self.EnableDisableGUI(False)

        self.initUI()

    def SplashScreen(self, ms):
        '''ms is the time in ms to show splash screen'''
        _image = Path(self.app_path).joinpath("SplashScreen.png")
        self.splash = QSplashScreen(QPixmap(str(_image)))
        self.splash.show()
        QtCore.QTimer.singleShot(ms, self.splash.close)
        
    def EnableDisableGUI(self,_var)->bool:
        '''Enable / Disable several GUI options'''
        self.actionAutomated_Annotation_MARCO.setEnabled(_var)
        self.actionAutoMARCO_current_image.setEnabled(_var)
        self.actionCalculate_Statistics.setEnabled(_var)
        self.actionDisplay_Heat_Map.setEnabled(_var)
        self.pushButton_CopyToNotes.setEnabled(_var)
        self.pushButton_DisplayHeatMap.setEnabled(_var)
        self.pushButton_ExportToPDF.setEnabled(_var)
        self.menuShow_autoMARCO_Grid.setEnabled(_var)
        self.actionChange_Preparation_date.setEnabled(_var)
        self.comboBoxProject.setEnabled(_var)

    def EnableDisableautoMARCO(self,_var)->bool:
        '''Enable / Disable several GUI options'''
        self.actionAutomated_Annotation_MARCO.setEnabled(_var)
        self.actionAutoMARCO_current_image.setEnabled(_var)
        self.menuShow_autoMARCO_Grid.setEnabled(_var)
        self.pushButton_Evaluate.setEnabled(_var)

    def initUI(self):

        self.MaxCol = 6

        #Shortcut definitions

        # self.exportPDFshortcut=QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+E"), self)
        # self.exportPDFshortcut.activated.connect(self.export_pdf)

        #Setup Menu
        self.openFile.triggered.connect(self.openFileNameDialog)
        self.openDir.triggered.connect(lambda: self.openDirDialog(dialog=True))

        self.actionAutoCrop.triggered.connect(self.AutoCrop)
        self.actionAutoMerge.triggered.connect(self.AutoMerge)
        self.actionAutomated_Annotation_MARCO.triggered.connect(
            self.autoAnnotation)
        self.actionAutoMARCO_current_image.triggered.connect(
            self.annotateCurrent)
        self.actionDisplay_Heat_Map.triggered.connect(self.show_HeatMap)
        self.actionExport_to_PDF.triggered.connect(self.export_pdf)
        self.actionDelete_Folder_rawimages.triggered.connect(
            lambda: self.DeleteFolder(self.imageDir, self.rawimages))
        self.actionDelete_Folder_cropped.triggered.connect(
            lambda: self.DeleteFolder(self.imageDir, "cropped"))
        self.actionautoMARCO_subwell_a.triggered.connect(
            lambda: self.show_autoMARCO("a"))
        self.actionautoMARCO_subwell_b.triggered.connect(
            lambda: self.show_autoMARCO("b"))
        self.actionautoMARCO_subwell_c.triggered.connect(
            lambda: self.show_autoMARCO("c"))
        self.actionautoMARCO_no_subwell.triggered.connect(
            lambda: self.show_autoMARCO(""))
        self.actionChange_Preparation_date.triggered.connect(
            self.editdate_updateGUI)

        self.actionPlateSubwell_a.triggered.connect(
            lambda: self.show_Plates("a"))
        self.actionPlateSubwell_b.triggered.connect(
            lambda: self.show_Plates("b"))
        self.actionPlateSubwell_c.triggered.connect(
            lambda: self.show_Plates("c"))
        self.actionPlateno_subwell.triggered.connect(
            lambda: self.show_Plates(""))
        self.PlateScreenshot_subwell_a.triggered.connect(
            lambda: self.take_plate_screenshot("a"))
        self.PlateScreenshot_subwell_b.triggered.connect(
            lambda: self.take_plate_screenshot("b"))
        self.PlateScreenshot_subwell_c.triggered.connect(
            lambda: self.take_plate_screenshot("c"))
        self.PlateScreenshot_no_subwell.triggered.connect(
            lambda: self.take_plate_screenshot(""))

        #Crystallization Screens
        self.actionMD_PGA.triggered.connect(
            lambda: self.show_xmlScreen("MD-PGA"))
        self.actionNextal_MbClassII_Suite.triggered.connect(
            lambda: self.show_xmlScreen("Nextal-MbClassII-Suite"))
        self.actionNeXtal_Ammonium_Sulfate_Suite.triggered.connect(
            lambda: self.show_xmlScreen("NeXtal-Ammonium_Sulfate-Suite"))
        self.actionNextal_Classics_Suite.triggered.connect(
            lambda: self.show_xmlScreen("Nextal-Classics-Suite"))
        self.actionNextal_ClassicsII_Suite.triggered.connect(
            lambda: self.show_xmlScreen("Nextal-ClassicsII-Suite"))
        self.actionNextal_PEGII_Suite.triggered.connect(
            lambda: self.show_xmlScreen("NeXtal-PEGs-II-Suite"))
        self.actionNeXtal_Protein_Complex_Suite.triggered.connect(
            lambda: self.show_xmlScreen("NeXtal-Protein-Complex-Suite"))
        self.actionNeXtal_Nucleix_Suite.triggered.connect(
            lambda: self.show_xmlScreen("NeXtal-Nucleix-Suite"))
        self.actionJena_JCSG_Plus_Plus.triggered.connect(
            lambda: self.show_xmlScreen("JBScreen-JCSG-Plus-Plus"))
        self.actionJBScreen_Classic_HTS_I.triggered.connect(
            lambda: self.show_xmlScreen("JBScreen_Classic_HTS_I"))
        self.actionJBScreen_Classic_HTS_II.triggered.connect(
            lambda: self.show_xmlScreen("JBScreen_Classic_HTS_II"))
        self.actionJBScreen_Classic_1_4.triggered.connect(
            lambda: self.show_csvScreen("JBScreen_Classic_1-4"))
        self.actionJBScreen_Classic_5_8.triggered.connect(
            lambda: self.show_csvScreen("JBScreen_Classic_5-8"))
        self.actionXP_Screen.triggered.connect(
            lambda: self.show_xmlScreen("JBScreen-XP-Screen"))
        self.actionPi_PEG_HTS.triggered.connect(
            lambda: self.show_xmlScreen("JBScreen_Pi-PEG_HTS"))
        self.action_Additive_screen_HT.triggered.connect(
            lambda: self.show_xmlScreen("HR-AdditiveScreen_HT"))
        self.actionPeg_Rx1Rx2.triggered.connect(
            lambda: self.show_xmlScreen("HR-PEGRx_HT_screen"))
        self.actionSaltRx.triggered.connect(
            lambda: self.show_xmlScreen("HR-SaltRx_HT_screen"))
        self.action_Cryo_HT.triggered.connect(
            lambda: self.show_xmlScreen("HR-Cryo_HT_screen"))
        self.actionMD_PACT_Premier.triggered.connect(
            lambda: self.show_xmlScreen("MD_PACT_Premier"))
        self.actionNextal_JCSG_Plus.triggered.connect(
            lambda: self.show_xmlScreen("NeXtal-JCSG-Plus-Suite"))
        self.actionMD_MIDAS.triggered.connect(
            lambda: self.show_xmlScreen("MD_MIDAS"))
        self.actionMD_BCS_Screen.triggered.connect(
            lambda: self.show_xmlScreen("MD_BCS_Screen"))        
        self.actionMD_MORPHEUS_Fusion.triggered.connect(
            lambda: self.show_xmlScreen("MD_MORPHEUS_FUSION"))
        self.actionimport_RockMaker_XML.triggered.connect(self.openXMLDialog)

        self.actionQuit_2.triggered.connect(self.on_exit)

        self.actionCalculate_Statistics.triggered.connect(self.show_Statistics)
        self.actionShortcuts.triggered.connect(self.ShowShortcuts)
        self.actionAbout.triggered.connect(self.ShowAbout)
        self.actionManual.triggered.connect(self.ShowManual)

        self.label_ProjectDetails.setFont(
            QtGui.QFont("Arial", 12, QtGui.QFont.Black))

        self.ImageViewer_1.setStyleSheet(
            """background-color:transparent;border: 1px solid black;""")
        self.labelVisuClassif.setStyleSheet(
            """background-color:yellow;color:black;""")

        #Setup Filtering Options
        self.radioButton_All.toggled.connect(
            lambda: self.FilterClassification(self._lay, "All"))
        self.radioButton_Crystal.toggled.connect(
            lambda: self.FilterClassification(self._lay, "Crystal"))
        self.radioButton_Clear.toggled.connect(
            lambda: self.FilterClassification(self._lay, "Clear"))
        self.radioButton_Other.toggled.connect(
            lambda: self.FilterClassification(self._lay, "Other"))
        self.radioButton_Precipitate.toggled.connect(
            lambda: self.FilterClassification(self._lay, "Precipitate"))
        self.radioButton_PhaseSep.toggled.connect(
            lambda: self.FilterClassification(self._lay, "PhaseSep"))
        self.radioButton_Unsorted.toggled.connect(
            lambda: self.FilterClassification(self._lay, "Unknown"))
        self.radioButton_HasNotes.toggled.connect(
            lambda: self.FilterNotes(self._lay))
        self.radioButton_Subwella.toggled.connect(
            lambda: self.FilterSubwell(self._lay, "a"))
        self.radioButton_Subwellb.toggled.connect(
            lambda: self.FilterSubwell(self._lay, "b"))
        self.radioButton_Subwellc.toggled.connect(
            lambda: self.FilterSubwell(self._lay, "c"))

        #Stylesheet scrollAreaPlate and some Qlabel
        self.scrollAreaPlate.setStyleSheet(
            """background-color: rgb(220,220,220);""")
        self.label_LastSaved.setStyleSheet(
            """background-color: rgb(230,230,230);""")

        #Change Some Styles in Scoring Section
        self.label_2.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Black))
        self.label_4.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Black))
        self.label_Timeline.setFont(
            QtGui.QFont("Arial", 12, QtGui.QFont.Black))
        self.label_CurrentWell.setFont(
            QtGui.QFont("Arial", 12, QtGui.QFont.Black))
        self.label_CurrentWell.setStyleSheet("""color: blue;""")

        self.radioButton_ScoreClear.setStyleSheet("""color: black;""")
        self.radioButton_ScorePrecipitate.setStyleSheet("""color: red;""")
        self.radioButton_ScoreCrystal.setStyleSheet("""color: green;""")
        self.radioButton_ScorePhaseSep.setStyleSheet("""color: orange;""")
        self.radioButton_ScoreOther.setStyleSheet("""color: magenta;""")
        self.radioButton_ScoreUnknown.setStyleSheet("""color: black;""")

        #Listen Scoring RadioButtons
        self.radioButton_ScoreClear.toggled.connect(
            lambda: self.SetDropClassif(self.radioButton_ScoreClear, self.currentWell))
        self.radioButton_ScorePrecipitate.toggled.connect(lambda: self.SetDropClassif(
            self.radioButton_ScorePrecipitate, self.currentWell))
        self.radioButton_ScoreCrystal.toggled.connect(
            lambda: self.SetDropClassif(self.radioButton_ScoreCrystal, self.currentWell))
        self.radioButton_ScorePhaseSep.toggled.connect(
            lambda: self.SetDropClassif(self.radioButton_ScorePhaseSep, self.currentWell))
        self.radioButton_ScoreOther.toggled.connect(
            lambda: self.SetDropClassif(self.radioButton_ScoreOther, self.currentWell))
        self.radioButton_ScoreUnknown.toggled.connect(
            lambda: self.SetDropClassif(self.radioButton_ScoreUnknown, self.currentWell))

        #Listen Display Heat Map and export to pdf buttons, other push buttons
        self.pushButton_DisplayHeatMap.clicked.connect(self.show_HeatMap)
        self.pushButton_ExportToPDF.clicked.connect(self.export_pdf)
        self.pushButton_Evaluate.clicked.connect(self.annotateCurrent)
        self.pushButton_CopyToNotes.clicked.connect(lambda: self.copytoNotes(self.currentScreen,self.currentWell))

        #Show shortcut in GUI for class selection
        self.label_ShortcutClear.setText(
            "(%s)" % QKeySequence(pref.Shortcut.Clear).toString())
        self.label_ShortcutPrec.setText(
            "(%s)" % QKeySequence(pref.Shortcut.Precipitate).toString())
        self.label_ShortcutCrystal.setText(
            "(%s)" % QKeySequence(pref.Shortcut.Crystal).toString())
        self.label_ShortcutPhaseSep.setText(
            "(%s)" % QKeySequence(pref.Shortcut.PhaseSep).toString())
        self.label_ShortcutOther.setText(
            "(%s)" % QKeySequence(pref.Shortcut.Other).toString())
        
        #Listen comboBoxes
        self.comboBoxScreen.activated.connect(self.setScreen)
        self.comboBoxScore.activated.connect(lambda: self.setScore(self.currentWell))
        
        #Project Tab
        classes=['Clear',
                 'Crystal',
                 'Precipitate',
                 'PhaseSep',
                 'Other',
                 'Unknown'
                 ]
        self.comboBoxProject.addItem(None)
        for i in classes:
            self.comboBoxProject.addItem(i)
        self.comboBoxProject.setCurrentIndex(0)
        
        self.comboBoxProject.activated.connect(lambda: self.searchClassifProject())
        self.pushButtonResetProject.clicked.connect(self.resetProject)
        self.tableViewProject.cellClicked.connect(self.cellClickedTable)
        self.comboBoxTargetFilter.activated.connect(lambda: self.filterTable(self.comboBoxTargetFilter.currentText(),
                                                                             self.tableViewProject))
        
        self.show()
                   
    def show_HeatMap(self):
        ''' Create window and map results on a grid'''
        if len(self.classifications) == 0:
            self.handle_error("No data yet!!!")
            return False
        self.heatmap_window = HeatMap_Grid.HeatMapGrid()
        self.heatmap_window.setWindowTitle(
            "Heat Map: %s (%s)" % (self.plate, self.date))
        self.heatmap_window.well_images = self.well_images
        self.heatmap_window.classifications = self.classifications
        self.heatmap_window.score = self.scores
        self.heatmap_window.notes = self.WellHasNotes
        self.heatmap_window.pushButton_ExportImage.clicked.connect(lambda: self.take_screenshot(
            self.heatmap_window, "HeatMap_Grid_%s_%s" % (self.plate, self.date)))
        self.heatmap_window.pushButton_Close.clicked.connect(
            self.heatmap_window.close)
        self.heatmap_window.show()

    def show_csvScreen(self, Screen):
        '''Screen is taken from key ScreenFile dictionnary in ReadScreen.py '''
        self.ScreenTable = ReadScreen.MyTable(10, 10)
        self.ScreenTable.setWindowTitle("%s" % Screen)
        data = self.ScreenTable.open_sheet(Screen)
        # self.ScreenTable.setColumnWidth(0, 100)
        self.ScreenTable.resize(1000, 500)

        if data is True:
            header = self.ScreenTable.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            self.ScreenTable.show()
        else:
            self.handle_error("WARNING: File %s not found in database" %
                              ReadScreen.ScreenFile[Screen])

    def show_xmlScreen(self, fileName):
        path = Path(fileName)
        self.ScreenTable = ReadScreen.MyTable(10, 10)
        self.ScreenTable.setWindowTitle(path.stem)

        if path.stem in self.DatabaseDict:
            data = self.DatabaseDict[path.stem]
        else:
            data = open_XML(fileName)
        
        if data is None:
            self.handle_error(
                "WARNING: unexpected format for file %s" % fileName)
            return
        else:
            self.ScreenTable.create_table(data)
            
        self.ScreenTable.resize(1000, 500)
        header = self.ScreenTable.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ScreenTable.show()

    def CreateScreenDictDatabase(self):
        '''Create a dict of dict containing all screens and crystallization
           conditions
           only load .xml formatted screens'''
        ScreenFile=ReadScreen.ScreenFile
        
        for _screen in ScreenFile.keys():
            path=Path(self.app_path).joinpath("Screen_Database", ScreenFile[_screen])
            if Path(path).suffix=='.xml':
                self.DatabaseDict[_screen]=open_XML(str(path))
        # for i,j in self.DatabaseDict.items(): print(i,j)

    def FindCrystCocktail(self,screen,well):
        '''find crystallization cocktail in database and return a list'''
        if well[-1] in ['a', 'b', 'c']:
            well=well[:-1]
        # cocktail=self.DatabaseDict[screen][self.reservoirs.index(well)+1]
        # if cocktail[0] != well:
        for i,j in self.DatabaseDict[screen].items():
            if j[0]==well:
                cocktail=j
                break
        return cocktail

    def show_autoMARCO(self, subwell):
        ''' Create window and map results on a grid'''

        if len(self.classifications) == 0:
            self.handle_error(
                "Please choose a directory containing the images first")
            return

        _file = Path(self.rootDir).joinpath(
            "Image_Data", self.date, "auto_MARCO.log")

        if Path(_file).exists():
            with open(_file, 'r') as f:
                data = f.readlines()
        else:
            self.handle_error("File %s not found" % _file)
            return

        autoMARCO_data = []

        for line in data:
            autoMARCO_data.append(line.split())
        #delete HEADER from list
        del autoMARCO_data[0]

        self.MARCO_window[subwell] = MARCO_Results()
        self.MARCO_window[subwell].subwell = subwell
        self.MARCO_window[subwell].setWindowTitle(
            "autoMARCO results for subwell %s" % subwell)
        self.MARCO_window[subwell].autoMARCO_data = autoMARCO_data

        #Define Legend
        self.MARCO_window[subwell].label_Crystal.setStyleSheet(
            """background-color:rgb(0, 255, 0)""")
        self.MARCO_window[subwell].label_Other.setStyleSheet(
            """background-color:rgb(255, 0, 255); color:rgb(255, 255, 255)""")
        self.MARCO_window[subwell].label_Precipitate.setStyleSheet(
            """background-color:rgb(255, 0, 0); color:rgb(255, 255, 255)""")
        self.MARCO_window[subwell].label_Clear.setStyleSheet(
            """background-color:rgb(0, 0, 0); color:rgb(255, 255, 255)""")

        self.MARCO_window[subwell].show()
        del autoMARCO_data

    def show_Plates(self, subwell):
        ''' Create window and map results on a grid'''

        if len(self.classifications) == 0:
            self.handle_error(
                "Please choose a directory containing the images first")
            return
        if subwell in self.PLATE_window:
            self.PLATE_window[subwell].UpdateBorder(
                self.files, self.classifications)
            self.PLATE_window[subwell].show()
        else:
            self.PLATE_window[subwell] = PlateOverview.Plate(
                9, 13, self.rootDir, self.date, self.files)
            self.PLATE_window[subwell].subwell = subwell
            self.PLATE_window[subwell].setWindowTitle(
                f"Plate Overview: {self.plate} ({self.date}) | subwell {subwell}")
            self.PLATE_window[subwell].create_table(
                self.files, self.classifications)
            self.PLATE_window[subwell].setStyleSheet(
                """background-color: rgb(240,240,240)""")
            self.PLATE_window[subwell].resize(1520, 810)
            self.PLATE_window[subwell].show()
            self.PLATE_window[subwell].testSignal.connect(lambda: self.ShowPlateSel(subwell))
        QtGui.QPixmapCache.clear()

    def ShowPlateSel(self, subwell):
        '''Show well selected in Plate Overview in the main window'''
        well,path=self.PLATE_window[subwell].CLICKED, self.PLATE_window[subwell].RETURNPATH
        self.open_image(path)
        self.currentWell=well
        self.dothings(well)    

    def show_Statistics(self):
        '''Calculate statistics on the plate'''
        #Check data before going further
        if len(self.classifications) == 0:
            self.handle_error("No data yet!!!")
            return False

        self.StatisticsWindow = QtWidgets.QDialog()
        ui = StatisticsDialog.Ui_Dialog()
        ui.setupUi(self.StatisticsWindow)
        results = self.Calculate_Statistics()
        positions = [(i, j) for i in range(6) for j in range(4)]
        # print("positions ", positions)

        for pos in positions:
            if pos[0] == 0:
                value = results[pos[1]]['Clear']
            elif pos[0] == 1:
                value = results[pos[1]]['Precipitate']
            elif pos[0] == 2:
                value = results[pos[1]]['Crystal']
            elif pos[0] == 3:
                value = results[pos[1]]['PhaseSep']
            elif pos[0] == 4:
                value = results[pos[1]]['Other']
            else:
                value = results[pos[1]]['Unknown']

            ui.StatisticsTable.setItem(
                pos[0], pos[1], QTableWidgetItem(str(value)))

        self.StatisticsWindow.show()
        ui.pushButton_Export.clicked.connect(
            lambda: self.export_statistics(results))

    def export_statistics(self, _list):
        filename = Path(self.rootDir).joinpath(
            "Image_Data", "Statistics_%s_%s.csv" % (self.plate, self.date))

        with open(filename, 'w', newline='') as f:
            fieldnames = ["Classification", "Subwell_a",
                          "Subwell_b", "Subwell_c", "No_Subwell"]
            writer = csv.DictWriter(
                f, fieldnames, delimiter=',', quoting=csv.QUOTE_ALL, dialect="excel")
            writer.writeheader()
            writer.writerow({'Classification': 'Clear', 'Subwell_a': _list[0]['Clear'], 'Subwell_b': _list[
                            1]['Clear'], 'Subwell_c': _list[2]['Clear'], 'No_Subwell': _list[3]['Clear']})
            writer.writerow({'Classification': 'Precipitate', 'Subwell_a': _list[0]['Precipitate'], 'Subwell_b': _list[
                            1]['Precipitate'], 'Subwell_c': _list[2]['Precipitate'], 'No_Subwell': _list[3]['Precipitate']})
            writer.writerow({'Classification': 'Crystal', 'Subwell_a': _list[0]['Crystal'], 'Subwell_b': _list[
                            1]['Crystal'], 'Subwell_c': _list[2]['Crystal'], 'No_Subwell': _list[3]['Crystal']})
            writer.writerow({'Classification': 'Phase Separation', 'Subwell_a': _list[0]['PhaseSep'], 'Subwell_b': _list[
                            1]['PhaseSep'], 'Subwell_c': _list[2]['PhaseSep'], 'No_Subwell': _list[3]['PhaseSep']})
            writer.writerow({'Classification': 'Other', 'Subwell_a': _list[0]['Other'], 'Subwell_b': _list[
                            1]['Other'], 'Subwell_c': _list[2]['Other'], 'No_Subwell': _list[3]['Other']})
            writer.writerow({'Classification': 'Unsorted', 'Subwell_a': _list[0]['Unknown'], 'Subwell_b': _list[
                            1]['Unknown'], 'Subwell_c': _list[2]['Unknown'], 'No_Subwell': _list[3]['Unknown']})
        message = "File saved to:\n %s" % filename
        self.informationDialog(message)

    def AutoCrop(self):
        if len(self.files) == 0:
            self.handle_error(
                "Please choose a directory containing the images first!!!")
            return

        try:
            import cv2
            import autocrop
            if cv2.__version__ < '4.0.1':
                self.handle_error(
                    "openCV version %s not supported" % cv2.__version__)
                return
        except ModuleNotFoundError:
            self.handle_error("module cv2 not found")
            return False

        path = Path(self.imageDir).joinpath("cropped")
        _f = ensure_directory(path)
        if _f is not None:  # if Permission issue
            self.handle_error(
                f"> {_f}\n\nYou must change the permissions to continue")
            return

        errors, error_list = 0, []
        count, size = 0, len(self.files)

        progress = QProgressDialog("Processing files...", "Abort", 0, size)
        progress.setWindowTitle("AutoCrop")
        progress.setMinimumWidth(300)
        progress.setModal(True)

        for _file in self.files:
            progress.setValue(count+1)
            img = cv2.imread(_file, cv2.IMREAD_COLOR)
            well = os.path.splitext(os.path.basename(_file))[0]
            output = autocrop.crop_ROI(img, self.imageDir, well)
            if output is False:
                errors += 1
                error_list.append(well)
            del img, output
            count += 1
            if progress.wasCanceled():
                break

        log = Path(path).joinpath("autocrop.log")
        with open(log, 'w') as f:
            if errors != 0:
                f.write("File(s) that could not be processed correctly \n")
                for err in error_list:
                    f.write(err+"\n")
            else:
                f.write("All Files could be processed.")

        if errors != 0:
            self.handle_error('''
%s file(s) were not processed.
For more information check log file %s

you can use the tool Check_Circle_detection.py filename to check
and modify detection parameters.
''' % (errors, log))

        #INFORM USER TO RELOAD images from cropped if needed
        self.informationDialog(
            "You need to load the images from the directory \"cropped\" to use the cropped images")

    def AutoMerge(self):
        # from utils import _RAWIMAGES
        self.informationDialog(f'''
                               
Please open the directory {_RAWIMAGES} !!!
The GUI will not be responsive during processing.

You can check progress in the terminal window.

''')
        self.openDirDialog()
        if len(self.files) == 0:
            return

        nproc = multiprocessing.cpu_count()
        #To Fix multiprocessing issue with OSX Catalina
        if self.os == 'darwin' and multiprocessing.get_start_method() != 'forkserver':
            multiprocessing.set_start_method('forkserver', force=True)

        # rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        # cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        wells = ['a', 'b', 'c']
        total_wells = [row + str(col) + str(well)
                       for row in rows for col in cols for well in wells]

        path = str(Path(self.imageDir).parent)

        if self.well_images[0].split('_')[0][-1] in ['a', 'b', 'c']:
            SUBWELL = True
        else:
            SUBWELL = False

        if SUBWELL == False:
            filtered = []
            for i in range(len(total_wells)):
                if total_wells[i][:-1] not in filtered:
                    filtered.append(total_wells[i][:-1])
            total_wells = filtered

        args = []
        for well in total_wells:
            arg = well, self.well_images, self.imageDir, path
            args.append(arg)

        njobs = len(args)

        MAX_CPU = pref.MAX_CPU
        if MAX_CPU is not None:
            try:
                int(MAX_CPU)
                if int(MAX_CPU) >= nproc:
                    MAX_CPU = nproc-1
            except:
                self.handle_error(
                    f"ABORTING, MAX_CPU not set properly, you must edit the value of MAX_CPU in:\n{self.app_path}/preferences.py \nand restart the GUI")
                return

        if nproc == 1:
            number_processes = 1
        elif njobs >= nproc and nproc != 1:
            if MAX_CPU is None:
                number_processes = nproc-1
            else:
                number_processes = int(MAX_CPU)

        print("Number of CORES = ", nproc,
              "Number of processes= ", number_processes)
        time_start = time.perf_counter()
        pool = multiprocessing.Pool(number_processes)
        results = [pool.apply_async(
            Merge_Zstack.MERGE_Zstack2, arg) for arg in args]
        pool.close()
        pool.join()
        time_end = time.perf_counter()

        self.informationDialog(f'''
Operation performed in {time_end - time_start:0.2f} seconds.

Merged images were automatically loaded from : \n {path}''')

        last = self.well_images[-1].split("_")[0]+".jpg"
        if Path(path).joinpath(last).is_file():
            with open(str(Path(path).joinpath("DONE")), 'w'):
                pass

        #Clean up
        for i in total_wells:
            del i
        del results, total_wells
        #autoLoad Merged
        self.openDirDialog(dialog=False, directory=path)

    def ShowShortcuts(self):
        shortcut = pref.Shortcut()
        BoxShortCuts = QMessageBox()
        text = '''
    Well navigation shortcuts:
    MoveUp= %s
    MoveDown= %s
    MoveLeft= %s
    MoveRight= %s
    
    Scoring shortcuts:
    Clear= %s
    Precipitate= %s
    Crystal= %s
    Phase Separation= %s
    Other= %s
    
        ''' % (QKeySequence(shortcut.MoveUp).toString(),
               QKeySequence(shortcut.MoveDown).toString(),
               QKeySequence(shortcut.MoveLeft).toString(),
               QKeySequence(shortcut.MoveRight).toString(),
               QKeySequence(shortcut.Clear).toString(),
               QKeySequence(shortcut.Precipitate).toString(),
               QKeySequence(shortcut.Crystal).toString(),
               QKeySequence(shortcut.PhaseSep).toString(),
               QKeySequence(shortcut.Other).toString())
        BoxShortCuts.information(self, "Shortcuts", text)
        del shortcut

    def ShowAbout(self):
        about = QMessageBox()
        text = f'''
AMi Image Analysis version {__version__}
Program written For Python 3 and PyQt5
by:
Ludovic Pecqueur
Chimie des Processus Biologiques
College de France
Paris, France
https://www.college-de-france.fr/site/en-chemistry-of-biological-processes/index.htm

Released under licence:
%s    
2019-{datetime.date.today().year}
 
GitHub repository:
https://github.com/LP-CDF/AMi_Image_Analysis    
 ''' % __license__
        about.information(self, "About", text)

    def ShowManual(self):
        path = Path(self.app_path).joinpath("Manual_AMi_Image_Analysis.pdf")
        if self.os == 'linux':
            import webbrowser
            webbrowser.open(str(path))
        else:
            from subprocess import run
            run(['open', path], check=True)

    def openXMLDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "XML Files (*.xml *.XML)", options=options)
        if fileName:
            self.show_xmlScreen(fileName)
        #Import temporarily Screen into database
        self.DatabaseDict[Path(fileName).stem]=open_XML(fileName)
        #Update comboBoxScreen List if item not present
        if self.comboBoxScreen.findText(Path(fileName).stem) == -1:
            self.comboBoxScreen.addItem(Path(fileName).stem)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "All Files (*);;Image Files (*.tiff *.tif *.jpg *.jpeg *.png *.PNG)", options=options)
        if fileName:
            print(fileName)
        if fileName:
            self.open_image(fileName)
            #Next line to activate zoom capability
            self.previousWell = self.extract_WellLabel(fileName)

    def Initialise(self, directory):
        '''directory is pathlib.Path object'''
        PATHS = initProject(directory)
        self.rawimages = PATHS.rawimages
        self.rootDir = PATHS.rootDir
        self.project = PATHS.project
        self.date = PATHS.date
        # self.timed = PATHS.timed
        self.target = PATHS.target
        self.plate = PATHS.plate
        self.prep_date_path = PATHS.prep_date_path
        self.imageDir = str(Path.resolve(directory))
        self.label_LastSaved.setText("")

        if self.rootDir is not None:
            if Path(self.prep_date_path).exists():
                with open(self.prep_date_path) as file:
                    self.prepdate = file.read().strip("\n")
            else:
                text, okPressed = QInputDialog.getText(
                    self, "File prep_date.txt not found", "Preparation date (format: YYYYMMDD)     ", QLineEdit.Normal, "")
                if okPressed and text != '':
                    try:
                        datetime.datetime.strptime(text, '%Y%m%d')
                        with open(self.prep_date_path, 'w') as f:
                            f.write(text)
                        self.prepdate = text
                    except:
                        self.handle_error(
                            f"Input date \"{text}\" not with correct format, skipping calculation of number of days")
                        self.prepdate = "None"
                else:
                    self.prepdate = "None"

    def Reset(self):
        '''reset file list and more when changing folder and reset layout grid'''
        self.classifications.clear()
        self.scores.clear()
        self.WellHasNotes.clear()
        self.rootDir = None
        self.previousWell = None
        self.currentWell = None
        self.currentScreen = None
        self.comboBoxScreen.setCurrentIndex(0)
        self.comboBoxScore.setCurrentIndex(0)
        self.currentButtonIndex = None
        self.idx = None
        self.files.clear()
        self.well_images.clear()
        self.reservoirs.clear()
        self.ClearLayout(self._lay)
        self.ClearLayout(self._timlay)
        self.MARCO_window.clear()
        self.PLATE_window.clear()
        self.InitialNotes = None
        self.InitialClassif = None
        self.InitialScore = None
        self.prepdate = "None"
        self.label_NDays.setText("Not available")
        self.EnableDisableGUI(False)

    def editdate_updateGUI(self):
        '''edit date in prep_date.txt'''
        if self.rootDir is not None:
            if Path(self.prep_date_path).exists():
                with open(self.prep_date_path) as file:
                    self.prepdate = file.read().strip("\n")
        text, okPressed = QInputDialog.getText(
                    self, "Change date for current plate", "Preparation date (format: YYYYMMDD)     ", QLineEdit.Normal, self.prepdate)
        if okPressed and text != '':
            try:
                datetime.datetime.strptime(text, '%Y%m%d')
                with open(self.prep_date_path, 'w') as f:
                    f.write(text)
                self.prepdate = text
            except:
                self.handle_error(
                    f"Input date \"{text}\" not with correct format, skipping calculation of number of days")
                self.prepdate = "None"
                
        self.PrepDate.setText(str(self.prepdate))
        if self.prepdate != "None":
            d0 = datetime.date(int(self.prepdate[0:4]), int(
                self.prepdate[4:6]), int(self.prepdate[6:]))
            d1 = datetime.date(int(self.date[0:4]), int(
                self.date[4:6]), int(self.date[6:]))
            delta = d1 - d0
            self.label_NDays.setText(str(delta.days))
            del d0, d1, delta        

    def createUniqueReservoirs(self, _list)->list:
        '''Create list of unique reservoirs, input is list of well image names'''
        if Path(_list[0]).stem[-1] in ['a', 'b', 'c']:
            SUBWELL = True
        else:
            SUBWELL = False

        if SUBWELL is True:
            for _well in _list:
                reservoir=Path(_well).stem[:-1]
                if reservoir not in self.reservoirs:
                    self.reservoirs.append(reservoir)
        else:
            self.reservoirs=[Path(_well).stem for _well in _list if Path(_well).stem not in self.reservoirs]
        # print("self.reservoirs: ", self.reservoirs)

    def openDirDialog(self, dialog=True, directory=''):
        self.Reset()
        if dialog is True:
            directory = str(QFileDialog.getExistingDirectory(
                self, "Directory containing Images"))
        if directory == '':
            return
        else:
            directory = Path(directory)

        #Initialise Project Details
        if directory:
            self.Initialise(directory)
            print("Plate root directory : ", self.rootDir)
            self.ProjectCode.setText(self.project)
            self.PrepDate.setText(str(self.prepdate))
            self.ImageDate.setText(self.date)
            self.TargetName.setText(self.target)
            self.PlateName.setText(self.plate)

            if self.prepdate != "None":
                d0 = datetime.date(int(self.prepdate[0:4]), int(
                    self.prepdate[4:6]), int(self.prepdate[6:]))
                try:
                    d1 = datetime.date(int(self.date[0:4]), int(
                        self.date[4:6]), int(self.date[6:]))
                except:
                    message = '''Unexpected directory name!!! \nAre you are opening the correct directory?'''
                    self.handle_error(message)
                    return
                delta = d1 - d0
                self.label_NDays.setText(str(delta.days))
                del d0, d1, delta

        if directory:
            self.files_it = iter([os.path.join(directory, file) for file in os.listdir(
                directory) if os.path.splitext(file)[1] in Ext])
            for file in os.listdir(directory):
                if os.path.splitext(file)[1] in Ext:
                    self.files.append(os.path.join(directory, file))
                    self.well_images.append(os.path.basename(file))
        if len(self.files) != 0:
            #sorting the output of os.listdir after filtering
            self.files.sort(key=self.natural_sort_key)
            self.well_images.sort(key=self.natural_sort_key)
            self._timer = QtCore.QTimer(self, interval=1)
            self._timer.timeout.connect(self.on_timeout)
            self._timer.start()
            self.check_previous_notes(self.rootDir, self.date)
            self.EnableDisableGUI(True)
#            QtGui.QPixmapCache.clear()
        else:
            self.handle_error("No Image File Found in directory")
            return

        for i in self.well_images:
            well = os.path.splitext(i)[0]
            self.CheckClassificationAndNotes(self.rootDir, self.date, well)

        #Create list of unique reservoirs
        self.createUniqueReservoirs(self.well_images)
        
        #line below to reset Filter to All
        self.radioButton_All.setChecked(True)


    def export_pdf(self):
        '''export to PDF a report for current well'''
        if self.previousWell is None:
            self.handle_error("No well selected")
            return

        rootDir = self.rootDir
        imgDir = self.imageDir
        img_list = self.well_images
        values = []
        # name = ""
        well = self.currentWell

        values.append(well)

        imgpath = self.buildWellImagePath(imgDir, well, img_list)
    #        path = directory + "/" + well
        pdfpath = Path(rootDir).joinpath(
            "Image_Data", "%s_%s.pdf" % (well, self.date))
    #        pdfpath=pdfpath + "/" + filename
        values.append(imgpath)

        values.append(self.project)
        values.append(self.target)
        values.append(self.plate)
        values.append(self.date)
        values.append(self.prepdate)
        values.append(pdfpath)
        text = self.Notes_TextEdit.toPlainText()
        values.append(text)
        pdf_writer.create_pdf(values)
        print("Report for well %s saved to %s" % (well, pdfpath))
        self.label_LastSaved.setText(f"### Report for {well} saved ###")

    @staticmethod
    def buildWellImagePath(directory, well, wellimage_list):
        '''search for a substring, returns a list, use first element
        directory is a string'''
        search = list(filter(lambda i: well in i, wellimage_list))
        path = directory + "/" + search[0]
        return path

    def handle_error(self, error):
        """Handle when an error occurs
        Show the error in an error message window.
        """
        em = QMessageBox(self)
#        em.setIcon(QMessageBox.Critical)
        em.setWindowTitle("Error!")
        em.setText(error)
        em.show()

    def informationDialog(self, message):
        info = QMessageBox(self)
        info.setWindowTitle("Information!")
        info.setText(message)
        info.setStandardButtons(QMessageBox.Ok)
        retval = info.exec_()

    def natural_sort_key(self, s):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split(self._nsre, s)]

    def GenerateGrid(self, filelist):
        MaxCol = self.MaxCol
        MaxRow = math.ceil(len(filelist)/MaxCol)+1
        positions = [(i, j) for i in range(MaxRow) for j in range(MaxCol)]
        return positions

    def on_timeout(self):
        positions = self.GenerateGrid(self.files)
        vmax = len(self.files)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(vmax)
        count = 0
        for position, name in zip(positions, self.files):
            #            print(position, name)
            try:
                # file = next(self.files_it)
                next(self.files_it)
                self.add_button(name, position[0], position[1])
                self.progressBar.setValue(count+1)
                count += 1
            except StopIteration:
                self._timer.stop()
                self.progressBar.setValue(vmax)
        #Needed here for shortcuts to run at first data load, why?
        self.SetAllVisible()
        
    @staticmethod
    def add_pixmap(layout, pixmap, x, y):
        if not pixmap.isNull():
            label = QtWidgets.QLabel(pixmap=pixmap)
            layout.addWidget(label, x, y, alignment=QtCore.Qt.AlignCenter)

    # def add_Timeline_pixmap(self, layout, pixmap, x, y):
    #     if not pixmap.isNull():
    #         label = QtWidgets.QLabel(pixmap=pixmap)
    #         layout.addWidget(label, x, y, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)
    
    def add_button(self, path, x, y):
        button = QtWidgets.QPushButton()
        button.setStyleSheet("""background-color: lightgray;""")
        # button.setFixedSize(90,30)
        # text=self.extract_WellLabel
        button.setText(self.extract_WellLabel(path))
        button.clicked.connect(self.buttonClicked)
        self._lay.addWidget(button, x, y, alignment=QtCore.Qt.AlignLeft)

    @staticmethod
    def extract_WellLabel(path):
        basename = os.path.basename(path)
        well = os.path.splitext(basename)[0]
        return well

    def add_WellLabel(self, text, x, y):
        label = QtWidgets.QLabel()
        basename = os.path.basename(text)
        well = os.path.splitext(basename)[0]
        label.setText(well)
        label.setFont(QtGui.QFont("Courier New", 8, QtGui.QFont.Black))
        label.setStyleSheet("""
        background-color: white;
        color: blue;
        padding: 0px 2px 0px 2px;
    """)
        self._lay.addWidget(
            label, x, y, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)

    @staticmethod
    def add_Label_Timeline(layout, text, x, y):
        '''text must be a string containing the directory path'''
        label = QtWidgets.QLabel()
        tag = os.path.basename(text)  # .split('_')[0]
        label.setText(tag)
        label.setFont(QtGui.QFont("Helvetica", 12, QtGui.QFont.Black))
        label.setStyleSheet("""s
        background-color: white;
        color: black;
        padding: 5px 2px 0px 2px;
    """)
        layout.addWidget(
            label, x, y, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)

    @staticmethod
    def checkForChanges(InitialClassif, CurrentClass, InitialScore, CurrentScore, InitialNotes, CurrentNotes, well):
        '''Check for modifications '''
        # print(f'''
        #       InitialClassif: {InitialClassif}
        #       CurrentClass: {CurrentClass}
        #       InitialNotes: {InitialNotes}
        #       CurrentNotes: {CurrentNotes}
        #       well: {well}
        #       ''')
        if InitialClassif != CurrentClass:
            return True
        elif InitialNotes != CurrentNotes:
            return True
        elif InitialScore != CurrentScore:
            return True
        else:
            return False

    def dothings(self,well):
        '''do many things when button is clicked
           save previous notes, load notes, GUI update...'''

        #Save Notes previous well before loading New notes
        if self.previousWell is None:
            #            print("\n\npreviousWell ", self.previousWell)
            #            print("currentWell ", self.currentWell)
            self.previousWell = well
        else:
            if self.checkForChanges(self.InitialClassif,
                                    self.classifications[self.previousWell],
                                    self.InitialScore,
                                    self.scores[self.previousWell],
                                    self.InitialNotes,
                                    self.Notes_TextEdit.toPlainText(),
                                    self.previousWell) is True:
                self.SaveDATA(self.previousWell)
                
        # #Change color of button after click
        # self.ChangeButtonColor(
        #     self._lay, self.currentButtonIndex, state="active")
        
        #Load notes current wells
        self.LoadNotes(self.rootDir, self.date, well)
        self.InitialNotes = self.Notes_TextEdit.toPlainText()
        self.InitialClassif = self.classifications[well]
        self.InitialScore = self.scores[well]
        #change Color previous well to "checked"
        for widget_item in self.layout_widgets(self._lay):
            widget = widget_item.widget()
            ButtonIndex = self._lay.getItemPosition(
                self._lay.indexOf(widget))
            if widget.text() == self.previousWell and self.previousWell != well:
                self.ChangeButtonColor(
                    self._lay, ButtonIndex, state="checked")
            #Change color of button after click
            elif widget.text() == self.currentWell:
                self.ChangeButtonColor(
                    self._lay, ButtonIndex, state="active")
        #Update self.previousWell
        self.previousWell = well

        self.Set_ClassifButtonState(
            self.Scoring_Layout, self.classifications[well])
        self.Load_Timeline(self.rootDir, self.imageDir, well)
        self.labelVisuClassif.setText(self.classifications[well])
        self.labelVisuClassif.setStyleSheet("""background-color:%s;
                                            color:%s;"""
                                            % (ClassificationColor[self.classifications[well]]["background"],
                                               ClassificationColor[self.classifications[well]]["text"]))
        self.ImageViewer_1.setStyleSheet("""border: 2px solid %s;""" % (
            ClassificationColor[self.classifications[well]]["background"]))
        if self.currentScreen is not None:
            self.FindCrystCocktail(self.currentScreen,self.currentWell)
        if self.scores[self.currentWell] != None:
            self.comboBoxScore.setCurrentIndex(int(self.scores[self.currentWell]))
        else:
            self.comboBoxScore.setCurrentIndex(0)

    def buttonClicked(self):
        button = self.sender()
        self.idx = self._lay.indexOf(button)
        # getItemPosition(int index, int *row, int *column, int *rowSpan, int *columnSpan)
        location = self._lay.getItemPosition(self.idx)
        self.currentButtonIndex = location
        # print("Button", button, "at row/col", location[:2])

        well = button.text()
        self.currentWell = well

        path = self.buildWellImagePath(self.imageDir, well, self.well_images)
        self.open_image(path)
        #do many things
        self.dothings(well)
            
    # def LoadWellImage(self,path):
    #     ''' '''
    #     QtGui.QPixmapCache.clear()
    #     label=QLabel(self)
    #     pixmap=QPixmap(path)
    #     #resize pixmap to size of the QscrollArea Temporary?
    #     label.setPixmap(pixmap.scaled(860, 630, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation))
    #     self.ImageViewer.setWidget(label)

    def setScreen(self):
        self.currentScreen=self.comboBoxScreen.currentText()
        if self.comboBoxScreen.currentText()=='':
            self.currentScreen=None
        # print("Current Screen: ", self.currentScreen)
    
    def setScore(self, well):
        # self.scores[well]=self.comboBoxScore.currentText()
        self.scores[well]=self.comboBoxScore.currentIndex()
        if self.comboBoxScore.currentText()=='':
            self.scores[well]=None
        # print(f"self.scores[{well}]: ", self.scores[well])

    def copytoNotes(self,screen,well):
        if screen is None or well is None:
            return False
        cocktail=self.FindCrystCocktail(screen,well)
        if len(self.Notes_TextEdit.toPlainText().strip('\n'))==0:
            spacer=''
        else:
            spacer='\n'       
        self.Notes_TextEdit.insertPlainText(f"{spacer}Crystallization Mix:\n")
        for _i in cocktail[1:]:
            self.Notes_TextEdit.insertPlainText(_i+'\n')
        return True

    def open_image(self, path):
        self.ImageViewer.open_image(path)
        self.ImageViewer.view_current()

    @staticmethod
    def compare_most_recent(most_recent, date):
        if int(most_recent[0:4]) > int(date[0:4]):
            return most_recent
        elif int(most_recent[0:4]) < int(date[0:4]):
            return date
        # Reaching here means years are equal
        if int(most_recent[4:6]) > int(date[4:6]):
            return most_recent
        elif int(most_recent[4:6]) < int(date[4:6]):
            return date
        # Reaching here means months are equal
        if int(most_recent[6:8]) > int(date[6:8]):
            return most_recent
        elif int(most_recent[6:8]) < int(date[6:8]):
            return date
        return most_recent

    @staticmethod
    def check_datetime(fullpath):
        try:
            datetime.datetime.strptime(fullpath.split("/")[-1], '%Y%m%d')
            return True
        except:
            return False

    def check_previous_notes(self, path, current_date):
        path = path.joinpath("Image_Data")
        ensure_directory(path)
        if not Path(path.joinpath(current_date)).exists():
            print("> No previous notes found in directory:")
            print("> " + str(path))

        most_recent = "18000101"  # YYYYMMDD

        folders = [str(i) for i in Path(path).iterdir() if i.is_dir()]

        #clean list to avoid crash if unexpected directory names added by USERS
        folders[:] = [folder for folder in folders if self.check_datetime(folder) is True]

        for folder in folders:
            date = folder.split("/")[-1]
            if date == current_date:
                return
            most_recent = self.compare_most_recent(most_recent, date)
        newPath = path.joinpath(current_date)
        _f = ensure_directory(newPath)
        if _f is not None:  # if Permission issue
            self.handle_error(
                f"> {_f}\n\nYou must change the permissions and reload the directory to continue")
            return

        if len(os.listdir(path)) != 1:  # if not first time more than one folder is present
            path = path.joinpath(most_recent)
            filesToCopy = [file for file in path.iterdir() if not Path(
                file).is_dir()]  # skip folders like Miniatures
            for file in filesToCopy:
                copyfile(str(file), str(newPath.joinpath(file.name)))
            print(f"> Copied previous notes from: {most_recent}")
            print("> ")
            del filesToCopy

    def LoadNotes(self, path, date, well):
        data_file = Path(path).joinpath(
            "Image_Data", date, "%s_data.txt" % well)
        self.Notes_TextEdit.clear()
        if Path(data_file).exists():
            with open(data_file, "r") as f:
                content = f.readlines()
                notes = content[10:]
                for i in notes:
                    self.Notes_TextEdit.insertPlainText(i)

    def SaveDATA(self, well):
        '''Save Notes in QPlainTextEdit and more'''
        text = self.Notes_TextEdit.toPlainText()
        if len(text) != 0:
            self.WellHasNotes[well] = True
        elif len(text) == 0 and self.WellHasNotes[well] == True:
            self.WellHasNotes[well] = False
        path = Path(self.rootDir).joinpath(
            "Image_Data", self.date, "%s_data.txt" % well)
        Notes = []
        Notes.append("Project Code:%s:\n" % self.project)
        Notes.append("Target Name:%s:\n" % self.target)
        Notes.append("Plate Name:%s:\n" % self.plate)
        Notes.append("Date:%s:\n" % self.date)
        Notes.append("\n")
        Notes.append("Classification:%s:\n" % self.classifications[well])
        Notes.append("Human Score:%s:\n" % self.scores[well])
        Notes.append("\n")
        Notes.append("Notes:\n")
        Notes.append("\n")
        Notes.append(text)

        print("Saving data to %s" % path)
        self.label_LastSaved.setText(f"### Data for {well} saved ###")
        try:
            with open(path, 'w') as f:
                for i in Notes:
                    f.write(i)
        except Exception as e:
            self.handle_error(str(e))

    def CheckClassificationAndNotes(self, path, date, well):
        '''create a dir well:classif when calling func AddtoClassificationDict
        and create a dict WellHasNotes True or False'''
        data_file = Path(path).joinpath(
            "Image_Data", date, "%s_data.txt" % well)
        if Path(data_file).exists():
            with open(data_file, "r") as f:
                content = f.readlines()
                classifications = content[5].split(":")
                score=content[6].split(":")
                if score==['\n']:
                    human_score=None
                elif score[1] =='None':
                    human_score=None
                else:
                    human_score=score[1]
                self.AddtoClassificationDict(well, classifications[1], human_score)
                if len(content[10:]) != 0:
                    self.WellHasNotes[well] = True
                else:
                    self.WellHasNotes[well] = False
        else:
            self.AddtoClassificationDict(well, "Unknown", None)
            self.WellHasNotes[well] = False

    def AddtoClassificationDict(self, well, classification, score):
        '''Create a dictionnary with well and classification'''
        self.classifications[well] = classification
        self.scores[well] = score

    def SetAllVisible(self):
        '''Specific to OSX Catalina due to crash when opening new dir
        (error in self.radioButton_All.setChecked(True) more
         specifically in function FilterClassification)'''
        self.VisiblesIdx.clear()
        for widget_item in self.layout_widgets(self._lay):
            widget = widget_item.widget()
            self.VisiblesIdx.append(self._lay.indexOf(widget))

    def FilterClassification(self, layout, classification):
        self.VisiblesIdx.clear()  # Clear before modification
        for widget_item in self.layout_widgets(layout):
            widget = widget_item.widget()
            if self.classifications[widget.text()] == classification:
                widget.setVisible(True)
                self.VisiblesIdx.append(layout.indexOf(widget))
            elif classification == "All":
                widget.setVisible(True)
                self.VisiblesIdx.append(layout.indexOf(widget))
            else:
                widget.setVisible(False)
#            print("well ",widget.text(), "dico Classif ", self.classifications[widget.text()])
        # print("Visibles", self.VisiblesIdx)

    def FilterSubwell(self, layout, subwell):
        self.VisiblesIdx.clear()  # Clear before modification
        for widget_item in self.layout_widgets(layout):
            widget = widget_item.widget()
            if widget.text()[-1] == subwell:
                widget.setVisible(True)
                self.VisiblesIdx.append(layout.indexOf(widget))
            else:
                widget.setVisible(False)

    def FilterNotes(self, layout):
        self.VisiblesIdx.clear()  # Clear before modification
        for widget_item in self.layout_widgets(layout):
            widget = widget_item.widget()
            if self.WellHasNotes[widget.text()] == True:
                widget.setVisible(True)
                self.VisiblesIdx.append(layout.indexOf(widget))
            else:
                widget.setVisible(False)

    @staticmethod
    def layout_widgets(layout):
        return (layout.itemAt(i) for i in range(layout.count()))

    @staticmethod
    def ClearLayout(layout):
        '''Code commented was crashing in specific cases
        solution found at https://www.thetopsites.net/article/51691104.shtml'''
        # for widget_item in self.layout_widgets(layout):
        #         widget_item.widget().deleteLater()
        for i in reversed(range(layout.count())):
            widgetToRemove = layout.itemAt(i).widget()
            layout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)

    def SetDropClassif(self, radioButton, well):
        if radioButton.isChecked() is True:
            if radioButton.text() == "Phase Separation":
                self.classifications[well] = "PhaseSep"
            else:
                self.classifications[well] = radioButton.text()

    def Set_ClassifButtonState(self, layout, classification):
        widgetlist = []
        #Extract non Qlabel widgets
        for widget_item in self.layout_widgets(layout):
            widget = widget_item.widget()
            # if isinstance(widget, QtWidgets.QLabel) is False and isinstance(widget, QtWidgets.QComboBox) is False:
            #     widgetlist.append(widget)
            if isinstance(widget, QtWidgets.QRadioButton) is True:
                widgetlist.append(widget)
        #Reset Activation State first
        for widget in widgetlist:
            if widget.isChecked() is True:
                widget.setAutoExclusive(False)
                widget.setChecked(False)
            widget.setAutoExclusive(True)
        #Then do the job
        for widget in widgetlist:
            # widget = widget_item.widget()
            if widget.text() == classification:
                widget.setChecked(True)
            elif classification == "Unknown":
                widget.setChecked(False)
            elif classification == "PhaseSep":
                if widget.text() == "Phase Separation":
                    widget.setChecked(True)
                else:
                    widget.setChecked(False)
            else:
                widget.setChecked(False)
        del widgetlist

    def Load_Timeline(self, rootdirectory, imagedir, well):
        rootdirectory = Path(rootdirectory)
        other_dates = []
        for i in os.listdir(rootdirectory):
            if i != "Image_Data":
                path = Path(rootdirectory).joinpath(i)
                if os.path.isdir(path):
                    other_dates.append(path)
        other_dates.sort()

        self.ClearLayout(self._timlay)

        for date in other_dates:
            if imagedir.split("/")[-1] == self.rawimages:
                path = Path(date).joinpath(self.rawimages)
            else:
                path = Path(date)
            name = self.buildWellImagePath(str(path), well, self.well_images)
            if Path(name).exists():
                button = QtWidgets.QPushButton()
                icon = QtGui.QIcon(name)
                button.setIcon(icon)
                button.setIconSize(QtCore.QSize(250, 188))
                button.setFixedWidth(260)
                tag = os.path.basename(date)  # .split('_')[0]
                # button.setText(tag)
                button.clicked.connect(lambda: self.Open_Timeline(well))
                self._timlay.addWidget(button, 0, other_dates.index(date))
                self.add_Label_Timeline(
                    self._timlay, tag, 1, other_dates.index(date))
        self.label_CurrentWell.setText(well)

    def Open_Timeline(self, well):
        '''open image from timeline and display in main window'''
        button = self.sender()
        idx = self._timlay.indexOf(button)
        location = self._timlay.getItemPosition(idx)
        row, col = location[0], location[1]
        item = self._timlay.itemAtPosition(row+1, col)
        widget = item.widget()
        date = widget.text()
        path = Path(self.buildWellImagePath(
            self.imageDir, well, self.well_images))
        parts = list(path.parts)
        imagedir = self.imageDir.split("/")
        if imagedir[-1] == self.rawimages or imagedir[-1] == "cropped":
            parts[-3] = date
        else:
            parts[-2] = date
        path = str(Path(*parts))
        # self.open_image(path)
        if self.TimelineInspector is None:
            self.TimelineInspector = ExternalViewer.Window()
        self.TimelineInspector.open_image(path)
        if self.prepdate != "None":
            d0 = datetime.date(int(self.prepdate[0:4]), int(
                self.prepdate[4:6]), int(self.prepdate[6:]))
            d1 = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8]))
            delta = d1 - d0
            self.TimelineInspector.setWindowTitle(
                "Timeline Inspector Well: %s Date: %s (%s day(s))" % (well, date[0:8], delta.days))
        else:
            self.TimelineInspector.setWindowTitle(
                "Timeline Inspector Well: %s Date: %s " % (well, date[0:8]))
        self.TimelineInspector.show()
        self.TimelineInspector.activateWindow()
        self.TimelineInspector.raise_()

        #Don't know if it is useful in case of long term use
        del imagedir, widget, date, path, parts, row, col, item, idx, location

    @staticmethod
    def ActivateButton(layout, idx):
        '''Activate a button in a QgridLayout,
        idx is a tuple of the current Button'''
        if idx is None:
            return
        row = idx[0]
        col = idx[1]
        # item = layout.itemAtPosition(row,col)
        try:
            item = layout.itemAtPosition(row, col)
            widget = item.widget()
            widget.click()
        except ValueError:
            return

    def ChangeButtonColor(self, layout, idx, state="active"):
        '''Change color of the button'''
        if idx is None:
            return
        row = idx[0]
        col = idx[1]
        try:
            item = layout.itemAtPosition(row, col)
            widget = item.widget()
        except:
            self.handle_error("Navigation error")

        if state == "active":
            widget.setStyleSheet("""color: black;background-color: cyan;""")
        elif state == "checked":
            widget.setStyleSheet("""color: black;background-color: blue;""")

    def keyPressEvent(self, event):
        '''iterate over a grid using shortcuts and assign quickly classification'''
        if self.currentButtonIndex is None:
            return
        location = self.currentButtonIndex
        currentrow = location[0]
        currentcol = location[1]

        shortcut = pref.Shortcut()

        if event.key() == shortcut.MoveLeft:
            try:
                NewlocationIdx = list(
                    filter(lambda i: i < self.idx, reversed(self.VisiblesIdx)))[0]
                Newlocation = self._lay.getItemPosition(NewlocationIdx)
                self.ActivateButton(self._lay, Newlocation)
            except:
                self.handle_error("Already at first well")

        if event.key() == shortcut.MoveRight:
            # print("self.idx :", self.idx)
            try:
                NewlocationIdx = list(
                    filter(lambda i: i > self.idx, self.VisiblesIdx))[0]
                Newlocation = self._lay.getItemPosition(NewlocationIdx)
                self.ActivateButton(self._lay, Newlocation)
            except:
                self.handle_error("Already at last well")

        if event.key() == shortcut.MoveUp:
            Newlocation = (currentrow-1, currentcol, location[2], location[3])
            try:
                self.ActivateButton(self._lay, Newlocation)
            except:
                self.handle_error("Already at first row")

        if event.key() == shortcut.MoveDown:
            Newlocation = (currentrow+1, currentcol, location[2], location[3])
            try:
                self.ActivateButton(self._lay, Newlocation)
            except:
                self.handle_error("Already at last row")

        if event.key() == shortcut.Clear:
            self.radioButton_ScoreClear.setChecked(True)
        elif event.key() == shortcut.Crystal:
            self.radioButton_ScoreCrystal.setChecked(True)
        elif event.key() == shortcut.Precipitate:
            self.radioButton_ScorePrecipitate.setChecked(True)
        elif event.key() == shortcut.PhaseSep:
            self.radioButton_ScorePhaseSep.setChecked(True)
        elif event.key() == shortcut.Other:
            self.radioButton_ScoreOther.setChecked(True)

    def Calculate_Statistics(self):
        '''Calculate statistics for plate'''
        from decimal import Decimal, ROUND_HALF_UP

        Count_subwell_a = {"Clear": 0, "Precipitate": 0,
                           "Crystal": 0, "PhaseSep": 0, "Other": 0, "Unknown": 0}
        Count_subwell_b = {"Clear": 0, "Precipitate": 0,
                           "Crystal": 0, "PhaseSep": 0, "Other": 0, "Unknown": 0}
        Count_subwell_c = {"Clear": 0, "Precipitate": 0,
                           "Crystal": 0, "PhaseSep": 0, "Other": 0, "Unknown": 0}
        Count_nosubwell = {"Clear": 0, "Precipitate": 0,
                           "Crystal": 0, "PhaseSep": 0, "Other": 0, "Unknown": 0}

        for well, classification in self.classifications.items():
            if "a" in well:
                Count_subwell_a[classification] += 1
            elif "b" in well:
                Count_subwell_b[classification] += 1
            elif "c" in well:
                Count_subwell_c[classification] += 1
            else:
                Count_nosubwell[classification] += 1

        _list = [Count_subwell_a, Count_subwell_b,
                 Count_subwell_c, Count_nosubwell]
        totals = []
        for i in _list:
            total = 0  # reset counter
            for classification, count in i.items():
                total += count
            totals.append(total)

        for i in _list:
            for classification, count in i.items():
                try:
                    # i[classification]=round(count/totals[_list.index(i)]*100,2)
                    value = Decimal(count/totals[_list.index(i)]*100.)
                    i[classification] = Decimal(value.quantize(
                        Decimal('.01'), rounding=ROUND_HALF_UP))
                except ValueError:
                    i[classification] = 0
                except ZeroDivisionError:
                    i[classification] = 0

        return _list

    def autoAnnotation(self):
        '''Do automated classification using MARCO'''
        from Automated_Marco import Predictor

        Unsupported_Ext = [".tif", ".tiff", ".TIFF"]

        if len(self.files) == 0:
            self.handle_error(
                "Please choose a directory containing the images first!!!")
            return

        ext = os.path.splitext(os.path.basename(self.files[0]))[1]
        if ext in Unsupported_Ext:
            self.handle_error("Image type ""%s"" unsupported for automated annotation"
                              % ext)
            return

        #Reset self.classifications NEED TO INFORM USER
        info = QMessageBox(self)
        info.setWindowTitle("Warning!")
        info.setText("This will erase any previous classification, score and notes")
        info.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = info.exec_()

        if retval == QtWidgets.QMessageBox.Cancel:
            return

        if self.Predicter is None:
            self.MARCO = Predictor()
            if self.MARCO.loadtensorflow() is True:
                self.Predicter = self.MARCO.createpredicter()
            else:
                self.handle_error(
                    "TensorFlow version %s not supported" % self.MARCO.tfversion)
                self.EnableDisableautoMARCO(False)
                return

        self.classifications.clear()
        self.scores.clear()
        self.Notes_TextEdit.clear()  # if not emptied, note is given to all wells

        logdir = Path(self.rootDir).joinpath("Image_Data", self.date)
        self.MARCO.predict(self.files, self.classifications,
                           logdir, self.Predicter)

        for well, _classif in self.classifications.items():
            self.scores[well]= None #as scores were cleared need to put None
            self.SaveDATA(well)

    def annotateCurrent(self):
        '''Single image classification using MARCO'''
        from Automated_Marco import Predictor
        Unsupported_Ext = [".tif", ".tiff", ".TIFF"]

        if self.currentWell is None:
            self.handle_error("Please choose a well first")
            return

        ext = os.path.splitext(os.path.basename(self.files[0]))[1]
        if ext in Unsupported_Ext:
            self.handle_error("Image type ""%s"" unsupported for automated annotation"
                              % ext)
            return

        if self.Predicter is None:
            self.MARCO = Predictor()
            if self.MARCO.loadtensorflow() is True:
                self.Predicter = self.MARCO.createpredicter()
            else:
                self.handle_error(
                    "TensorFlow version %s not supported" % self.MARCO.tfversion)
                self.EnableDisableautoMARCO(False)
                return

        imgpath = self.buildWellImagePath(
            self.imageDir, self.currentWell, self.well_images)
        result = self.MARCO.single_predict(str(imgpath), self.Predicter)

        info = QMessageBox(self)
        info.setWindowTitle("autoMARCO prediction results")
        info.setText(f'''classification: {result[0]} | probability: {round(float(result[1]),3)}
Threshold set in preferences for accepting prediction is: {pref.autoMARCO_threshold}

Click "OK" to accept prediction, "Cancel" to ignore''')
        info.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = info.exec_()

        if retval == QtWidgets.QMessageBox.Ok:
            self.classifications[self.currentWell] = result[0]
            self.Set_ClassifButtonState(
                self.Scoring_Layout, self.classifications[self.currentWell])
        else:
            return

        del result

    @staticmethod
    def on_exit():
        '''things to do before exiting'''
#        self.SaveDATA(self.currentWell)
        app.closeAllWindows()
        Citation()

    def take_plate_screenshot(self, subwell):
        if len(self.classifications) == 0:
            self.handle_error("No data yet!!!")
            return

        if subwell == "":
            title = "PlateOverview_%s_%s_%snosubwell" % (
                self.plate, self.date, subwell)
        else:
            title = "PlateOverview_%s_%s_subwell_%s" % (
                self.plate, self.date, subwell)

        if subwell in self.PLATE_window:
            # print("Window is VISIBLE? :",self.PLATE_window[subwell].isVisible())
            # Update Classif if changes were made after table creation
            self.PLATE_window[subwell].UpdateBorder(
                self.files, self.classifications)
            self.PLATE_window[subwell].show()
            # Ensure window is on foreground
            self.PLATE_window[subwell].activateWindow()
            #wait some time to before screenshot
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(500, loop.quit)
            loop.exec_()
            self.take_screenshot(self.PLATE_window[subwell], title)
        else:
            self.show_Plates(subwell)
            # print("Window is VISIBLE? :",self.PLATE_window[subwell].isVisible())
            #wait some time to generate the window
            try:
                self.PLATE_window[subwell].isVisible() is True
            except:
                time.sleep(1)
            # Ensure window is on foreground
            self.PLATE_window[subwell].activateWindow()
            #wait some time to before screenshot
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(500, loop.quit)
            loop.exec_()
            self.take_screenshot(self.PLATE_window[subwell], title)

    def take_screenshot(self, window, title):
        #If no data prevent crashing
        if len(self.classifications) == 0:
            self.handle_error("No data yet!!!")
            return False

        filename = Path(self.rootDir).joinpath("Image_Data", "%s.jpg" % title)
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow(window.winId())
        screenshot.save(str(filename), 'jpg')
        message = "File saved to:\n %s" % filename
        self.informationDialog(message)

    def DeleteFolder(self, datepath, folder):
        '''Delete specific Folder at location datepath to save disk space, platepath and folder are string'''
        import shutil

        try:
            path = Path(datepath).joinpath(folder)
        except:
            self.handle_error("Open a directory containing images first!!!")
            return

        #WARN USER
        info = QMessageBox(self)
        info.setWindowTitle("Warning!")
        info.setText(
            f'''This will erase the directory: "{path}" and its content. \nThis action cannot be undone!!!''')
        info.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = info.exec_()

        if retval == QtWidgets.QMessageBox.Cancel:
            return
        try:
            os.path.isdir(path)
            shutil.rmtree(path)
        except:
            self.handle_error(f"WARNING: {path} not found")
            return

#BELOW CODE RELATED TO PROJECT TAB

    def resetProject(self):
        '''Reset Table in Project Tab'''
        # self.tableViewProject.clearContents()
        self.tableViewProject.setRowCount(0)
        self.comboBoxProject.setCurrentIndex(0)
        self.imageP=None
        self.ProjectInspector.scene.clear()

    # def clearTableWidget(self, TableWidget, col=4):
    #     '''clear all widget in a Table col'''
    #     for i in range(TableWidget.rowCount()):
    #         TableWidget.removeCellWidget(i,col)

    def listTargetsTable(self, TableWidget, col=0):
        '''clear all widget in a Table col'''
        targets=[]
        for i in range(TableWidget.rowCount()):
            target=TableWidget.item(i,col).text()
            if target not in targets:
                targets.append(target)
        return targets

    def filterTable(self, key, TableWidget, col=0):
        for i in range(TableWidget.rowCount()):
            if key==TableWidget.item(i,col).text():
                TableWidget.showRow(i)
            elif key=="":
                TableWidget.showRow(i)
            else:
                TableWidget.hideRow(i)
        
    def searchClassifProject(self):
        searchC=self.comboBoxProject.currentText()
        if self.comboBoxProject.currentText()=='':
            searchC=None
            return
        _path=Path(*self.rootDir.parts[:self.rootDir.parts.index(self.project)+1])
        fname='All_'+searchC+'.csv'
        self.open_Summary(_path, fname)
        self.show_project_overview()

    def cellClickedTable(self):
        row = self.tableViewProject.currentRow()
        # col = self.tableViewProject.currentColumn()
        path=self.tableViewProject.item(row,3).text()
        # self.open_imageP(path)
        self.ProjectInspector.open_image(path)
        self.tableViewProject.item(row,4).setBackground(QtGui.QColor(153, 153, 255))

    def loadcsvtoTable(self, path):
            with open(path, newline='') as csv_file:
                self.csvreader = csv.reader(csv_file, delimiter=',', quotechar='"')
                next(self.csvreader) #skip header
                self.tableViewProject.setRowCount(0); self.tableViewProject.setColumnCount(5)
                for row_data in self.csvreader:
                    row = self.tableViewProject.rowCount()
                    self.tableViewProject.insertRow(row)
                    if len(row_data) > 5:
                        self.tableViewProject.setColumnCount(len(row_data))
                    for column, stuff in enumerate(row_data):
                        # print("STUFF: ", stuff)
                        item = QTableWidgetItem(stuff)
                        self.tableViewProject.setItem(row, column, item)
            #Render Table not editable
            self.tableViewProject.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            del self.csvreader
            
    def open_Summary(self, path, filename):
        '''open a csv file, create a Table and returns True or False'''
        _path=Path(path).joinpath(filename)
        prog=Path(self.app_path).joinpath("tools", "Search_classif_Project.py")
        _dir=Path(*self.rootDir.parts[:self.rootDir.parts.index(self.project)+1])
        
        _check=Path(_path).is_file()
        if _check is True:
            info = QMessageBox(self)
            info.setWindowTitle("Warning File Found")
            info.setText(f'''File:
{_path}

Do you want to re-run the analysis?''')
            info.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = info.exec_()
            if retval == QtWidgets.QMessageBox.Cancel:
                self.loadcsvtoTable(_path)
            else:
                subprocess.run([sys.executable, prog,"--unique", 
                                "--class", self.comboBoxProject.currentText(),
                                _dir])
                self.loadcsvtoTable(_path)
        else:
                subprocess.run([sys.executable, prog,"--unique", 
                                "--class", self.comboBoxProject.currentText(),
                                _dir])
                self.loadcsvtoTable(_path)
        self.targets=self.listTargetsTable(self.tableViewProject)
        
        #Populate combobox
        self.comboBoxTargetFilter.clear()
        self.comboBoxTargetFilter.addItem("")
        for _i in self.targets:
            self.comboBoxTargetFilter.addItem(_i)
        return _check

    def show_project_overview(self):
        self.tableViewProject.setColumnHidden(3,True)
        header = self.tableViewProject.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    MainWindow = ViewerModule()
    sys.exit(app.exec_())
