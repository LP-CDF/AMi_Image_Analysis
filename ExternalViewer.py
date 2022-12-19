# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

__date__ = "14-05-2021"


class ViewerWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(882, 652)
        self.ImageViewer = QtWidgets.QScrollArea(Dialog)
        self.ImageViewer.setGeometry(QtCore.QRect(10, 10, 861, 601))
        font = QtGui.QFont()
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(12)
        self.ImageViewer.setFont(font)
        self.ImageViewer.setWidgetResizable(True)
        self.ImageViewer.setObjectName("ImageViewer")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 859, 629))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.ImageViewer.setWidget(self.scrollAreaWidgetContents_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))



class Window(QtWidgets.QDialog, ViewerWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        ui = ViewerWindow()
        self.setupUi(self)
        
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.view.wheelEvent = self.wheel_event
        self.ImageViewer.setWidget(self.view)
        
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
        w_pix, h_pix = self.pixmap.width(), self.pixmap.height()
        self.scene.clear()
        self.scene.setSceneRect(0, 0, w_pix, h_pix)
        self.scene.addPixmap(self.pixmap)
        self.view.setScene(self.scene)


    def wheel_event (self, event):
        '''based on https://vincent-vande-vyvre.developpez.com/tutoriels/pyqt/manipulation-images/'''
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