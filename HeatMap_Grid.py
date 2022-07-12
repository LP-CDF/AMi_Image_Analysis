# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DesignerFiles/HeatMap.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont, QColor
from utils import rows, cols, wells
from preferences import ClassificationColor


class Ui_Dialog():
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1040, 760)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.pushButton_ExportImage = QtWidgets.QPushButton(Dialog)
        self.pushButton_ExportImage.setGeometry(QtCore.QRect(400, 730, 101, 25))
        self.pushButton_ExportImage.setObjectName("pushButton_ExportImage")
        self.pushButton_Close = QtWidgets.QPushButton(Dialog)
        self.pushButton_Close.setGeometry(QtCore.QRect(540, 730, 101, 25))
        self.pushButton_Close.setObjectName("pushButton_Close")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Heat Map Grid"))
        self.pushButton_ExportImage.setText(_translate("Dialog", "Export JPEG"))
        self.pushButton_Close.setText(_translate("Dialog", "Close"))

class HeatMapGrid(QtWidgets.QDialog, Ui_Dialog):
    ''' '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.well_images=None
        self.classifications=None
        self.notes=None
        self.setupUi(self)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.paint_heat_diagram(qp)
        qp.end()

    def paint_heat_diagram(self, qp):
        ''' adapted from https://github.com/dakota0064/Fluorescent_Robotic_Imager '''

        # rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        # cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        # wells = ['a', 'b', 'c']

        total_wells = [row + str(col) + str(well)
                       for row in rows for col in cols for well in wells]

        def well_to_coordinates(well):
            row = int(ord(well[0])) - 65
            column = int(('').join(re.findall(r'\d+', well))) - 1
            try:
                well[-1] in wells
                subrow = wells.index(well[-1])
            except:
                subrow = 0
            x1 = 80 + (column * 80)
            dx = 20
            y1 = (80 + row * 80) + (subrow * 20)
            dy = 20
            return (x1, y1, dx, dy, subrow)

        for row in rows:
            row_int = int(ord(row)) - 65
            y1 = 80 + row_int * 80
            qp.setFont(QFont("Courier New", 20))
            # qp.drawText(40, y1,row)
            qp.drawText(20, y1, 60, 60, QtCore.Qt.AlignCenter, row)

        for col in cols:
            col_int = int(col) - 1
            x1 = 70 + (col_int * 80)
            qp.setFont(QFont("Courier New", 20))
            # qp.drawText(x1, 40, col)
            qp.drawText(x1, 30, 40, 40, QtCore.Qt.AlignCenter, col)

        for well in total_wells:
            (x1, y1, dx, dy, subrow) = well_to_coordinates(well)
            qp.setBrush(QColor(0, 0, 0))
            qp.drawRect(x1, y1, dx, dy)

        classification = str
        for i in range(len(self.well_images)):
            well = self.well_images[i].split(".")[0]
            (x1, y1, dx, dy, subrow) = well_to_coordinates(well)
            try:
                classification = self.classifications[well]
            except:
                classification = "Unknown"
            color = QtGui.QColor()
            if classification == "Unknown":
                color = QtGui.QColor(ClassificationColor["Unknown"]["Qcolor"])
            elif classification == "Clear":
                color = QtGui.QColor(ClassificationColor["Clear"]["Qcolor"])
            elif classification == "Precipitate":
                color = QtGui.QColor(
                    ClassificationColor["Precipitate"]["Qcolor"])
            elif classification == "Crystal":
                color = QtGui.QColor(ClassificationColor["Crystal"]["Qcolor"])
            elif classification == "PhaseSep":
                color = QtGui.QColor(ClassificationColor["PhaseSep"]["Qcolor"])
            elif classification == "Other":
                color = QtGui.QColor(ClassificationColor["Other"]["Qcolor"])
            qp.setBrush(color)
            qp.drawRect(x1, y1, dx, dy)
            if self.notes[well] is True:
                qp.setBrush(QColor(0, 0, 0))
                # qp.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine))
                qp.drawEllipse(x1+25, y1+6, 8, 8)  # 6=(dy-8)/2
                # qp.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
            if well[-1] not in wells:
                qp.drawText(x1, y1, dx, dy, QtCore.Qt.AlignCenter, '')
            else:
                qp.setFont(QFont("Courier New", 10))
                qp.drawText(x1, y1, dx, dy,
                            QtCore.Qt.AlignCenter, wells[subrow])

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
