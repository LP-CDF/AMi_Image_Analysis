#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 09:36:00 2021

"""

__version__ = "0.0.1"
__author__ = "Ludovic Pecqueur (ludovic.pecqueur \at college-de-france.fr)"
__date__ = "30-06-2021"
__license__ = "New BSD http://www.opensource.org/licenses/bsd-license.php"


from PyQt5 import QtCore, QtWidgets, QtGui
import os, re
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel,QFrame, QProgressDialog
from pathlib import Path
from preferences import ClassificationColor
from utils import ensure_directory, Ext

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        # Dialog.setObjectName("Dialog")
        # Dialog.resize(1100, 760)
        Dialog.resize(1600, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(140, 720, 761, 21))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_ExportImage = QtWidgets.QPushButton(Dialog)
        self.pushButton_ExportImage.setGeometry(QtCore.QRect(400, 870, 101, 25))
        self.pushButton_ExportImage.setObjectName("pushButton_ExportImage")
        self.pushButton_Close = QtWidgets.QPushButton(Dialog)
        self.pushButton_Close.setGeometry(QtCore.QRect(540, 870, 101, 25))
        self.pushButton_Close.setObjectName("pushButton_Close")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Results"))
        self.pushButton_ExportImage.setText(_translate("Dialog", "Export JPEG"))
        self.pushButton_Close.setText(_translate("Dialog", "Close"))

# class Plate(QtWidgets.QDialog,PlateOverview.Ui_Dialog):
#     ''' '''
#     def __init__(self, parent=None):
#         super(Plate, self).__init__(parent)
#         self.dx=120
#         self.dy=90
#         self.setupUi(self)
    
#     def paintEvent(self, e):
#         qp = QtGui.QPainter()
#         qp.begin(self)
#         self.paint_Grid(qp)
#         qp.end()
#         QtGui.QPixmapCache.clear()

#     def paint_Grid(self, qp):
#         ''' adapted from https://github.com/dakota0064/Fluorescent_Robotic_Imager '''

#         rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
#         cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
#         wells = ['a', 'b', 'c']

#         total_wells = [row + str(col) for row in rows for col in cols]

#         def well_to_coordinates(well):
#             row = int(ord(well[0])) - 65
#             column = int(('').join(re.findall(r'\d+',well))) - 1
#             x1 = 80 + (column * self.dx)
#             y1 = (80 + row * self.dy)
#             return (x1, y1, self.dx, self.dy)
        
#         for row in rows:
#             row_int = int(ord(row)) - 65
#             y1 = 80 + row_int * self.dy
#             qp.setFont(QFont("Courier New", 20))
#             qp.drawText(0, y1, self.dx, self.dy, QtCore.Qt.AlignCenter, row)  

#         for col in cols:
#             col_int = int(col) - 1
#             x1 = 80 + (col_int * self.dx)
#             qp.setFont(QFont("Courier New", 20))
#             qp.drawText(x1, 5, self.dx, self.dy, QtCore.Qt.AlignCenter, col)
        
#         for path in self.files:
#             filepath=Path(path)
#             well=filepath.stem
#             # print("path: ", path, "filepath: ", filepath)
#             if self.subwell!="" and self.subwell in well[-1]:
#                 (x1, y1, dx, dy) = well_to_coordinates(well)
#                 # r = QtCore.QRect(x1, y1, dx, dy)
#                 pixmap=QPixmap(str(filepath))
#                 pixmap = pixmap.scaled(dx,dy, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
#                 qp.drawPixmap(x1,y1,dx,dy, pixmap)
#                 # QtGui.QPixmapCache.clear()
#                 # del pixmap,filepath
#             elif self.subwell=="" and well[-1] not in wells:
#                 (x1, y1, dx, dy) = well_to_coordinates(well)
#                 # r = QtCore.QRect(x1, y1, dx, dy)
#                 pixmap=QPixmap(str(filepath))
#                 pixmap = pixmap.scaled(dx,dy, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
#                 qp.drawPixmap(x1,y1,dx,dy, pixmap)
#                 # QtGui.QPixmapCache.clear()
#                 # del pixmap,filepath
#             else:
#                 continue

class Plate(QTableWidget):
    def __init__(self, r, c, rootDir, date):
        super().__init__(r, c)
        self.dx=120
        self.dy=90
        self.rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        self.wells = ['a', 'b', 'c']
        self.resizedpath=Path(rootDir).joinpath("Image_Data", date, "Miniatures")
        ensure_directory(self.resizedpath)
        self.miniatures=[os.path.join(self.resizedpath, file) for file in os.listdir(self.resizedpath) if os.path.splitext(file)[1] in Ext]

    def well_to_coordinates(self,well):
        row = int(ord(well[0])) - 64
        column = int(('').join(re.findall(r'\d+',well)))
        return (row, column)

    def UpdateBorder(self, files, classifications):
        for path in files:
            well=Path(path).stem
            if self.subwell!="" and self.subwell in well[-1]:
                (row, column)=self.well_to_coordinates(str(well))
                item=self.cellWidget(row, column)
                item.setStyleSheet("color: %s;"%ClassificationColor[classifications[well]]["background"])
            elif self.subwell=="" and well[-1] not in self.wells:
                (row, column)=self.well_to_coordinates(str(well))
                item=self.cellWidget(row, column)
                item.setStyleSheet("color: %s;"%ClassificationColor[classifications[well]]["background"])
            else: continue

    def create_miniatures(self, files):
        count, size=0, len(files)
        progress = QProgressDialog("Generating miniatures...", "Abort", 0, size)
        progress.setWindowTitle("Plate Overview")
        progress.setMinimumWidth(300)
        progress.setModal(True)
        for path in files:
            progress.setValue(count+1)
            filepath=Path(path)
            well=filepath.stem
            pixmap=QPixmap(str(filepath))
            pixmap = pixmap.scaled(self.dx,self.dy, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
            path=self.resizedpath.joinpath("%s.jpg"%well)
            pixmap.save(str(path))
            count+=1
            if progress.wasCanceled(): break

    def create_table(self, files, classifications):
        #Create miniatures if not present
        if len(self.miniatures)!=len(files):
            self.create_miniatures(files)
            self.miniatures=[os.path.join(self.resizedpath, file) for file in os.listdir(self.resizedpath) if os.path.splitext(file)[1] in Ext]
        
        for path in self.miniatures:
            filepath=Path(path)
            well=filepath.stem
            for row in self.rows:
                item = QTableWidgetItem(row)
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                item.setFont(QFont("Courier New", 20))
                self.setItem(self.rows.index(row)+1,0, item)
            for col in self.cols:
                item = QTableWidgetItem(col)
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                item.setFont(QFont("Courier New", 20))
                self.setItem(0, self.cols.index(col)+1, item)
                
            if self.subwell!="" and self.subwell in well[-1]:
                (row, column)=self.well_to_coordinates(str(well))
                label=QLabel()
                pixmap=QPixmap(str(filepath))
                # pixmap = pixmap.scaled(self.dx,self.dy, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                label.setPixmap(pixmap)
                label.setFrameShape(QFrame.Panel)
                label.setLineWidth(2)
                label.setStyleSheet("color: %s;"%ClassificationColor[classifications[well]]["background"])
                label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.setCellWidget(row, column, label)
            elif self.subwell=="" and well[-1] not in self.wells:
                (row, column)=self.well_to_coordinates(str(well))
                label=QLabel()
                pixmap=QPixmap(str(filepath))
                # pixmap = pixmap.scaled(self.dx-2,self.dy-2, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                label.setPixmap(pixmap)
                label.setFrameShape(QFrame.Panel)
                label.setLineWidth(2)
                label.setStyleSheet("color: %s;"%ClassificationColor[classifications[well]]["background"])
                label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.setCellWidget(row, column, label)
            else:
                continue
            self.horizontalHeader().setDefaultSectionSize(self.dx)
            self.verticalHeader().setDefaultSectionSize(self.dy)
            self.horizontalHeader().resizeSection(0,50)
            self.verticalHeader().resizeSection(0,50)
            

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())