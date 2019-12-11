#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 13:57:18 2019

@author: ludovic
"""

from gui import Ui_MainWindow
import os
import re
import math
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QFont, QColor, QKeySequence
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons
from PyQt5.QtWidgets import (QLabel, QTableWidgetItem, QFileDialog,
    QMessageBox, QGridLayout,QStyleFactory)

from utils import ensure_directory
from shutil import copyfile
import pdf_writer 
from HeatMap import Ui_Dialog
import Shortcuts
import StatisticsDialog

__version__ = "1.0.0a"
__author__ = "Ludovic Pecqueur (ludovic.pecqueur \at college-de-france.fr)"
__date__ = "10-12-2019"
__license__ = "New BSD http://www.opensource.org/licenses/bsd-license.php"


def Citation():
    print('''
Program inspired from the original program at 
https://github.com/dakota0064/Fluorescent_Robotic_Imager
written by Dakota Handzlik

Program written for Qt5 by L.P.
licence: %s
'''%__license__)

class ViewerModule(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ViewerModule, self).__init__(parent)
        self.ui=Ui_MainWindow()
        self.setupUi(self)
        self.setWindowTitle("LCPB AMi Image Analysis version %s"%__version__)
        #Setup a progressBar not placed in Designer
#        self.progressBar = QProgressBar(self)
        self._nsre = re.compile('([0-9]+)') #used to sort alphanumerics
        
        content_widget = QtWidgets.QWidget()
        self.scrollAreaPlate.setWidget(content_widget)
        self._lay = QGridLayout(content_widget)
        
        timeline_widget = QtWidgets.QWidget()
        self.scrollArea_Timeline.setWidget(timeline_widget)
        self._timlay = QGridLayout(timeline_widget)
        
        self.files = []
        self.well_images = []
        self.directory = str
        self.rootDir = str
        self.imageDir = str
        self.project = str
        self.target = str
        self.plate = str
        self.date = str
        self.prepdate = str
        self.classifications = {}
        self.previousWell = None
        self.currentWell = None
        self.currentButtonIndex= None

        #If using the QGraphics view, use open_image
        #If not comment the next five lines and use
        #function LoadWellImage
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.view.wheelEvent = self.wheel_event
        self.ImageViewer.setWidget(self.view)
                
        self.initUI()


    def show_HeatMap(self):
        ''' Create window and map results on a grid'''
        self.heatmap_window = HeatMapGrid()
        self.heatmap_window.well_images=self.well_images
        self.heatmap_window.classifications=self.classifications
        self.heatmap_window.show()


    def show_Statistics(self):
        '''Calculate statistics on the plate'''
        #Check data before going further
        if len(self.classifications)==0:
            self.handle_error("No data yet!!!")
            return
        
        self.StatisticsWindow=QtWidgets.QDialog()
        ui=StatisticsDialog.Ui_Dialog()
        ui.setupUi(self.StatisticsWindow)
        results=self.Calculate_Statistics()
        positions = [(i,j) for i in range(6) for j in range(4)]
        # print("positions ", positions)
        
        for pos in positions:
            if pos[0]==0:
                value=results[pos[1]]['Clear']
            elif pos[0]==1:
                value=results[pos[1]]['Precipitate']
            elif pos[0]==2:
                value=results[pos[1]]['Crystal']
            elif pos[0]==3:
                value=results[pos[1]]['PhaseSep']
            elif pos[0]==4:
                value=results[pos[1]]['Other']
            else:
                value=results[pos[1]]['Unknown']
                
            ui.StatisticsTable.setItem(pos[0],pos[1], QTableWidgetItem(str(value)))
        
        self.StatisticsWindow.show()
        
        
        
    def initUI(self):

        self.MaxCol=6
        
        #Shortcut definitions
        
        self.exportPDFshortcut=QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+E"), self)
        self.exportPDFshortcut.activated.connect(self.export_pdf)
        
        #Setup Menu
        self.openFile.triggered.connect(self.openFileNameDialog)
        self.openDir.triggered.connect(self.openDirDialog)
        
        self.actionDisplay_Heat_Map.triggered.connect(self.show_HeatMap)
        self.actionExport_to_PDF.triggered.connect(self.export_pdf)
        self.actionQuit_2.triggered.connect(self.close)
        
        self.actionCalculate_Statistics.triggered.connect(self.show_Statistics)
        self.actionShortcuts.triggered.connect(self.ShowShortcuts)
        self.actionAbout.triggered.connect(self.ShowAbout)
        
        
        self.label_ProjectDetails.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Black))
        
        self.ImageViewer.setStyleSheet("""background-color:transparent;border: 1px solid black;""")
 
        #Setup Filtering Options
        self.radioButton_All.toggled.connect(lambda:self.FilterClassification(self._lay,"All"))
        self.radioButton_Crystal.toggled.connect(lambda:self.FilterClassification(self._lay,"Crystal"))
        self.radioButton_Clear.toggled.connect(lambda:self.FilterClassification(self._lay,"Clear"))
        self.radioButton_Other.toggled.connect(lambda:self.FilterClassification(self._lay,"Other"))
        self.radioButton_Precipitate.toggled.connect(lambda:self.FilterClassification(self._lay,"Precipitate"))
        self.radioButton_PhaseSep.toggled.connect(lambda:self.FilterClassification(self._lay,"PhaseSep"))
        self.radioButton_Unsorted.toggled.connect(lambda:self.FilterClassification(self._lay,"Unknown"))
        
        
        #Change Some Styles in Scoring Section
        self.label_2.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Black))
        self.label_4.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Black))
        self.label_Timeline.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Black))
        self.label_CurrentWell.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Black))
        self.label_CurrentWell.setStyleSheet("""color: blue;""")

        self.radioButton_ScoreClear.setStyleSheet("""color: black;""")
        self.radioButton_ScorePrecipitate.setStyleSheet("""color: red;""")
        self.radioButton_ScoreCrystal.setStyleSheet("""color: green;""")                                            
        self.radioButton_ScorePhaseSep.setStyleSheet("""color: orange;""")
        self.radioButton_ScoreOther.setStyleSheet("""color: magenta;""")

        #Listen Scoring RadioButtons
        self.radioButton_ScoreClear.toggled.connect(lambda:self.ScoreDrop(self.radioButton_ScoreClear, self.currentWell))
        self.radioButton_ScorePrecipitate.toggled.connect(lambda:self.ScoreDrop(self.radioButton_ScorePrecipitate, self.currentWell))
        self.radioButton_ScoreCrystal.toggled.connect(lambda:self.ScoreDrop(self.radioButton_ScoreCrystal, self.currentWell))
        self.radioButton_ScorePhaseSep.toggled.connect(lambda:self.ScoreDrop(self.radioButton_ScorePhaseSep, self.currentWell))
        self.radioButton_ScoreOther.toggled.connect(lambda:self.ScoreDrop(self.radioButton_ScoreOther, self.currentWell))

        #Listen Display Heat Map and export to pdf buttons
        self.pushButton_DisplayHeatMap.clicked.connect(self.show_HeatMap)
        self.pushButton_ExportToPDF.clicked.connect(self.export_pdf)
        
        self.show()
 
    
    def ShowShortcuts(self):
        shortcut=Shortcuts.Shortcut()
        BoxShortCuts=QMessageBox()
        text='''
    Well navigation shortcuts:
    MoveUp= %s
    MoveDown= %s
    MoveLeft= %s
    MoveRight= %s
    
    Scoring shortcuts:
    Clear= %s
    Crystal= %s
    Precipitate= %s
    Phase Separation= %s
    Other= %s
        '''%(QKeySequence(shortcut.MoveUp).toString(),
        QKeySequence(shortcut.MoveDown).toString(),
        QKeySequence(shortcut.MoveLeft).toString(),
        QKeySequence(shortcut.MoveRight).toString(),
        QKeySequence(shortcut.Clear).toString(),
        QKeySequence(shortcut.Crystal).toString(),
        QKeySequence(shortcut.Precipitate).toString(),
        QKeySequence(shortcut.PhaseSep).toString(),
        QKeySequence(shortcut.Other).toString())
        BoxShortCuts.information(self,"Shortcuts", text)
        del shortcut


    def ShowAbout(self):
        about=QMessageBox()
        text='''
 Program written For Python 3 and PyQt5
 written by Ludovic Pecqueur
 College de France
 Released under licence:
 %s    
    '''%__license__
        about.information(self,"About", text)    
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open File", "","All Files (*);;Image Files (*.tiff *.tif *.jpg *.jpeg)", options=options)
        if fileName:
            print(fileName)
        if fileName:
            self.open_image(fileName)

    def Initialise(self):
        '''reset file list when changing folder and reset layout grid'''
        self.classifications.clear()
        self.previousWell = None
        self.currentWell = None
        self.currentButtonIndex= None
        self.files.clear()
        self.well_images.clear()
        self.ClearLayout(self._lay)


    def openDirDialog(self):
        Ext=[".tif",".tiff",".TIFF",".jpg", ".jpeg",".JPG",".JPEG"]
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = str(QFileDialog.getExistingDirectory(self,"Directory containing Images"))
        self.Initialise()
        if directory:
            print(directory)
            self.imageDir=os.path.realpath(directory)
            #Initialise Project Details 
            self.Directory(os.path.realpath(directory))
            print("Plate root directory : ", self.rootDir)
            self.ProjectCode.setText(self.project)
            self.PrepDate.setText(str(self.prepdate))
            self.ImageDate.setText(self.date)
            self.TargetName.setText(self.target)
            self.PlateName.setText(self.plate)

        if directory:
            self.files_it = iter([os.path.join(directory, file) for file in os.listdir(directory) if os.path.splitext(file)[1] in Ext])
            for file in os.listdir(directory):
                if os.path.splitext(file)[1] in Ext:
                    self.files.append(os.path.join(directory, file))
                    self.well_images.append(os.path.basename(file))
        if len(self.files)!=0:
            #sorting the output of os.listdir after filtering
            self.files.sort(key=self.natural_sort_key)
            self.well_images.sort(key=self.natural_sort_key)
            self._timer = QtCore.QTimer(self, interval=1)
            self._timer.timeout.connect(self.on_timeout)
            self._timer.start()
            self.check_previous_notes(self.rootDir, self.date)
#            QtGui.QPixmapCache.clear()
        else:
            self.handle_error("No Image File Found in directory")

        for i in self.well_images:
            well=os.path.splitext(i)[0]
            self.ReadClassification(self.rootDir, self.date, well)


    def export_pdf(self):
        '''export to PDF a report for current well'''
        if self.previousWell is None:
            self.handle_error("No well selected")
            return
        
        rootDir=self.rootDir
        imgDir=self.imageDir
        img_list=self.well_images
        values = []
        name = ""
        well=self.currentWell

        values.append(name)

        imgpath=self.buildWellImagePath(imgDir, well, img_list)
    #        path = directory + "/" + well
        pdfpath=Path(rootDir).joinpath("Image_Data", "%s_%s.pdf"%(well,self.date))
    #        pdfpath=pdfpath + "/" + filename
        values.append(imgpath)
    
        values.append(self.project)
        values.append(self.target)
        values.append(self.plate)
        values.append(self.date)
        text=self.Notes_TextEdit.toPlainText()
        values.append(text)
        values.append(pdfpath)
    #            print(values)
        pdf_writer.create_pdf(values)
        print("Report for well %s saved to %s"%(well, pdfpath))


    def Directory(self, path):
#        print("ClassPath ", path.split("/"))
        directory = path.split("/")
        if directory[-1]=="rawimages":
            self.rootDir = "/".join(directory[:-2])
            self.project=directory[-4]
            self.target=directory[-4]
            self.plate=directory[-3]
            self.date=directory[-2].split("_")[0]
            prep_date_path = "/".join(directory[:-2]) + "/"+ "prep_date.txt"
        else:
            self.rootDir = "/".join(directory[:-1])
            self.project=str(directory[-3])
            self.target=directory[-3]
            self.plate=directory[-2]
            self.date=directory[-1].split("_")[0]
            prep_date_path = "/".join(directory[:-1]) + "/"+ "prep_date.txt"
        
        if Path(prep_date_path).exists():
            file = open(prep_date_path)
            contents = file.read().strip("\n")
            self.prepdate=contents


    def buildWellImagePath(self,directory, well, wellimage_list):
        '''search for a substring, returns a list, use first element
        directory is a string'''
        search = list(filter(lambda i: well in i, wellimage_list))
        path=directory+ "/" + search[0]
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
    
    
    def natural_sort_key(self, s):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split(self._nsre, s)] 

        
    def GenerateGrid(self, filelist):
        MaxCol=self.MaxCol
        MaxRow=math.ceil(len(filelist)/MaxCol)+1
#        print("Nb of Files", len(filelist))
#        print("MaxCol ", MaxCol, "MaxRow ", MaxRow)
        positions = [(i,j) for i in range(MaxRow) for j in range(MaxCol)]
        return positions


    def on_timeout(self):
        positions=self.GenerateGrid(self.files)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(len(self.files))
        vmin,vmax=0, len(self.files)
        count=0
        for position, name in zip(positions, self.files):
#            print(position, name)
            try:
                file = next(self.files_it)
#                pixmap = QtGui.QPixmap(name)
#                self.add_pixmap(pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation), position[0],position[1])
#                self.add_WellLabel(name, position[0],position[1])
                self.add_button(name, position[0],position[1])
                self.progressBar.setValue(count+1)
                count+=1
            except StopIteration:
                self._timer.stop()
                self.progressBar.setValue(vmax)


    def add_pixmap(self, layout, pixmap, x, y):
        if not pixmap.isNull():
            label = QtWidgets.QLabel(pixmap=pixmap)
            layout.addWidget(label, x, y, alignment=QtCore.Qt.AlignCenter)


    def add_Timeline_pixmap(self, layout, pixmap, x, y):
        if not pixmap.isNull():
            label = QtWidgets.QLabel(pixmap=pixmap)
            layout.addWidget(label, x, y, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)


    def add_button(self, path, x, y):
            button = QtWidgets.QPushButton()
            text=self.extract_WellLabel
            button.setText(self.extract_WellLabel(path))
            button.clicked.connect(self.buttonClicked)
            self._lay.addWidget(button, x, y, alignment=QtCore.Qt.AlignLeft)


    def extract_WellLabel(self, path):
        basename=os.path.basename(path)
        well=os.path.splitext(basename)[0]
        return well

    
    def add_WellLabel(self, text, x, y):
            label = QtWidgets.QLabel()
            basename=os.path.basename(text)
            well=os.path.splitext(basename)[0]
            label.setText(well)
            label.setFont(QtGui.QFont("Courier New", 8, QtGui.QFont.Black))
            label.setStyleSheet("""
            background-color: white;
            color: blue;
            padding: 0px 2px 0px 2px;
        """)
            self._lay.addWidget(label, x, y, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)

    def add_Label_Timeline(self, layout, text, x, y):
        '''text must be a string containing the directory path'''
        label = QtWidgets.QLabel()
        tag=os.path.basename(text).split('_')[0]
        label.setText(tag)
        label.setFont(QtGui.QFont("Helvetica", 12, QtGui.QFont.Black))
        label.setStyleSheet("""
        background-color: white;
        color: black;
        padding: 5px 2px 0px 2px;
    """)
        layout.addWidget(label, x, y, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)

    def buttonClicked(self):
        button = self.sender()            
        idx=self._lay.indexOf(button)
        location = self._lay.getItemPosition(idx)
        self.currentButtonIndex=location
#        print("location", location, "Type locationx", type(location))
#        print("Button", button, "at row/col", location[:2])
#        fileindex=location[0]*MaxCol + location[1]
#        print("self.files well index ", fileindex)
#        self.LoadWellImage(self.files[fileindex])
        
        well=button.text()
        self.currentWell=well
        
        path=self.buildWellImagePath(self.imageDir, well, self.well_images)
        self.open_image(path)
        #Change color of button after click
        self.ChangeButtonColor(self._lay, self.currentButtonIndex, state="active")
        
        #Save Notes previous well before loading New notes
        if self.previousWell is None:
            self.LoadNotes(self.rootDir, self.date, well)
#            print("\n\npreviousWell ", self.previousWell)
#            print("currentWell ", self.currentWell)
            self.previousWell=well

        else:
#            print("\n\npreviousWell ", self.previousWell)
#            print("currentWell ", self.currentWell)
            self.SaveNotes(self.previousWell)
            #Load notes current wells
            self.LoadNotes(self.rootDir, self.date, well)
            #change Color previous well to "checked"
            for widget_item in self.layout_widgets(self._lay):
                widget = widget_item.widget()             
                previousButtonIndex=self._lay.getItemPosition(self._lay.indexOf(widget))
                if widget.text()==self.previousWell:
                    self.ChangeButtonColor(self._lay, previousButtonIndex, state="checked")
            #Update self.previousWell
            self.previousWell=well

        self.Set_ScoreButtonState(self.Scoring_Layout, self.classifications[well])
        self.Load_Timeline(self.rootDir, self.imageDir, well)
        

    def LoadWellImage(self,path):
#        imageLabel = QLabel()
#        image=QImage(path)
#        imageLabel.setPixmap(QPixmap.fromImage(image))
        QtGui.QPixmapCache.clear()
        label=QLabel(self)
        pixmap=QPixmap(path)
        #resize pixmap to size of the QscrollArea Temporary?
        label.setPixmap(pixmap.scaled(860, 630, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation))
        self.ImageViewer.setWidget(label)

    def open_image(self, path):
        '''based on https://vincent-vande-vyvre.developpez.com/tutoriels/pyqt/manipulation-images/'''
        w_view, h_view = self.view.width(), self.view.height() 
        self.current_image = QtGui.QImage(path)
        self.pixmap = QtGui.QPixmap.fromImage(self.current_image.scaled(w_view, h_view,
                                    QtCore.Qt.KeepAspectRatio, 
                                    QtCore.Qt.SmoothTransformation))
        self.view_current()

    def view_current(self):
        '''based on https://vincent-vande-vyvre.developpez.com/tutoriels/pyqt/manipulation-images/'''
#        self.view = QtWidgets.QGraphicsView(self.scene)
        w_pix, h_pix = self.pixmap.width(), self.pixmap.height()
        self.scene.clear()
        self.scene.setSceneRect(0, 0, w_pix, h_pix)
        self.scene.addPixmap(self.pixmap)
        self.view.setScene(self.scene)


    def wheel_event (self, event):
        '''based on https://vincent-vande-vyvre.developpez.com/tutoriels/pyqt/manipulation-images/'''
        if self.previousWell is not None: #To prevent crash at startup if using the wheel
            steps = event.angleDelta().y() / 120.0
            self.zoom(steps)
            event.accept()
    

    def zoom(self, step):
        '''based on https://vincent-vande-vyvre.developpez.com/tutoriels/pyqt/manipulation-images/'''
        w_pix, h_pix = self.pixmap.width(), self.pixmap.height()
        w, h = w_pix * (1 + 0.1*step), h_pix * (1 + 0.1*step)
        self.pixmap = QtGui.QPixmap.fromImage(self.current_image.scaled(w, h, 
                                            QtCore.Qt.KeepAspectRatio, 
                                            QtCore.Qt.FastTransformation))
        self.view_current()


    def compare_most_recent(self,most_recent, date):
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

    def check_previous_notes(self, path, current_date):
        path=path + "/Image_Data/"
        ensure_directory(path)
        if not Path(path + current_date).exists():
            print("> No previous notes found in directory:")
            print("> " + path)
   
        most_recent = "18000101" #YYYYMMDD
        
        folders=[str(i) for i in Path(path).iterdir() if i.is_dir()]
#        print("FOLDERS ", folders)

        for folder in folders:
            date = folder.split("/")[-1]
            if date == current_date:
                return
            most_recent = self.compare_most_recent(most_recent, date)
        newPath = path + current_date + "/"

        if len(os.listdir(path)) !=0:
            path = path + most_recent + "/"
            ensure_directory(newPath)
            for file in os.listdir(path):
                copyfile(path + file , newPath + file)
            print("> Copied previous notes from: " + most_recent)
            print("> ")
        else:
            ensure_directory(newPath)


    def LoadNotes(self, path, date, well):
        data_file=Path(self.rootDir).joinpath("Image_Data", self.date, "%s_data.txt"%well)
        self.Notes_TextEdit.clear()
        if Path(data_file).exists():
            with open(data_file, "r") as f:
                content=f.readlines()
                notes=content[10:]
                for i in notes: self.Notes_TextEdit.insertPlainText(i)


    def SaveNotes(self, well):
        '''Save Notes in QPlainTextEdit and more'''
        text=self.Notes_TextEdit.toPlainText()
        path=Path(self.rootDir).joinpath("Image_Data", self.date, "%s_data.txt"%well)
        Notes=[]
        Notes.append("Project Code:%s:\n"%self.project)
        Notes.append("Target Name:%s:\n"%self.target)
        Notes.append("Plate Name:%s:\n"%self.plate)
        Notes.append("Date:%s:\n"%self.date)
        Notes.append("\n")
        Notes.append("Classification:%s:\n"%self.classifications[well])
        Notes.append("\n\n")
        Notes.append("Notes:\n")
        Notes.append("\n")
        Notes.append(text)

        print("Saving data to %s"%path)
        try:
            with open(path, 'w') as f:
                for i in Notes: f.write(i)
        except Exception as e:
            self.dialog_critical(str(e))
               

    def ReadClassification(self, path, date, well):
#        data_file=path+ "/Image_Data/" + date + "/" + well + "/" + "image_data_0.txt"
        data_file=Path(self.rootDir).joinpath("Image_Data", self.date, "%s_data.txt"%well)
        if Path(data_file).exists():
            with open(data_file, "r") as f:
                content=f.readlines()
                classifications = content[5].split(":")
                self.AddtoClassificationDict(well, classifications[1])
        else:
            self.AddtoClassificationDict(well, "Unknown")


    def AddtoClassificationDict(self, well, classification):
        '''Create a dictionnary with well and classification'''
        self.classifications[well]=classification


    def FilterClassification(self, layout, classification):
        for widget_item in self.layout_widgets(layout):
            widget = widget_item.widget()
            if self.classifications[widget.text()]==classification:
#                widget.setEnabled(True)
                widget.setVisible(True)
            elif classification=="All":
#                widget.setEnabled(True)
                widget.setVisible(True)
            else:
#                widget.setEnabled(False)
                widget.setVisible(False)
#            print("well ",widget.text(), "dico Classif ", self.classifications[widget.text()])


    def layout_widgets(self,layout):
        return (layout.itemAt(i) for i in range(layout.count()))


    def ClearLayout(self, layout):
        for widget_item in self.layout_widgets(layout):
                widget_item.widget().deleteLater()


    def ScoreDrop(self, radioButton, well):
        if radioButton.isChecked() is True:
            if radioButton.text()=="Phase Separation":
                self.classifications[well]="PhaseSep"
            else:
                self.classifications[well]=radioButton.text()


    def Set_ScoreButtonState(self, layout, classification):
        #Reset Activation State first
        for widget_item in self.layout_widgets(layout):
            widget = widget_item.widget()
            if widget.isChecked() is True:
                widget.setAutoExclusive(False)
                widget.setChecked(False)
            widget.setAutoExclusive(True)
        #Then do the job
        for widget_item in self.layout_widgets(layout):
            widget = widget_item.widget()
            if widget.text()==classification:
                widget.setChecked(True)
            elif classification=="Unknown":
                widget.setChecked(False)
            elif classification=="PhaseSep":
                if widget.text()=="Phase Separation": widget.setChecked(True)
                else: widget.setChecked(False)
            else:
                widget.setChecked(False)


    def Load_Timeline(self, rootdirectory, imagedir, well):
        rootdirectory = Path(rootdirectory)
        other_dates = []
        for i in os.listdir(rootdirectory):
            if i!="Image_Data":
                path=Path(rootdirectory).joinpath(i)
                if os.path.isdir(path): other_dates.append(path)
        other_dates.sort()
        
        self.ClearLayout(self._timlay)
        
        for date in other_dates:
            if imagedir.split("/")[-1]=="rawimages":
                path=Path(date).joinpath("rawimages")
            else:
                path=Path(date)
            name=self.buildWellImagePath(str(path), well, self.well_images)
            if Path(name).exists():
                pixmap = QtGui.QPixmap(name)
                self.add_Timeline_pixmap(self._timlay, pixmap.scaled(300, 230, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation), 0, other_dates.index(date))
                self.add_Label_Timeline(self._timlay, date, 0,other_dates.index(date))
        self.label_CurrentWell.setText(well)


    def ActivateButton(self,layout, idx):
        '''Activate a button in a QgridLayout,
        idx is a tuple of the current Button'''
        if idx is None: return
        row=idx[0]
        col=idx[1]
        # item = layout.itemAtPosition(row,col)
        try:
            item = layout.itemAtPosition(row,col)
            widget=item.widget()
            widget.click()
        except ValueError:
            return
          

    def ChangeButtonColor(self, layout, idx, state="active"):
        '''Change color of the button'''
        if idx is None: return
        row=idx[0]
        col=idx[1]
        try:
            item = layout.itemAtPosition(row,col)
            widget=item.widget()
        except:
            self.handle_error("Navigation error")
            
        if state=="active":
            widget.setStyleSheet("""color: black;background-color: cyan;""")
        elif state=="checked":
            widget.setStyleSheet("""color: black;background-color: blue;""")
        

    def keyPressEvent(self, event):
        '''iterate over a grid using the cursor and assign quickly classification'''
        if self.currentButtonIndex is None:
            return
        location=self.currentButtonIndex
        currentrow=location[0]; currentcol=location[1]
        self.ChangeButtonColor(self._lay, self.currentButtonIndex, state="checked")
        NumberOfColumns=self._lay.columnCount()
        # if event.key()==QtCore.Qt.Key_Q:
        shortcut=Shortcuts.Shortcut()
        if event.key()==shortcut.MoveLeft:
#            print("Left Arrow")
            if currentcol==0:
                Newlocation=(currentrow-1, NumberOfColumns-1,location[2],location[3])
                try:
                    self.ActivateButton(self._lay, Newlocation)
                except:
                    self.handle_error("Already at first well")
            else:
                Newlocation=(currentrow, currentcol-1,location[2],location[3])
#                print("Newlocation ", Newlocation)
                self.ActivateButton(self._lay, Newlocation)

        if event.key()==shortcut.MoveRight:
#            print("Right Arrow")
            if currentcol==NumberOfColumns-1:
                Newlocation=(currentrow+1, 0,location[2],location[3])
                try:
                    self.ActivateButton(self._lay, Newlocation)
                except:
                    self.handle_error("Already at last well")
            else:
                Newlocation=(currentrow, currentcol+1,location[2],location[3])
#                print("Newlocation ", Newlocation)
                self.ActivateButton(self._lay, Newlocation)
            
        if event.key()==shortcut.MoveUp:
#            print("Up Arrow")
            Newlocation=(currentrow-1, currentcol,location[2],location[3])
            try:
                self.ActivateButton(self._lay, Newlocation)
            except:
                self.handle_error("Already at first row")
            
        if event.key()==shortcut.MoveDown:
#            print("Down Arrow")
            Newlocation=(currentrow+1, currentcol,location[2],location[3])
            try:
                self.ActivateButton(self._lay, Newlocation)
            except:
                self.handle_error("Already at last row")
                
        if event.key()==shortcut.Clear:
            self.radioButton_ScoreClear.setChecked(True)
        elif event.key()==shortcut.Crystal:
            self.radioButton_ScoreCrystal.setChecked(True)
        elif event.key()==shortcut.Precipitate:
            self.radioButton_ScorePrecipitate.setChecked(True)
        elif event.key()==shortcut.PhaseSep:
            self.radioButton_ScorePhaseSep.setChecked(True)
        elif event.key()==shortcut.Other:
            self.radioButton_ScoreOther.setChecked(True)

    def Calculate_Statistics(self):
        '''Calculate statistics for plate'''

        Count_subwell_a={"Clear":0, "Precipitate":0, "Crystal":0, "PhaseSep":0, "Other":0, "Unknown":0}
        Count_subwell_b={"Clear":0, "Precipitate":0, "Crystal":0, "PhaseSep":0, "Other":0, "Unknown":0}
        Count_subwell_c={"Clear":0, "Precipitate":0, "Crystal":0, "PhaseSep":0, "Other":0, "Unknown":0}
        Count_nosubwell={"Clear":0, "Precipitate":0, "Crystal":0, "PhaseSep":0, "Other":0, "Unknown":0}
        
         
        for well,classification in self.classifications.items():
#                print("well= ", well,"classification= ", classification)
            if "a" in well:
                 Count_subwell_a[classification]+=1
            elif "b" in well:
                 Count_subwell_b[classification]+=1
            elif "c" in well:
                 Count_subwell_c[classification]+=1
            else:
                 Count_nosubwell[classification]+=1                    
        
        _list=[Count_subwell_a,Count_subwell_b,Count_subwell_c,Count_nosubwell]
        totals=[]
        for i in _list:
            total=0 #reset counter
            for classification, count in i.items():
                total +=count
            totals.append(total)

        for i in _list:
            for classification, count in i.items():
                try:
                    i[classification]=round(count/totals[_list.index(i)]*100,1)
                except ValueError:
                    i[classification]=0
                except ZeroDivisionError:
                    i[classification]=0
        print("Stats subwell a in %", _list[0])
        print("Stats subwell b in %", _list[1])
        print("Stats subwell c in %", _list[2])
        print("Stats no subwell in %", _list[3])
        return _list
        
            
    def on_exit(self):
        '''things to do before exiting'''
#        self.SaveNotes(self.currentWell)
        

# class StatsWindow(QtWidgets.QDialog, Ui_Dialog):
#     def __init__(self, parent=None):
#         super(StatsWindow, self).__init__(parent)
#         ui = Ui_Dialog()
#         self.setupUi(self)

class HeatMapGrid(QtWidgets.QDialog, Ui_Dialog):
    ''' '''
    def __init__(self, parent=None):
        super(HeatMapGrid, self).__init__(parent)
        ui = Ui_Dialog()
        self.setupUi(self)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.paint_heat_diagram(qp)
        qp.end()


    def paint_heat_diagram(self, qp):
        '''adapted from https://github.com/dakota0064/Fluorescent_Robotic_Imager '''

        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        wells = ['a', 'b', 'c']

        total_wells = [row + str(col) + str(well) for row in rows for col in cols for well in wells]

        def well_to_coordinates(well):
            row = int(ord(well[0])) - 65
            column = int(('').join(re.findall(r'\d+',well))) - 1
            try:
                well[-1] in wells
                subrow = wells.index(well[-1])
            except:
                subrow = 0
            x1 = 80 + (column * 80)
            dx = 20
            y1 = (80 + row * 80) + (subrow * 20)
            dy = 20
            return x1, y1, dx, dy, subrow
        
        for row in rows:
            row_int = int(ord(row)) - 65
            y1 = 120 + row_int * 80
            qp.setFont(QFont("Courier New", 20))
            qp.drawText(40, y1,row)  

        for col in cols:
            col_int = int(col) - 1
            x1 = 80 + (col_int * 80)
            qp.setFont(QFont("Courier New", 20))
            qp.drawText(x1, 40, col)  

        for well in total_wells:
            coordinates = well_to_coordinates(well)
            qp.setBrush(QColor(0, 0, 0))
            qp.drawRect(coordinates[0], coordinates[1], coordinates[2], coordinates[3])
#            
        classification=str
        for i in range(len(self.well_images)):
            well = self.well_images[i].split(".")[0]
            coordinates = well_to_coordinates(well)
            try:
                classification = self.classifications[well]
            except:
                classification=="Unknown"
            color=QtGui.QColor()
            if classification == "Unknown":
                color = QtGui.QColor(0, 0, 0) #Black
            elif classification == "Clear":
                color = QtGui.QColor(255, 255, 255) #White
            elif classification == "Precipitate":
                color = QtGui.QColor(255, 0, 0) #red
            elif classification == "Crystal":
                color = QtGui.QColor(0, 255, 0) #green
            elif classification == "PhaseSep":
                color = QtGui.QColor(255, 153, 51) #orange
            elif classification == "Other":
                color = QtGui.QColor(255, 0, 255) #magenta
            qp.setBrush(color)
            qp.drawRect(coordinates[0], coordinates[1], coordinates[2], coordinates[3])
            if well[-1] not in wells:
                qp.drawText(coordinates[0], coordinates[1], coordinates[2], coordinates[3], QtCore.Qt.AlignCenter,'')
            else:
                qp.setFont(QFont("Courier New", 10))
                qp.drawText(coordinates[0], coordinates[1], coordinates[2], coordinates[3], QtCore.Qt.AlignCenter, wells[coordinates[4]])


            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    MainWindow = ViewerModule()
    sys.exit(app.exec_())
    Citation()
