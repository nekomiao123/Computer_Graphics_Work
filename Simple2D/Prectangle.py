from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5.Qt
from PCloseShape import *
from math import *

FT_HORIZONTAL = 0  # 水平翻转
FT_VERTICAL = 1  # 垂直翻转

SH_LINE = 0  # 直线图形
SH_POLYLINE = 1  # 折线图形
SH_CURVE = 2  # 曲线
SH_POLYGON = 3  # 多边形
SH_RECT = 4  # 矩形
SH_ELLIPSE = 5  # 椭圆


class Prectangle(PCloseShape):
    def __init__(self, *args):
        super().__init__()
        # 相当于无参数的构造函数
        self.shapeType = SH_RECT
        self.rect = QRect()
        # 相当于带参的构造函数
        if len(args) != 0:
            rect1 = args[0]  # args是一个tuple
            self.shapeType = rect1.shapeType
            self.rect = rect1.rect
            self.pen = rect1.pen
            self.brush = rect1.brush
            self.isVisible = rect1.isVisible
            self.isAdjusting = rect1.isAdjusting
            self.isSelected = rect1.isSelected
            self.path = rect1.path

    # 序列化函数
    def serialize(self, data):
        super().serialize(data)
        data << QRect(self.rect)
    # 反序列化函数
    def desSerialize(self, data):
        super().desSerialize(data)
        data >> self.rect

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

    # 用QPoint设置的setRect
    def setRectQ(self, topleft, bottomright):
        self.rect.setTopLeft(topleft)
        self.rect.setBottomRight(bottomright)
        self.updatePath()

    def setRect(self, x1, y1, x2, y2):
        self.setRectQ(QPoint(x1, y1), QPoint(x2, y2))
        self.updatePath()

    def ptInShape(self, point):
        return self.rect.contains(point)

    def setTopLeft(self, topleft):
        self.rect.setTopLeft(topleft)
        self.updatePath()

    def setBottomRight(self, bottomright, isShapely):
        if isShapely:
            dx = bottomright.x() - self.rect.x()
            dy = bottomright.y() - self.rect.y()
            # 设置正方形的边长为矩形的最长边
            if abs(dx) > abs(dy):
                nMaxLength = dx
            else:
                nMaxLength = dy
            self.rect.setWidth(nMaxLength)
            self.rect.setHeight(nMaxLength)
            return

        self.rect.setBottomRight(bottomright)
        self.updatePath()

    def getRect(self):
        return self.rect

    def getTopLeft(self):
        return self.rect.topLeft()

    def getBottomRight(self):
        return self.rect.bottomRight()

    def ptOnShape(self, point):
        if self.brush.style() != Qt.NoBrush:
            return self.rect.contains(point)
        r1 = QRect()
        r2 = QRect()
        r1.setTopLeft(QPoint(self.rect.x() - self.gravity, self.rect.y() - self.gravity))
        r1.setBottomRight(QPoint(self.rect.right() + self.gravity, self.rect.bottom() + self.gravity))
        r2.setTopLeft(QPoint(self.rect.x() + self.gravity, self.rect.y() + self.gravity))
        r2.setBottomRight(QPoint(self.rect.right() - self.gravity, self.rect.bottom() - self.gravity))

        return r1.contains(point) ^ r2.contains(point)

    def isInRect(self, Rect):
        return Rect.contains(self.rect)

    def translate(self, point):
        self.rect = QRect(self.rect).translated(point)
        #self.rect.translate(point)
        self.updatePath()

    def scaleM(self, S):
        self.rect = S.mapRect(self.rect)
        self.updatePath()

    def rotate(self, dTheta, ptOrigin):
        pt = [QPoint() for i in range(4)]
        pt[0] = self.rect.center()
        pt[1] = QPoint(ptOrigin.x() + ptOrigin.y() - pt[0].y(), ptOrigin.y() + pt[0].x() - ptOrigin.x())
        pt[2] = QPoint(2 * ptOrigin.x() - pt[0].x(), 2 * ptOrigin.y() - pt[0].y())
        pt[3] = QPoint(ptOrigin.x() - ptOrigin.y() + pt[0].y(), ptOrigin.y() - pt[0].x() + ptOrigin.x())

        center = QPoint()

        if fabs(dTheta) < pi / 4:
            center = pt[0]
        elif fabs(dTheta) > pi / 4 and fabs(dTheta) < 3 * pi / 4:
            center = pt[1]
        elif fabs(dTheta) > 3 * pi / 4:
            center = pt[2]
        else:
            center = pt[3]

        hw = self.rect.width() / 2
        hh = self.rect.height() / 2

        if fabs(dTheta) > pi / 4 and fabs(dTheta) < 3 * pi / 4:
            self.rect.setRect(center.x() - hh, center.y() - hw, 2 * hh, 2 * hw)
        else:
            self.rect.translate(center - self.rect.center())
        self.updatePath()

    def flipM(self, F):
        self.rect = F.mapRect(self.rect)
        self.updatePath()

    def updatePath(self):
        self.path = QPainterPath()
        if self.shapeType == SH_RECT:
            self.path.addRect(QRectF(self.rect))
        else:
            self.path.addEllipse(QRectF(self.rect))




