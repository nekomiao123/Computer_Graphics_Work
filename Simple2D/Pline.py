from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PnonCloseShape import *
import Pshape
import math
import pickle

class Pline(PnonCloseShape):
    def __init__(self, *args):
        super(Pline,self).__init__()
        self.shapeType = SH_LINE
        self.l = QLine()
        if len(args) != 0:
            line = args[0]
            self.l = line.l
            self.shapeType = SH_LINE
            self.pen = line.pen
            self.path = line.path
            self.isSelected = line.isSelected
            self.isVisible = line.isVisible
            self.isAdjusting = line.isAdjusting
            self.gravity = line.gravity

    # 序列化函数
    def serialize(self, data):
        super().serialize(data)
        data << self.l

    # 反序列化函数
    def desSerialize(self, data):
        data >> self.l
        # 复合赋值位相关运算符重载
        # other对应QDataStream类型，pshape对应Pshape类型

    # 左移<<
    def __lshift__(self, data, pshape):
        pshape.serialize(data)
        return data

    # 右移>>
    def __rshift__(self, data, pshape):
        pshape.disSerialize(data)
        return data

    def getLine(self):
        return self.l

    def setLine(self, start, end):
        self.l.setPoints(start, end)
        self.updatePath()

    def setStart(self, start):
        self.l.setP1(start)
        self.l.setP2(start)
        self.updatePath()

    def setEnd(self, end, isDriection):
        if(isDriection):
            stoe = end-self.l.p1()
            v = []
            v.append(QPointF(0.7071, 0.7071))
            v.append(QPointF(0.7071, -0.7071))
            v.append(QPointF(-0.7071, 0.7071))
            v.append(QPointF(-0.7071, -0.7071))
            v.append(QPointF(1, 0))
            v.append(QPointF(0, 1))
            v.append(QPointF(-1, 0))
            v.append(QPointF(0, -1))
            for i in range(8):
                if(QPointF.dotProduct(stoe, v[i]) / math.sqrt(QPointF.dotProduct(stoe, stoe)) > 0.91388):
                    self.l.setP2((v[i]*QPointF.dotProduct(stoe,v[i])).toPoint()+self.l.p1())
                    self.updatePath()
                    return
        self.l.setP2(end)
        self.updatePath()

    def ptOnShape(self, point):
        return self.ptOnLine(self.l.p1(), self.l.p2(), point)

    def isInRect(self, rect):
        return rect.contains(self.l.p1()) and rect.contains(self.l.p2())

    def translate(self, size):
        if isinstance(size, QSize):
            size = QPoint(size.width(), size.height())
        self.l = QLine(self.l)
        self.l.translate(size)
        self.updatePath()

    def scaleM(self, S):
        self.l = S.map(self.l)
        self.updatePath()

    def rotateM(self, R):
        self.l = R.map(self.l)
        #print(self.l)
        self.updatePath()

    def flipM(self, F):
        self.l = F.map(self.l)
        self.updatePath()

    def updatePath(self):
        path1 = QPainterPath()
        path1.moveTo(self.l.p1())
        path1.lineTo(self.l.p2())
        self.path = path1
