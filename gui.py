# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DesignerFiles/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1600, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalFrame = QtWidgets.QFrame(self.centralwidget)
        self.verticalFrame.setMinimumSize(QtCore.QSize(300, 0))
        self.verticalFrame.setAutoFillBackground(True)
        self.verticalFrame.setObjectName("verticalFrame")
        self.gridLayoutWidget = QtWidgets.QWidget(self.verticalFrame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 671, 631))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.PrepDate = QtWidgets.QLabel(self.gridLayoutWidget)
        self.PrepDate.setObjectName("PrepDate")
        self.gridLayout_3.addWidget(self.PrepDate, 2, 1, 1, 1)
        self.ProjectCode = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ProjectCode.setObjectName("ProjectCode")
        self.gridLayout_3.addWidget(self.ProjectCode, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 2, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 3, 0, 1, 1)
        self.TargetName = QtWidgets.QLabel(self.gridLayoutWidget)
        self.TargetName.setObjectName("TargetName")
        self.gridLayout_3.addWidget(self.TargetName, 2, 3, 1, 1)
        self.ImageDate = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ImageDate.setObjectName("ImageDate")
        self.gridLayout_3.addWidget(self.ImageDate, 3, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 3, 2, 1, 1)
        self.PlateName = QtWidgets.QLabel(self.gridLayoutWidget)
        self.PlateName.setObjectName("PlateName")
        self.gridLayout_3.addWidget(self.PlateName, 3, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.scrollAreaPlate = QtWidgets.QScrollArea(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaPlate.sizePolicy().hasHeightForWidth())
        self.scrollAreaPlate.setSizePolicy(sizePolicy)
        self.scrollAreaPlate.setMouseTracking(True)
        self.scrollAreaPlate.setLineWidth(5)
        self.scrollAreaPlate.setMidLineWidth(0)
        self.scrollAreaPlate.setWidgetResizable(True)
        self.scrollAreaPlate.setObjectName("scrollAreaPlate")
        self.scrollAreaPlateContent = QtWidgets.QWidget()
        self.scrollAreaPlateContent.setGeometry(QtCore.QRect(0, 0, 667, 417))
        self.scrollAreaPlateContent.setObjectName("scrollAreaPlateContent")
        self.scrollAreaPlate.setWidget(self.scrollAreaPlateContent)
        self.gridLayout.addWidget(self.scrollAreaPlate, 3, 0, 1, 1)
        self.FilterBox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.FilterBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FilterBox.sizePolicy().hasHeightForWidth())
        self.FilterBox.setSizePolicy(sizePolicy)
        self.FilterBox.setMinimumSize(QtCore.QSize(635, 100))
        self.FilterBox.setMaximumSize(QtCore.QSize(650, 100))
        self.FilterBox.setAutoFillBackground(False)
        self.FilterBox.setFlat(False)
        self.FilterBox.setCheckable(False)
        self.FilterBox.setObjectName("FilterBox")
        self.layoutWidget = QtWidgets.QWidget(self.FilterBox)
        self.layoutWidget.setGeometry(QtCore.QRect(12, 32, 601, 63))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton_All = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_All.setChecked(True)
        self.radioButton_All.setObjectName("radioButton_All")
        self.verticalLayout.addWidget(self.radioButton_All)
        self.radioButton_Crystal = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_Crystal.setObjectName("radioButton_Crystal")
        self.verticalLayout.addWidget(self.radioButton_Crystal)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radioButton_Clear = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_Clear.setObjectName("radioButton_Clear")
        self.verticalLayout_2.addWidget(self.radioButton_Clear)
        self.radioButton_Other = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_Other.setObjectName("radioButton_Other")
        self.verticalLayout_2.addWidget(self.radioButton_Other)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.radioButton_Precipitate = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_Precipitate.setObjectName("radioButton_Precipitate")
        self.verticalLayout_3.addWidget(self.radioButton_Precipitate)
        self.radioButton_PhaseSep = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_PhaseSep.setObjectName("radioButton_PhaseSep")
        self.verticalLayout_3.addWidget(self.radioButton_PhaseSep)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.radioButton_Unsorted = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_Unsorted.setObjectName("radioButton_Unsorted")
        self.horizontalLayout_2.addWidget(self.radioButton_Unsorted)
        self.labelVisuClassif = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelVisuClassif.sizePolicy().hasHeightForWidth())
        self.labelVisuClassif.setSizePolicy(sizePolicy)
        self.labelVisuClassif.setMinimumSize(QtCore.QSize(175, 50))
        self.labelVisuClassif.setMaximumSize(QtCore.QSize(175, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.labelVisuClassif.setFont(font)
        self.labelVisuClassif.setFrameShape(QtWidgets.QFrame.Box)
        self.labelVisuClassif.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.labelVisuClassif.setText("")
        self.labelVisuClassif.setAlignment(QtCore.Qt.AlignCenter)
        self.labelVisuClassif.setObjectName("labelVisuClassif")
        self.horizontalLayout_2.addWidget(self.labelVisuClassif, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.FilterBox, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, -1, 50, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_ProjectDetails = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ProjectDetails.sizePolicy().hasHeightForWidth())
        self.label_ProjectDetails.setSizePolicy(sizePolicy)
        self.label_ProjectDetails.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_ProjectDetails.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ProjectDetails.setObjectName("label_ProjectDetails")
        self.horizontalLayout_4.addWidget(self.label_ProjectDetails, 0, QtCore.Qt.AlignLeft)
        self.progressBar = QtWidgets.QProgressBar(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_4.addWidget(self.progressBar, 0, QtCore.Qt.AlignLeft)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.verticalFrame)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 650, 1541, 283))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea_Timeline = QtWidgets.QScrollArea(self.gridLayoutWidget_2)
        self.scrollArea_Timeline.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_Timeline.sizePolicy().hasHeightForWidth())
        self.scrollArea_Timeline.setSizePolicy(sizePolicy)
        self.scrollArea_Timeline.setMinimumSize(QtCore.QSize(857, 250))
        self.scrollArea_Timeline.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollArea_Timeline.setBaseSize(QtCore.QSize(400, 250))
        self.scrollArea_Timeline.setWidgetResizable(True)
        self.scrollArea_Timeline.setObjectName("scrollArea_Timeline")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 855, 248))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea_Timeline.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea_Timeline, 1, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(38, 0))
        self.label_2.setMaximumSize(QtCore.QSize(50, 20))
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(50, 0))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 1, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.Notes_TextEdit = QtWidgets.QPlainTextEdit(self.gridLayoutWidget_2)
        self.Notes_TextEdit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Notes_TextEdit.sizePolicy().hasHeightForWidth())
        self.Notes_TextEdit.setSizePolicy(sizePolicy)
        self.Notes_TextEdit.setMinimumSize(QtCore.QSize(300, 250))
        self.Notes_TextEdit.setMaximumSize(QtCore.QSize(16777215, 300))
        self.Notes_TextEdit.setBaseSize(QtCore.QSize(100, 0))
        self.Notes_TextEdit.setWhatsThis("")
        self.Notes_TextEdit.setAccessibleDescription("")
        self.Notes_TextEdit.setAutoFillBackground(False)
        self.Notes_TextEdit.setObjectName("Notes_TextEdit")
        self.gridLayout_2.addWidget(self.Notes_TextEdit, 1, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.groupBox = QtWidgets.QGroupBox(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(150, 100))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setBaseSize(QtCore.QSize(150, 0))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 30, 125, 58))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pushButton_DisplayHeatMap = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_DisplayHeatMap.setObjectName("pushButton_DisplayHeatMap")
        self.verticalLayout_5.addWidget(self.pushButton_DisplayHeatMap)
        self.pushButton_ExportToPDF = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_ExportToPDF.setObjectName("pushButton_ExportToPDF")
        self.verticalLayout_5.addWidget(self.pushButton_ExportToPDF)
        self.gridLayout_2.addWidget(self.groupBox, 1, 3, 1, 1, QtCore.Qt.AlignRight|QtCore.Qt.AlignBottom)
        self.Scoring_Layout = QtWidgets.QVBoxLayout()
        self.Scoring_Layout.setObjectName("Scoring_Layout")
        self.radioButton_ScoreClear = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_ScoreClear.setFont(font)
        self.radioButton_ScoreClear.setAutoFillBackground(False)
        self.radioButton_ScoreClear.setObjectName("radioButton_ScoreClear")
        self.Scoring_Layout.addWidget(self.radioButton_ScoreClear)
        self.radioButton_ScorePrecipitate = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_ScorePrecipitate.setFont(font)
        self.radioButton_ScorePrecipitate.setObjectName("radioButton_ScorePrecipitate")
        self.Scoring_Layout.addWidget(self.radioButton_ScorePrecipitate)
        self.radioButton_ScoreCrystal = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_ScoreCrystal.setFont(font)
        self.radioButton_ScoreCrystal.setObjectName("radioButton_ScoreCrystal")
        self.Scoring_Layout.addWidget(self.radioButton_ScoreCrystal)
        self.radioButton_ScorePhaseSep = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_ScorePhaseSep.setFont(font)
        self.radioButton_ScorePhaseSep.setObjectName("radioButton_ScorePhaseSep")
        self.Scoring_Layout.addWidget(self.radioButton_ScorePhaseSep)
        self.radioButton_ScoreOther = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_ScoreOther.setFont(font)
        self.radioButton_ScoreOther.setObjectName("radioButton_ScoreOther")
        self.Scoring_Layout.addWidget(self.radioButton_ScoreOther)
        self.gridLayout_2.addLayout(self.Scoring_Layout, 1, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_Timeline = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_Timeline.setMinimumSize(QtCore.QSize(121, 20))
        self.label_Timeline.setMaximumSize(QtCore.QSize(140, 20))
        self.label_Timeline.setObjectName("label_Timeline")
        self.horizontalLayout_3.addWidget(self.label_Timeline)
        self.label_CurrentWell = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_CurrentWell.setObjectName("label_CurrentWell")
        self.horizontalLayout_3.addWidget(self.label_CurrentWell)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 2, 1, 1)
        self.ImageViewer = QtWidgets.QScrollArea(self.verticalFrame)
        self.ImageViewer.setGeometry(QtCore.QRect(700, 10, 861, 631))
        self.ImageViewer.setWidgetResizable(True)
        self.ImageViewer.setObjectName("ImageViewer")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 859, 629))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.ImageViewer.setWidget(self.scrollAreaWidgetContents_3)
        self.horizontalLayout.addWidget(self.verticalFrame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1600, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuDisplay_Heat_Map = QtWidgets.QMenu(self.menuBar)
        self.menuDisplay_Heat_Map.setObjectName("menuDisplay_Heat_Map")
        self.menuShow_autoMARCO_Grid = QtWidgets.QMenu(self.menuDisplay_Heat_Map)
        self.menuShow_autoMARCO_Grid.setObjectName("menuShow_autoMARCO_Grid")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.openFile = QtWidgets.QAction(MainWindow)
        self.openFile.setStatusTip("")
        self.openFile.setObjectName("openFile")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.openDir = QtWidgets.QAction(MainWindow)
        self.openDir.setObjectName("openDir")
        self.actionQuit_2 = QtWidgets.QAction(MainWindow)
        self.actionQuit_2.setObjectName("actionQuit_2")
        self.actionDisplay_Heat_Map = QtWidgets.QAction(MainWindow)
        self.actionDisplay_Heat_Map.setObjectName("actionDisplay_Heat_Map")
        self.actionExport_to_PDF = QtWidgets.QAction(MainWindow)
        self.actionExport_to_PDF.setObjectName("actionExport_to_PDF")
        self.actionCalculate_Statistics = QtWidgets.QAction(MainWindow)
        self.actionCalculate_Statistics.setObjectName("actionCalculate_Statistics")
        self.actionShortcuts = QtWidgets.QAction(MainWindow)
        self.actionShortcuts.setObjectName("actionShortcuts")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAutomated_Annotation_MARCO = QtWidgets.QAction(MainWindow)
        self.actionAutomated_Annotation_MARCO.setObjectName("actionAutomated_Annotation_MARCO")
        self.actionautoMARCO_subwell_a = QtWidgets.QAction(MainWindow)
        self.actionautoMARCO_subwell_a.setObjectName("actionautoMARCO_subwell_a")
        self.actionautoMARCO_subwell_b = QtWidgets.QAction(MainWindow)
        self.actionautoMARCO_subwell_b.setObjectName("actionautoMARCO_subwell_b")
        self.actionautoMARCO_subwell_c = QtWidgets.QAction(MainWindow)
        self.actionautoMARCO_subwell_c.setObjectName("actionautoMARCO_subwell_c")
        self.actionautoMARCO_no_subwell = QtWidgets.QAction(MainWindow)
        self.actionautoMARCO_no_subwell.setObjectName("actionautoMARCO_no_subwell")
        self.actionAutoCrop = QtWidgets.QAction(MainWindow)
        self.actionAutoCrop.setObjectName("actionAutoCrop")
        self.menuFile.addAction(self.openFile)
        self.menuFile.addAction(self.openDir)
        self.menuFile.addAction(self.actionExport_to_PDF)
        self.menuFile.addAction(self.actionQuit_2)
        self.menuShow_autoMARCO_Grid.addAction(self.actionautoMARCO_subwell_a)
        self.menuShow_autoMARCO_Grid.addAction(self.actionautoMARCO_subwell_b)
        self.menuShow_autoMARCO_Grid.addAction(self.actionautoMARCO_subwell_c)
        self.menuShow_autoMARCO_Grid.addAction(self.actionautoMARCO_no_subwell)
        self.menuDisplay_Heat_Map.addAction(self.actionAutoCrop)
        self.menuDisplay_Heat_Map.addAction(self.actionAutomated_Annotation_MARCO)
        self.menuDisplay_Heat_Map.addAction(self.actionCalculate_Statistics)
        self.menuDisplay_Heat_Map.addAction(self.actionDisplay_Heat_Map)
        self.menuDisplay_Heat_Map.addAction(self.menuShow_autoMARCO_Grid.menuAction())
        self.menuHelp.addAction(self.actionShortcuts)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuDisplay_Heat_Map.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AMi Image Analysis for LCPB AMi version x.x.x"))
        self.PrepDate.setText(_translate("MainWindow", "----"))
        self.ProjectCode.setText(_translate("MainWindow", "----"))
        self.label_8.setText(_translate("MainWindow", "Project Code: "))
        self.label_7.setText(_translate("MainWindow", "Target name: "))
        self.label_6.setText(_translate("MainWindow", "Image date: "))
        self.TargetName.setText(_translate("MainWindow", "----"))
        self.ImageDate.setText(_translate("MainWindow", "----"))
        self.label_9.setText(_translate("MainWindow", "Plate name: "))
        self.PlateName.setText(_translate("MainWindow", "----"))
        self.label_10.setText(_translate("MainWindow", "Prep date: "))
        self.FilterBox.setTitle(_translate("MainWindow", "Filter"))
        self.radioButton_All.setText(_translate("MainWindow", "All"))
        self.radioButton_Crystal.setText(_translate("MainWindow", "Crystal"))
        self.radioButton_Clear.setText(_translate("MainWindow", "Clear"))
        self.radioButton_Other.setText(_translate("MainWindow", "Other"))
        self.radioButton_Precipitate.setText(_translate("MainWindow", "Precipitate"))
        self.radioButton_PhaseSep.setText(_translate("MainWindow", "Phase Separation"))
        self.radioButton_Unsorted.setText(_translate("MainWindow", "Unsorted"))
        self.label_ProjectDetails.setText(_translate("MainWindow", "Project Details"))
        self.label_2.setText(_translate("MainWindow", "Notes"))
        self.label_4.setText(_translate("MainWindow", "Drop Score"))
        self.pushButton_DisplayHeatMap.setText(_translate("MainWindow", "Display Heat Map"))
        self.pushButton_ExportToPDF.setText(_translate("MainWindow", "Export to PDF"))
        self.radioButton_ScoreClear.setText(_translate("MainWindow", "Clear"))
        self.radioButton_ScorePrecipitate.setText(_translate("MainWindow", "Precipitate"))
        self.radioButton_ScoreCrystal.setText(_translate("MainWindow", "Crystal"))
        self.radioButton_ScorePhaseSep.setText(_translate("MainWindow", "Phase Separation"))
        self.radioButton_ScoreOther.setText(_translate("MainWindow", "Other"))
        self.label_Timeline.setText(_translate("MainWindow", "Timeline for well :"))
        self.label_CurrentWell.setText(_translate("MainWindow", "------"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuDisplay_Heat_Map.setTitle(_translate("MainWindow", "Tools"))
        self.menuShow_autoMARCO_Grid.setTitle(_translate("MainWindow", "Show autoMARCO Results"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.openFile.setText(_translate("MainWindow", "Open File"))
        self.openFile.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.openDir.setText(_translate("MainWindow", "Open Directory"))
        self.openDir.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actionQuit_2.setText(_translate("MainWindow", "Quit"))
        self.actionQuit_2.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionDisplay_Heat_Map.setText(_translate("MainWindow", "Display Heat Map"))
        self.actionDisplay_Heat_Map.setShortcut(_translate("MainWindow", "Shift+H"))
        self.actionExport_to_PDF.setText(_translate("MainWindow", "Export to PDF"))
        self.actionExport_to_PDF.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionCalculate_Statistics.setText(_translate("MainWindow", "Calculate Statistics"))
        self.actionCalculate_Statistics.setShortcut(_translate("MainWindow", "Shift+S"))
        self.actionShortcuts.setText(_translate("MainWindow", "Shortcuts"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAutomated_Annotation_MARCO.setText(_translate("MainWindow", "Automated Annotation (MARCO)"))
        self.actionautoMARCO_subwell_a.setText(_translate("MainWindow", "autoMARCO subwell a"))
        self.actionautoMARCO_subwell_b.setText(_translate("MainWindow", "autoMARCO subwell b"))
        self.actionautoMARCO_subwell_c.setText(_translate("MainWindow", "autoMARCO subwell c"))
        self.actionautoMARCO_no_subwell.setText(_translate("MainWindow", "autoMARCO no subwell"))
        self.actionAutoCrop.setText(_translate("MainWindow", "AutoCrop"))
        self.actionAutoCrop.setShortcut(_translate("MainWindow", "Shift+C"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
