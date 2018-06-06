import sys
from PySide.QtCore import *
from PySide.QtGui import *
from MorphingGUI import *
from Morphing import *
import os
import imageio
import numpy as np
from scipy import spatial

class MorphingApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MorphingApp, self).__init__(parent)
        self.setupUi(self)

        # Helper members.
        self.startScene = QGraphicsScene()
        self.endScene = QGraphicsScene()
        self.radius = 6
        self.alpha = 0.0
        self.startSet = False
        self.endSet = False
        self.hasPresetPoints = False
        self.hasCustomPoints = False
        self.hasPoints = False
        self.state = 'INIT'
        self.blends = [QGraphicsScene(), QGraphicsScene(), QGraphicsScene(), QGraphicsScene(), QGraphicsScene(), QGraphicsScene(), QGraphicsScene(),
                       QGraphicsScene(), QGraphicsScene(), QGraphicsScene(), QGraphicsScene(), QGraphicsScene(), QGraphicsScene(), QGraphicsScene(),
                       QGraphicsScene(), QGraphicsScene(), QGraphicsScene(), QGraphicsScene(), QGraphicsScene(), QGraphicsScene(), QGraphicsScene()]

        # Signal functionality.
        self.gfxStart.setScene(self.startScene)
        self.gfxStart.mousePressEvent = self.setStartPoint
        self.gfxEnd.setScene(self.endScene)
        self.gfxEnd.mousePressEvent = self.setEndPoint
        self.btnStart.clicked.connect(self.loadStartImage)
        self.btnEnd.clicked.connect(self.loadEndImage)
        self.chkTriangles.stateChanged.connect(self.checkTriangles)
        self.sliAlpha.valueChanged.connect(self.changeAlpha)
        self.btnBlend.clicked.connect(self.blend)
        self.keyPressEvent = self.rewindPoint
        self.mousePressEvent = self.exitSelection

    def loadStartImage(self):
        # Get image file path.
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open Start Image ...', filter="Picture Files (*.jpg *.png)")
        if not filePath: return

        # Initialize scene and graphics.
        self.startImage = imageio.imread(filePath)
        self.startScene.clear()
        self.startScene.addPixmap(QPixmap(filePath))

        # Determine existance of point file.
        self.startFile = filePath + '.txt'
        if os.path.isfile(self.startFile):
            # Add correspondences from file.
            pen = QPen(QtCore.Qt.red)
            brush = QBrush(QtCore.Qt.red)
            self.startPoints = np.loadtxt(self.startFile)
            for x, y in self.startPoints:
                self.startScene.addEllipse(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2, pen, brush)
            self.hasPresetPoints = True
            self.hasCustomPoints = False
            self.hasPoints = True
        else:
            open(self.startFile, 'w').close()
            self.startPoints = None
            self.hasPresetPoints = False
            self.hasCustomPoints = False
            self.hasPoints = False

        # Update UI status.
        self.gfxStart.fitInView(self.startScene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
        self.startSet = True
        if self.startSet and self.endSet:
            self.chkTriangles.setEnabled(True)
            self.sliAlpha.setEnabled(True)
            self.txtAlpha.setEnabled(True)
            self.gfxBlend.setEnabled(True)
            self.btnBlend.setEnabled(True)
            self.state = 'IDLE'

            # Update triangulation.
            if self.chkTriangles.isChecked():
                self.chkTriangles.setChecked(False)
                self.chkTriangles.setChecked(True)

    def loadEndImage(self):
        # Get image file path.
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open End Image ...', filter="Picture Files (*.jpg *.png)")
        if not filePath: return

        # Initialize scene and graphics.
        self.endImage = imageio.imread(filePath)
        self.endScene.clear()
        self.endScene.addPixmap(QPixmap(filePath))

        # Determine existance of point file.
        self.endFile = filePath + '.txt'
        if os.path.isfile(self.endFile):
            # Add correspondences from file.
            pen = QPen(QtCore.Qt.red)
            brush = QBrush(QtCore.Qt.red)
            self.endFile = filePath + '.txt'
            self.endPoints = np.loadtxt(self.endFile)
            for x, y in self.endPoints:
                self.endScene.addEllipse(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2, pen, brush)
            self.hasPresetPoints = True
            self.hasCustomPoints = False
            self.hasPoints = True
        else:
            open(self.endFile, 'w').close()
            self.endPoints = None
            self.hasPresetPoints = False
            self.hasCustomPoints = False
            self.hasPoints = False

        # Update UI status.
        self.gfxEnd.fitInView(self.endScene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
        self.endSet = True
        if self.startSet and self.endSet:
            self.chkTriangles.setEnabled(True)
            self.sliAlpha.setEnabled(True)
            self.txtAlpha.setEnabled(True)
            self.gfxBlend.setEnabled(True)
            self.btnBlend.setEnabled(True)
            self.state = 'IDLE'

            # Update triangulation.
            if self.chkTriangles.isChecked():
                self.chkTriangles.setChecked(False)
                self.chkTriangles.setChecked(True)

    def checkTriangles(self):
        # Add triangles to scene.
        if self.chkTriangles.isChecked():
            if self.startPoints is not None and self.startPoints.shape[0] == self.endPoints.shape[0] and self.startPoints.shape[0] > 2:
                # Initialize triangle color and simplices.
                if self.hasPresetPoints and self.hasCustomPoints: pen = QPen(QtCore.Qt.cyan)
                elif self.hasPresetPoints: pen = QPen(QtCore.Qt.red)
                else: pen = QPen(QtCore.Qt.blue)

                self.simplices = spatial.Delaunay(self.startPoints).simplices
                for triangle in self.simplices:
                    # Draw triangles in start.
                    sTri = QPolygonF([QPointF(self.startPoints[triangle[0]][0], self.startPoints[triangle[0]][1]),
                                          QPointF(self.startPoints[triangle[1]][0], self.startPoints[triangle[1]][1]),
                                          QPointF(self.startPoints[triangle[2]][0], self.startPoints[triangle[2]][1])])
                    self.startScene.addPolygon(sTri, pen)

                    # Draw triangles in end.
                    dTri = QPolygonF([QPointF(self.endPoints[triangle[0]][0], self.endPoints[triangle[0]][1]),
                                          QPointF(self.endPoints[triangle[1]][0], self.endPoints[triangle[1]][1]),
                                          QPointF(self.endPoints[triangle[2]][0], self.endPoints[triangle[2]][1])])
                    self.endScene.addPolygon(dTri, pen)
        else:
            # Remove triangles from start.
            for item in self.startScene.items():
                if type(item) is QGraphicsPolygonItem:
                    self.startScene.removeItem(item)

            # Remove triangles from end.
            for item in self.endScene.items():
                if type(item) is QGraphicsPolygonItem:
                    self.endScene.removeItem(item)

    def changeAlpha(self):
        # Rescale and display alpha.
        print(self.sliAlpha.value())
        self.txtAlpha.setText(str(self.sliAlpha.value() / 20.0))
        self.gfxBlend.setScene(self.blends[self.sliAlpha.value()])

    def blend(self):
        # Check for valid triangulation.
        if self.startPoints is not None and self.startPoints.shape[0] > 2:
            # Initialize and blend.
            if self.startImage.ndim is 3: blender = ColorBlender(self.startImage, self.startPoints, self.endImage, self.endPoints)
            else: blender = Blender(self.startImage, self.startPoints, self.endImage, self.endPoints)

            self.blends[0].addPixmap(QPixmap(self.startFile[:-4]))
            for alpha in range(1, 20):
                # Save and display image.
                Image.fromarray(blender.getBlendedImage(alpha / 20.0)).save('temp.jpg')
                self.blends[alpha].addPixmap(QPixmap('temp.jpg'))
                os.remove('temp.jpg')
            self.blends[20].addPixmap(QPixmap(self.endFile[:-4]))
            self.changeAlpha()
            self.gfxBlend.fitInView(self.blends[0].itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

    def setStartPoint(self, event):
        if self.state == 'IDLE': # Set initial point.
            self.startPos = self.gfxStart.mapToScene(event.pos())
            if self.startScene.itemsBoundingRect().contains(self.startPos):
                pen = QPen(QtCore.Qt.green)
                brush = QBrush(QtCore.Qt.green)
                self.startScene.addEllipse(self.startPos.x() - self.radius, self.startPos.y() - self.radius, self.radius * 2, self.radius * 2, pen, brush)
                self.state = 'STARTSET'
        elif self.state == 'ENDSET': # Confirm points and start new point.
            self.confirmPoint()
            self.startPos = self.gfxStart.mapToScene(event.pos())
            if self.startScene.itemsBoundingRect().contains(self.startPos):
                pen = QPen(QtCore.Qt.green)
                brush = QBrush(QtCore.Qt.green)
                self.startScene.addEllipse(self.startPos.x() - self.radius, self.startPos.y() - self.radius, self.radius * 2, self.radius * 2, pen, brush)
                self.state = 'STARTSET'

    def setEndPoint(self, event):
        if self.state == 'STARTSET': # Set final point.
            self.endPos = self.gfxEnd.mapToScene(event.pos())
            if self.endScene.itemsBoundingRect().contains(self.endPos):
                pen = QPen(QtCore.Qt.green)
                brush = QBrush(QtCore.Qt.green)
                self.endScene.addEllipse(self.endPos.x() - self.radius, self.endPos.y() - self.radius, self.radius * 2, self.radius * 2, pen, brush)
                self.state = 'ENDSET'

    def rewindPoint(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            if self.state == 'STARTSET': # Remove point from start scene.
                self.startScene.removeItem(self.startScene.items()[0])
                self.state = 'IDLE'
            elif self.state == 'ENDSET': # Remove point from end scene.
                self.endScene.removeItem(self.endScene.items()[0])
                self.state = 'STARTSET'

    def exitSelection(self, event):
        if self.state == 'ENDSET': # Confirm points and exit.
            self.confirmPoint()
            self.state = 'IDLE'

    def confirmPoint(self):
        # Remove temporary points.
        self.startScene.removeItem(self.startScene.items()[0])
        self.endScene.removeItem(self.endScene.items()[0])

        # Draw confirmed points.
        pen = QPen(QtCore.Qt.blue)
        brush = QBrush(QtCore.Qt.blue)
        self.startScene.addEllipse(self.startPos.x() - self.radius, self.startPos.y() - self.radius, self.radius * 2, self.radius * 2, pen, brush)
        self.endScene.addEllipse(self.endPos.x() - self.radius, self.endPos.y() - self.radius, self.radius * 2, self.radius * 2, pen, brush)
        self.hasCustomPoints = True

        # Add confirmed points to lists.
        if self.hasPoints:
            self.startPoints = np.vstack((self.startPoints, [self.startPos.x(), self.startPos.y()]))
            self.endPoints = np.vstack((self.endPoints, [self.endPos.x(), self.endPos.y()]))
        else:
            self.startPoints = np.array([[self.startPos.x(), self.startPos.y()]])
            self.endPoints = np.array([[self.endPos.x(), self.endPos.y()]])
            self.hasPoints = True

        # Update triangulation.
        if self.chkTriangles.isChecked():
            self.chkTriangles.setChecked(False)
            self.chkTriangles.setChecked(True)

        # Write confirmed points to files.
        with open(self.startFile, 'w') as file:
            file.writelines([str(int(np.round(coord[0]))) + ' ' + str(int(np.round(coord[1]))) + '\n' for coord in self.startPoints.tolist()])
        with open(self.endFile, 'w') as file:
            file.writelines([str(int(np.round(coord[0]))) + ' ' + str(int(np.round(coord[1]))) + '\n' for coord in self.endPoints.tolist()])

    def resizeEvent(self, event):
        self.gfxStart.fitInView(self.startScene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
        self.gfxEnd.fitInView(self.endScene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
        self.gfxBlend.fitInView(self.blends[0].itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
        QMainWindow.resizeEvent(self, event)

if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = MorphingApp()

    currentForm.show()
    currentApp.exec_()
