from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5.Qt
from PCloseShape import *
import math

FT_HORIZONTAL = 0  # 水平翻转
FT_VERTICAL = 1  # 垂直翻转

SH_LINE = 0  # 直线图形
SH_POLYLINE = 1  # 折线图形
SH_CURVE = 2  # 曲线
SH_POLYGON = 3  # 多边形
SH_RECT = 4  # 矩形
SH_ELLIPSE = 5  # 椭圆


class Ppolygon(PCloseShape):
    def __init__(self, *args):
        super().__init__()
        # 相当于无参数的构造函数
        self.shapeType = SH_POLYGON
        self.finished = False
        self.polygon = []
        # 相当于带参的构造函数
        if len(args) != 0:
            poly = args[0]
            self.polygon = poly.polygon
            self.pen = poly.pen
            self.brush = poly.brush
            self.path = poly.path
            self.isVisible = poly.isVisible
            self.isAdjusting = poly.isAdjusting
            self.isSelected = poly.isSelected
            self.gravity = poly.gravity

    # 序列化函数
    def serialize(self, data):
        super().serialize(data)
        if len(self.polygon)==0:
            print("我没有")
        else:
            for i in range(len(self.polygon)):
                data << QPoint(self.polygon[i])

    # 反序列化函数
    def desSerialize(self, data):
        super().desSerialize(data)
        polygon=None
        data >> polygon
        if isinstance(polygon,QPoint):
            self.polygon.append(polygon)

    # 复合赋值位相关运算符重载
    # other对应QDataStream类型，pshape对应Pshape类型
    # 左移<<
    def __lshift__(self, other, pshape):
        pshape.serialize(other)
        return other

    # 右移>>
    def __rshift__(self, other, pshape):
        pshape.disSerialize(other)
        return other

    def updatePath(self):
        path1 = QPainterPath()
        path1.addPolygon(QPolygonF(self.polygon))
        if self.finished:
            path1.lineTo(self.polygon[0])
        self.path = path1

    def addPoint(self, point):
        self.polygon.append(point)
        self.updatePath()

    def setLastPoint(self, point):
        self.polygon[-1] = point
        self.updatePath()

    def clear(self):
        self.polygon.clear()
        self.updatePath()

    def getPointCount(self):
        return len(self.polygon)

    def ptOnShape(self, point):
        if self.brush.style() != Qt.NoBrush:
            return self.ptInShape(point)
        # 只要点在其中一条线段的引力场范围内，就认为它在多边形上
        for i in range(len(self.polygon)):
            if self.ptOnLine(self.polygon[i], self.polygon[(i + 1) % len(self.polygon)], point):
                return True
        return False

    def ptInShape(self, point):
        return self.path.contains(point)

    def isInRect(self, rect):
        return rect.contains(self.path.boundingRect().toRect())

    def translate(self, size):
        self.polygon = QPolygon(self.polygon).translated(size)
        self.updatePath()

    def scaleM(self, S):
        self.polygon = S.map(QPolygon(self.polygon))
        self.updatePath()

    def rotateM(self, R):
        self.polygon = R.map(QPolygon(self.polygon))
        self.updatePath()

    def flipM(self, F):
        self.polygon = F.map(QPolygon(self.polygon))
        self.updatePath()

    # 注意，这里有点不一样，不知道为啥
    def getPolygon(self):
        return self.polygon

    def setPolygon(self, value):
        self.polygon = value
        self.updatePath()

    def setFinished(self, value):
        self.finished = value
        self.updatePath()

