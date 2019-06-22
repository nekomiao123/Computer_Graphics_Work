from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PnonCloseShape import *
import Pshape
import math
import pickle

class Ppoliline(PnonCloseShape):
    def __init__(self, *args):
        super().__init__()
        self.pointArray = []
        self.shapeType = SH_POLYLINE
        if len(args) != 0:
            polyline = args[0]
            self.pointArray = polyline.pointArray
            self.pen = polyline.pen
            self.path = polyline.path
            self.isSelected = polyline.isSelected
            self.isVisible = polyline.isVisible
            self.isAdjusting = polyline.isAdjusting
            self.gravity = polyline.gravity


    # 序列化函数
    def serialize(self, data):
        super().serialize(data)
        if len(self.pointArray)==0:
            print("a")
        else:
            for i in range(len(self.pointArray)):
                data << QPoint(self.pointArray[i])

    # 反序列化函数
    def desSerialize(self, data):
        #这里注意一下：
        point=None
        data >>point
        if isinstance(point,QPoint):
            self.pointArray.append(point)
        # 复合赋值位相关运算符重载

    # 左移<<
    def __lshift__(self, data, pshape):
        pshape.serialize(data)
        return data

    # 右移>>
    def __rshift__(self, data, pshape):
        pshape.disSerialize(data)
        return data

    def getPointArray(self):
        return self.pointArray

    def addPoint(self,point):
        self.pointArray.append(point)
        self.updatePath()

    def setLastPoint(self,point):
        self.pointArray[-1]=point
        self.updatePath()

    def clear(self):
        self.pointArray.clear()
        self.updatePath()

    def getPointCount(self):
        return len(self.pointArray)

    def ptOnShape(self, point):
        for i in range(1,len(self.pointArray)):
            if self.ptOnLine(self.pointArray[i-1],self.pointArray[i],point):
                return True
        return False

    def isInRect(self, rect):
        return rect.contains(self.path.boundingRect().toRect())

    def translate(self, size):
        self.pointArray = QPolygon(self.pointArray).translated(size)
        self.updatePath()

    def scaleM(self, S):
        self.pointArray = S.map(QPolygon(self.pointArray))
        self.updatePath()

    def rotateM(self, R):
        self.pointArray=R.map(QPolygon(self.pointArray))
        self.updatePath()

    def flipM(self, F):
        self.pointArray = F.map(QPolygon(self.pointArray))
        self.updatePath()

    
    def updatePath(self):
        path1 = QPainterPath()
        if len(self.pointArray)!=0:
            path1.moveTo(QPointF(self.pointArray[0]))
            for i in range(1, len(self.pointArray)):
                path1.lineTo(QPointF(self.pointArray[i]))
            self.path = path1
        