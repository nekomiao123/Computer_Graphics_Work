from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PnonCloseShape import *
import Pshape
import math
import pickle

class Pcurve(PnonCloseShape):
    def __init__(self, *args):
        super().__init__()
        self.shapeType = SH_CURVE
        self.changed = True
        self.isAdjusting = False
        self.pointArray = []
        self.rectArray = []
        if len(args) != 0:
            curve = args[0]
            self.pen = curve.pen
            self.isVisible = curve.isVisible
            self.isSelected = curve.isSelected
            self.isAdjusting = curve.isAdjusting
            self.changed = True
            self.shapeType = SH_CURVE
            self.pointArray = curve.pointArray
            self.gravity = curve.gravity
            self.rectArray = curve.rectArray
            self.path = curve.path

    def addPoint(self, point):
        if len(self.pointArray) == 0:   #添加第一个点
            self.pointArray.append(point)
            self.rectArray.append(QRect(point.x()-5, point.y()-5, 10, 10))
        elif len(self.pointArray) == 1:
            self.pointArray.append(self.pointArray[0])  #添加一个点作为贝塞尔曲线的两个控制顶点
            self.rectArray.append(QRect(self.pointArray[0].x()-5, self.pointArray[0].y()-5, 10, 10))
            self.pointArray.append(point)
            self.rectArray.append(QRect(point.x()-5, point.y()-5, 10, 10))
        else:
            self.pointArray.append(self.getRelativePoint(self.pointArray[-2], self.pointArray[-1]))
            #将贝塞尔曲线的第一个控制点设置在上一段曲线的第二个控制点与终点的连线的反向延长线上
            self.rectArray.append(QRect(self.pointArray[-1].x()-5, self.pointArray[-1].y()-5, 10, 10))
            self.pointArray.append(point)
            self.rectArray.append(QRect(point.x()-5, point.y()-5, 10, 10))
            self.pointArray.append(point)
            self.rectArray.append(QRect(point.x()-5, point.y()-5, 10, 10))
            #添加两次

        self.isAdjusting = True
        self.changed = True
        self.updatePath()
        '''for i in range(len(self.pointArray)):
            print (self.pointArray[i])
        print("    ")'''

    def getRelativePoint(self, ptSrc, ptOrg):
        pt = QPoint()
        pt = 2 * ptOrg - ptSrc
        return pt

    def clear(self):
        self.pointArray.clear()
        self.rectArray.clear()
        self.path = QPainterPath()
        self.changed = True

    def setLastContrlPoint(self, point):#设置最后一个控制点
        self.pointArray[-2] = point
        r = self.rectArray[-2]
        r.moveTo(point)
        self.rectArray[-2] = r
        self.updatePath()

    def ptOnControlPoint(self, point):
        return self.getCurrentContrlPoint(point)>=0

    def getContrlPoint(self, nlndex):
        if nlndex < 0 or nlndex >= len(self.pointArray):
            return QPoint()
        return self.pointArray[nlndex]

    def getCurrentContrlPoint(self, point):
        for i in range(len(self.pointArray)):
            if self.rectArray[i].contains(point) :
                return i
        return -1

    def getAllContrlRect(self):        
        return self.rectArray

    def ptOnShape(self, point):
        #用gravity/2的间隔在曲线上取点，然后用圆形范围判断
        len_ = self.path.length()
        p = QPointF()
        i = 0.0
        while(i < 1.0):
            p = self.path.pointAtPercent(i)
            p = p - point
            if QPointF.dotProduct(p, p) < self.gravity * self.gravity:
                return True
            if len_ == 0:
                return 
            i += self.gravity / (2 * len_)
            #沿曲线前进
        return False
    
    def isInRect(self, rect):
        return self.path.boundingRect().contains(QRectF(rect))

    def translate(self,size):
        if isinstance(size, QSize):
            size = QPoint(size.width(), size.height())
        self.pointArray=QPolygon(self.pointArray).translated(size)
        self.updatePath()

    def scaleM(self, S):
        self.pointArray = S.map(QPolygon(self.pointArray))
        self.updatePath()

    def rotateM(self, R):
        self.pointArray = R.map(QPolygon(self.pointArray))
        self.updatePath()

    def flipM(self, F):
        self.pointArray = F.map(QPolygon(self.pointArray))
        self.updatePath()

    def adjust(self, point, nIndex):
        r = QRect()
        lenth = 0.0
        realpoint, p1, p2 = QPoint()
        if nIndex == 0 or nIndex == len(self.pointArray) - 1 or nIndex == len(self.pointArray) - 2:
            self.pointArray.replace(nIndex, point)
            r = self.rectArray[nIndex]
            r.moveCenter(point)
            self.rectArray.replace(nIndex, r)
        elif nIndex % 3 == 1:
            p1 = self.pointArray[nIndex] - self.pointArray[nIndex+1]
            p2 = point - self.pointArray[nIndex+1]
            lenth = QPointF.dotProduct(p1, p2) / math.sqrt(QPointF.dotProduct(p1, p2))
            if lenth < 10:
                lenth =10
            p2 = (lenth / math.sqrt(QPointF.dotProduct(p1, p1))) * p1
            realpoint = p2 + self.pointArray[nIndex+1]
            self.pointArray.replace(nIndex, realpoint)
            r = self.rectArray[nIndex]
            r.moveCenter(realpoint)
            self.rectArray.replace(nIndex, r)
        elif nIndex % 3 == 2:
            p1 = point - self.pointArray[nIndex]
            self.pointArray.replace(nIndex - 1, self.pointArray[nIndex - 1] + p1)
            self.pointArray.replace(nIndex + 1, self.pointArray[nIndex + 1] + p1)
            self.pointArray.replace(nIndex, point)
            r = self.rectArray[nIndex]
            r.moveCenter(point)
            self.rectArray.replace(nIndex, r)
            r.moveCenter(self.pointArray[nIndex - 1])
            self.rectArray.replace(nIndex - 1, r)
            r.moveCenter(self.pointArray[nIndex + 1])
            self.rectArray.replace(nIndex + 1, r)
        else:
            p1 = self.pointArray[nIndex] - self.pointArray[nIndex - 1];
            p2 = point - self.pointArray[nIndex - 1];
            length = QPointF.dotProduct(p1, p2) / math.sqrt(QPointF.dotProduct(p1, p1))
            if length < 10:
                length = 10
            p2 = (length / math.sqrt(QPointF.dotProduct(p1, p1)))*p1
            realpoint = p2 + self.pointArray[nIndex - 1]
            self.pointArray.replace(nIndex, realpoint)
            r = self.rectArray[nIndex]
            r.moveCenter(realpoint)
            self.rectArray.replace(nIndex, r)
        self.updatePath()

    def getChanged(self):
        return self.changed

    def setChanged(self, value):
        self.changed = value

    def getPointArrayLength(self):
        return len(self.pointArray)

    def updatePath(self):
        if len(self.pointArray) < 3:
            return
        path1 = QPainterPath()
        path1.moveTo(self.pointArray[0])
        path1.cubicTo(self.pointArray[1], self.pointArray[1], self.pointArray[2])
        for i in range(1, int((len(self.pointArray) + 2) / 3)):
            path1.cubicTo(self.pointArray[3 * i], self.pointArray[3 * i + 1], self.pointArray[3 * i + 2])
            #三个一组，不包括开头和结尾
        self.path = path1

    # 序列化函数
    def serialize(self, data):
        super().serialize(data)
        if len(self.pointArray)!=0:
            for i in range(self.pointArray):
                data<<QPoint(self.pointArray[i])
        if len(self.rectArray)!=0:
            for i in range(self.rectArray):
                data<<QRect(self.rectArray)

    # 反序列化函数
    def desSerialize(self, data):
        point=None
        data >>point
        if isinstance(point,QPoint):
            self.pointArray.append(point)
        if isinstance(point,QRect):
            self.rectArray.append(point)

    # 左移<<
    def __lshift__(self, data, pshape):
        pshape.serialize(data)
        return data

    # 右移>>
    def __rshift__(self, data, pshape):
        pshape.disSerialize(data)
        return data

