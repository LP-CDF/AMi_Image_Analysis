#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 09:36:00 2021

"""

__version__ = "0.0.2"
__author__ = "Ludovic Pecqueur (ludovic.pecqueur \at college-de-france.fr)"
__date__ = "07-07-2022"
__license__ = "New BSD http://www.opensource.org/licenses/bsd-license.php"


from PyQt5 import QtCore, QtWidgets
import os
import re
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QProgressDialog
from pathlib import Path
from preferences import ClassificationColor
from utils import ensure_directory, Ext, rows, cols, wells


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.resize(1600, 900)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(
            QtCore.QRect(140, 720, 761, 21))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_ExportImage = QtWidgets.QPushButton(Dialog)
        self.pushButton_ExportImage.setGeometry(
            QtCore.QRect(400, 870, 101, 25))
        self.pushButton_ExportImage.setObjectName("pushButton_ExportImage")
        self.pushButton_Close = QtWidgets.QPushButton(Dialog)
        self.pushButton_Close.setGeometry(QtCore.QRect(540, 870, 101, 25))
        self.pushButton_Close.setObjectName("pushButton_Close")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Results"))
        self.pushButton_ExportImage.setText(
            _translate("Dialog", "Export JPEG"))
        self.pushButton_Close.setText(_translate("Dialog", "Close"))


class Plate(QTableWidget):
    testSignal = QtCore.pyqtSignal()
    def __init__(self, r, c, rootDir, date, files):
        super().__init__(r, c)
        self.dx = 120
        self.dy = 90
        self.rows = rows
        self.cols = cols
        self.wells = wells
        self.files=files
        self.resizedpath = Path(rootDir).joinpath(
            "Image_Data", date, "Miniatures")
        ensure_directory(self.resizedpath)
        self.miniatures = [os.path.join(self.resizedpath, file) for file in os.listdir(
            self.resizedpath) if os.path.splitext(file)[1] in Ext]
        self.CLICKED=None
        self.RETURNPATH=None
        self.testSignal.connect(self.returnpath)

    def well_to_coordinates(self, well):
        row = int(ord(well[0])) - 64
        column = int(('').join(re.findall(r'\d+', well)))
        return (row, column)

    def UpdateBorder(self, files, classifications):
        for path in files:
            well = Path(path).stem
            if self.subwell != "" and self.subwell in well[-1]:
                (row, column) = self.well_to_coordinates(str(well))
                item = self.cellWidget(row, column)
                item.setStyleSheet(
                    "border :2px solid %s"% ClassificationColor[classifications[well]]["background"])
            elif self.subwell == "" and well[-1] not in self.wells:
                (row, column) = self.well_to_coordinates(str(well))
                item = self.cellWidget(row, column)
                item.setStyleSheet(
                    "border :2px solid %s"% ClassificationColor[classifications[well]]["background"])
            else:
                continue

    def ScaleAndSavePixmap(self, path):
        filepath = Path(path)
        well = filepath.stem
        pixmap = QPixmap(str(filepath))
        pixmap = pixmap.scaled(
            self.dx, self.dy, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        path = self.resizedpath.joinpath("%s.jpg" % well)
        pixmap.save(str(path))
        return 1  # return 1 when done to increment counter

    def create_miniatures(self, files):
        count, size = 0, len(files)
        progress = QProgressDialog(
            "Generating miniatures...", "Abort", 0, size)
        progress.setWindowTitle("Plate Overview")
        progress.setMinimumWidth(300)
        progress.setModal(True)

        for path in files:
            progress.setValue(count+1)
            self.ScaleAndSavePixmap(path)
            count += 1
            if progress.wasCanceled():
                break

    def create_table(self, files, classifications):
        # Create miniatures if not present
        if len(self.miniatures) != len(files):
            self.create_miniatures(files)
            self.miniatures = [os.path.join(self.resizedpath, file) for file in os.listdir(
                self.resizedpath) if os.path.splitext(file)[1] in Ext]

        for path in self.miniatures:
            filepath = Path(path)
            well = filepath.stem
            for row in self.rows:
                item = QTableWidgetItem(row)
                item.setTextAlignment(
                    QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                item.setFont(QFont("Courier New", 20))
                self.setItem(self.rows.index(row)+1, 0, item)
            for col in self.cols:
                item = QTableWidgetItem(col)
                item.setTextAlignment(
                    QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                item.setFont(QFont("Courier New", 20))
                self.setItem(0, self.cols.index(col)+1, item)

            if self.subwell != "" and self.subwell in well[-1]:
                (row, column) = self.well_to_coordinates(str(well))
                # label = QLabel()
                # pixmap = QPixmap(str(filepath))
                # label.setPixmap(pixmap)
                # label.setFrameShape(QFrame.Panel)
                # label.setLineWidth(2)
                # label.setStyleSheet(
                #     "color: %s;" % ClassificationColor[classifications[well]]["background"])
                # label.setAlignment(QtCore.Qt.AlignHCenter |
                #                    QtCore.Qt.AlignVCenter)
                # self.setCellWidget(row, column, label)
                
                button=QtWidgets.QPushButton()
                button.clicked.connect(self.clickme)
                button.setIcon(QIcon(str(filepath)))
                button.setIconSize(QtCore.QSize(self.dx-6,self.dy-6))
                button.setStyleSheet("border :2px solid %s"% 
                                     ClassificationColor[classifications[well]]["background"])
                self.setCellWidget(row, column, button)    
            elif self.subwell == "" and well[-1] not in self.wells:
                (row, column) = self.well_to_coordinates(str(well))
                # label = QLabel()
                # pixmap = QPixmap(str(filepath))
                # label.setPixmap(pixmap)
                # label.setFrameShape(QFrame.Panel)
                # label.setLineWidth(2)
                # label.setStyleSheet(
                #     "color: %s;" % ClassificationColor[classifications[well]]["background"])
                # label.setAlignment(QtCore.Qt.AlignHCenter |
                #                     QtCore.Qt.AlignVCenter)
                # self.setCellWidget(row, column, label)
                button=QtWidgets.QPushButton()
                button.clicked.connect(self.clickme)
                button.setIcon(QIcon(str(filepath)))
                button.setIconSize(QtCore.QSize(self.dx-6,self.dy-6))
                button.setStyleSheet("border :2px solid %s"% 
                                     ClassificationColor[classifications[well]]["background"])
                self.setCellWidget(row, column, button)    
            else:
                continue
            self.horizontalHeader().setDefaultSectionSize(self.dx)
            self.verticalHeader().setDefaultSectionSize(self.dy)
            self.horizontalHeader().resizeSection(0, 50)
            self.verticalHeader().resizeSection(0, 50)

    def clickme(self):
        '''test'''
        self.CLICKED='%s%s%s'%(self.rows[self.currentRow()-1],
                       self.cols[self.currentColumn()-1],
                       self.subwell)
        # print("row: ", self.currentRow(), "column: ", self.currentColumn(),
        #       "well: %s" %self.CLICKED)
        self.testSignal.emit()
    
    def returnpath(self):
        '''returns the tuple (well,path) to clicked well as str'''
        # print("Signal emitted %s"%self.CLICKED)
        search = list(filter(lambda i: self.CLICKED in i, self.files))
        self.RETURNPATH=str(search[0])

        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
