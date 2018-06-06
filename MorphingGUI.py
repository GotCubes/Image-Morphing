# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MorphingGUI.ui'
#
# Created: Sat Jun  2 02:14:52 2018
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(940, 820)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gfxEnd = QtGui.QGraphicsView(self.centralwidget)
        self.gfxEnd.setEnabled(True)
        self.gfxEnd.setGeometry(QtCore.QRect(530, 50, 400, 300))
        self.gfxEnd.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gfxEnd.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gfxEnd.setObjectName("gfxEnd")
        self.dspEnd = QtGui.QLabel(self.centralwidget)
        self.dspEnd.setGeometry(QtCore.QRect(670, 360, 120, 17))
        self.dspEnd.setAlignment(QtCore.Qt.AlignCenter)
        self.dspEnd.setObjectName("dspEnd")
        self.gfxBlend = QtGui.QGraphicsView(self.centralwidget)
        self.gfxBlend.setGeometry(QtCore.QRect(270, 440, 400, 300))
        self.gfxBlend.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gfxBlend.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gfxBlend.setObjectName("gfxBlend")
        self.dspBlend = QtGui.QLabel(self.centralwidget)
        self.dspBlend.setGeometry(QtCore.QRect(410, 750, 120, 17))
        self.dspBlend.setAlignment(QtCore.Qt.AlignCenter)
        self.dspBlend.setObjectName("dspBlend")
        self.btnBlend = QtGui.QPushButton(self.centralwidget)
        self.btnBlend.setEnabled(False)
        self.btnBlend.setGeometry(QtCore.QRect(425, 780, 90, 27))
        self.btnBlend.setObjectName("btnBlend")
        self.dspAlpha = QtGui.QLabel(self.centralwidget)
        self.dspAlpha.setGeometry(QtCore.QRect(10, 395, 40, 17))
        self.dspAlpha.setAlignment(QtCore.Qt.AlignCenter)
        self.dspAlpha.setObjectName("dspAlpha")
        self.txtAlpha = QtGui.QLineEdit(self.centralwidget)
        self.txtAlpha.setEnabled(False)
        self.txtAlpha.setGeometry(QtCore.QRect(880, 390, 50, 27))
        self.txtAlpha.setMaximumSize(QtCore.QSize(50, 27))
        self.txtAlpha.setAlignment(QtCore.Qt.AlignCenter)
        self.txtAlpha.setReadOnly(True)
        self.txtAlpha.setObjectName("txtAlpha")
        self.sliAlpha = QtGui.QSlider(self.centralwidget)
        self.sliAlpha.setEnabled(False)
        self.sliAlpha.setGeometry(QtCore.QRect(60, 390, 810, 24))
        self.sliAlpha.setMaximum(20)
        self.sliAlpha.setPageStep(10)
        self.sliAlpha.setProperty("value", 0)
        self.sliAlpha.setOrientation(QtCore.Qt.Horizontal)
        self.sliAlpha.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sliAlpha.setTickInterval(2)
        self.sliAlpha.setObjectName("sliAlpha")
        self.dspMin = QtGui.QLabel(self.centralwidget)
        self.dspMin.setGeometry(QtCore.QRect(60, 420, 20, 17))
        self.dspMin.setAlignment(QtCore.Qt.AlignCenter)
        self.dspMin.setObjectName("dspMin")
        self.dspMax = QtGui.QLabel(self.centralwidget)
        self.dspMax.setGeometry(QtCore.QRect(850, 420, 20, 17))
        self.dspMax.setAlignment(QtCore.Qt.AlignCenter)
        self.dspMax.setObjectName("dspMax")
        self.gfxStart = QtGui.QGraphicsView(self.centralwidget)
        self.gfxStart.setGeometry(QtCore.QRect(10, 50, 400, 300))
        self.gfxStart.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gfxStart.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gfxStart.setObjectName("gfxStart")
        self.dspStart = QtGui.QLabel(self.centralwidget)
        self.dspStart.setGeometry(QtCore.QRect(150, 360, 120, 17))
        self.dspStart.setAlignment(QtCore.Qt.AlignCenter)
        self.dspStart.setObjectName("dspStart")
        self.btnStart = QtGui.QPushButton(self.centralwidget)
        self.btnStart.setGeometry(QtCore.QRect(10, 10, 165, 27))
        self.btnStart.setObjectName("btnStart")
        self.chkTriangles = QtGui.QCheckBox(self.centralwidget)
        self.chkTriangles.setEnabled(False)
        self.chkTriangles.setGeometry(QtCore.QRect(410, 360, 125, 22))
        self.chkTriangles.setObjectName("chkTriangles")
        self.btnEnd = QtGui.QPushButton(self.centralwidget)
        self.btnEnd.setGeometry(QtCore.QRect(526, 12, 158, 27))
        self.btnEnd.setObjectName("btnEnd")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.dspEnd.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Ending Image</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.dspBlend.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Blending Image</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBlend.setText(QtGui.QApplication.translate("MainWindow", "Blend", None, QtGui.QApplication.UnicodeUTF8))
        self.dspAlpha.setText(QtGui.QApplication.translate("MainWindow", "Alpha", None, QtGui.QApplication.UnicodeUTF8))
        self.txtAlpha.setText(QtGui.QApplication.translate("MainWindow", "0.0", None, QtGui.QApplication.UnicodeUTF8))
        self.dspMin.setText(QtGui.QApplication.translate("MainWindow", "0.0", None, QtGui.QApplication.UnicodeUTF8))
        self.dspMax.setText(QtGui.QApplication.translate("MainWindow", "1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.dspStart.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Starting Image</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.btnStart.setText(QtGui.QApplication.translate("MainWindow", "Load Starting Image ...", None, QtGui.QApplication.UnicodeUTF8))
        self.chkTriangles.setText(QtGui.QApplication.translate("MainWindow", "Show Triangles", None, QtGui.QApplication.UnicodeUTF8))
        self.btnEnd.setText(QtGui.QApplication.translate("MainWindow", "Load Ending Image ...", None, QtGui.QApplication.UnicodeUTF8))

