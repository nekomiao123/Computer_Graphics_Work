from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5.Qt
import math

FT_HORIZONTAL = 0  # 水平翻转
FT_VERTICAL = 1  # 垂直翻转

SH_LINE = 0  # 直线图形
SH_POLYLINE = 1  # 折线图形
SH_CURVE = 2  # 曲线
SH_POLYGON = 3  # 多边形
SH_RECT = 4  # 矩形
SH_ELLIPSE = 5  # 椭圆


class Pshape(QObject):
    # 利用python的类的成员变量来实现C++中静态变量的效果,但这种只能使用类来访问
    penBlueDot = QPen(Qt.blue, 2, Qt.DotLine)  # 蓝色虚线画笔
    penBlueSolid = QPen(Qt.blue, 2, Qt.SolidLine)  # 蓝色实线画笔
    def __init__(self):
        super(Pshape,self).__init__()
        self.isVisible = False  # 是否可见
        self.isSelected = False  # 是否被选中
        self.isAdjusting = False  # 是否处于被调整状态
        self.shapeType = 0  # 图形类型
        self.gravity = 10  # 引力场强度
        self.pen = QPen()  # 保存线宽，颜色，线型等属性
        self.path = QPainterPath()  # 用于显示的数据结构

    # 序列化函数
    def serialize(self, data):
        data.writeInt(self.shapeType)
        data << self.pen

    # 反序列化函数
    def desSerialize(self, data):
        self.shapeType = data.readInt()
        data >> self.pen
        

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

    # 定义虚函数,参数可以和后面真正实现的函数不一样
    # 判断本图形是否在给定矩形内
    def isInRect(self):
        pass

    # 判断给定点是否在图形内部
    def ptInShape(self):
        pass

    # 判断给定点是否在图形边上
    def ptOnShape(self):
        pass

    # 获取控制点
    def getContrlPoint(self):
        pass

    # 获取当前控制点
    def getCurrentContrlPoint(self):
        pass

    # 获取当前控制点2
    def getCurrentContrlPoint2(self):
        pass

    def ptOnContrlPoint(self):
        pass

    def adjust(self):
        pass

    # 用给定点和类型进行翻转
    def flip(self, nType, ptOrigin):
        a = QTransform(1, 0, 0, 1, 0, 0)
        b = a
        a.translate(-ptOrigin.x(), -ptOrigin.y())
        if nType == FT_HORIZONTAL:
            a = a * QTransform(-1, 0, 0, 1, 0, 0)
        else:
            a = a * QTransform(1, 0, 0, -1, 0, 0)
        b.translate(ptOrigin.x(), ptOrigin.y())
        a = a * b
        self.flipM(a)

    # 根据给定矩阵进行翻转
    def filpM(self, F):
        pass

    # 以给定点为旋转中心旋转给定角度
    def rotate(self, dTheta, ptOrigin):
        '''R00 = math.cos(dTheta)
        R01 = -math.sin(dTheta)	
        R02 = ptOrigin.x()*(1-math.cos(dTheta))+ptOrigin.y()*math.sin(dTheta)
        R10 = math.sin(dTheta)
        R11 = math.cos(dTheta)
        R12 = ptOrigin.y()*(1-math.cos(dTheta))-ptOrigin.x()*math.sin(dTheta)
        a = QTransform(R00,R01,R02, R10,R11,R12, 0,0,1)
        '''
        a = QTransform(1,0,0, 0,1,0, 0,0,1)
        b = a
        c = a
        b.translate(-ptOrigin.x(), -ptOrigin.y())
        c.rotate(dTheta)
        bt = b * c
        a.translate(ptOrigin.x(), ptOrigin.y())
        b = bt * a
        self.rotateM(b)

    # 根据给定矩阵进行旋转
    def rotateM(self, R):
        pass

    # 以给定的缩放中心按比例进行缩放
    def scale(self, sx, sy, ptOrigin):
        a = QTransform(1, 0, 0, 1, 0, 0)
        b = a
        c = a
        b.translate(-ptOrigin.x(), -ptOrigin.y())
        c.scale(sx, sy)
        b = b * c
        a.translate(ptOrigin.x(), ptOrigin.y())
        b = b * a
        self.scaleM(b)

    # 根据给定矩阵进行缩放
    def scaleM(self, S):
        pass

    # 根据给定大小进行平移,python的特性决定了只需要写了一个
    def translate(self,t):
        pass

    # 绘制图形
    def draw(self, pt):
        if not self.isVisible:
            return
        pt.save()
        if self.isSelected:
            pt.setPen(Pshape.penBlueDot)
        else:
            pt.setPen(self.pen)
        pt.drawPath(self.path)
        pt.restore()

    # 绘制图形边框
    def drawFrame(self, pt):
        pt.save()
        pt.setPen(Pshape.penBlueSolid)
        pt.drawPath(self.path)
        pt.restore()

    # 更新路径
    def updatePath(self):
        pass

    def setGravity(self, value):
        self.gravity = value

    def ptOnLine(self, start, end, point):
        a = QPointF()  # 浮点数的QPoint
        b = QPointF()
        a = end - start
        b = point - start

        ab = QPointF.dotProduct(a, b)
        aa = QPointF.dotProduct(a, a)
        if (ab >= 0 and ab <= aa):
            btoa = b - ab * a / aa
            if QPointF.dotProduct(btoa, btoa) <= self.gravity * self.gravity:
                return True

        if QPointF.dotProduct(b, b) <= self.gravity * self.gravity * 4:
            return True

        b = point - end

        if QPointF.dotProduct(b, b) <= self.gravity * self.gravity * 4:
            return True
        return False

    def rectInRect(self, rect1, rect2):
        return rect1.intersected(rect2) == rect1

    def getBoundingRect(self):
        return self.path.boundingRect().toRect()
