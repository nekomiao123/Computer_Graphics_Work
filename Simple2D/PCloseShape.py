from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5.Qt
from Pshape import *


class PCloseShape(Pshape):
    def __init__(self):
        super().__init__()
        self.brush = QBrush()
        self.brush.setStyle(Qt.NoBrush)

    def draw(self, pt):
        if not self.IsVisible:
            return
        pt.save()
        if self.IsSelected:
            pt.setPen(Pshape.penBlueDot)
        else:
            pt.setPen(self.pen)
        pt.setBrush(self.brush)
        pt.drawPath(self.path)
        pt.restore()

    def drawFrame(self, pt):
        pt.save()
        pt.setPen(Pshape.penBlueSolid)
        pt.drawPath(self.path)
        pt.restore()

    def getBrush(self):
        return self.brush
