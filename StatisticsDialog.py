# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DesignerFiles/Statistics.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(543, 254)
        self.StatisticsTable = QtWidgets.QTableWidget(Dialog)
        self.StatisticsTable.setGeometry(QtCore.QRect(0, 0, 541, 211))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StatisticsTable.sizePolicy().hasHeightForWidth())
        self.StatisticsTable.setSizePolicy(sizePolicy)
        self.StatisticsTable.setObjectName("StatisticsTable")
        self.StatisticsTable.setColumnCount(4)
        self.StatisticsTable.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.StatisticsTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.StatisticsTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.StatisticsTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.StatisticsTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.StatisticsTable.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.StatisticsTable.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.StatisticsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.StatisticsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.StatisticsTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.StatisticsTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.StatisticsTable.setItem(0, 0, item)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 220, 541, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_Export = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_Export.setObjectName("pushButton_Export")
        self.horizontalLayout.addWidget(self.pushButton_Export)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.horizontalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Statistics in percent"))
        item = self.StatisticsTable.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "Clear"))
        item = self.StatisticsTable.verticalHeaderItem(1)
        item.setText(_translate("Dialog", "Precipitate"))
        item = self.StatisticsTable.verticalHeaderItem(2)
        item.setText(_translate("Dialog", "Crystal"))
        item = self.StatisticsTable.verticalHeaderItem(3)
        item.setText(_translate("Dialog", "Phase Separation"))
        item = self.StatisticsTable.verticalHeaderItem(4)
        item.setText(_translate("Dialog", "Other"))
        item = self.StatisticsTable.verticalHeaderItem(5)
        item.setText(_translate("Dialog", "Unsorted"))
        item = self.StatisticsTable.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Subwell a"))
        item = self.StatisticsTable.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Subwell b"))
        item = self.StatisticsTable.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Subwell c"))
        item = self.StatisticsTable.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "No subwell"))
        __sortingEnabled = self.StatisticsTable.isSortingEnabled()
        self.StatisticsTable.setSortingEnabled(False)
        self.StatisticsTable.setSortingEnabled(__sortingEnabled)
        self.pushButton_Export.setText(_translate("Dialog", "Export"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
