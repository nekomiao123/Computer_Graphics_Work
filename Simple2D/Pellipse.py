from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5.Qt
from PCloseShape import *
import math
FT_HORIZONTAL  = 0	#水平翻转
FT_VERTICAL	   = 1	#垂直翻转

SH_LINE        = 0       #直线图形
SH_POLYLINE    = 1       #折线图形
SH_CURVE       = 2       #曲线
SH_POLYGON     = 3       #多边形
SH_RECT        = 4       #矩形
SH_ELLIPSE     = 5       #椭圆

class Pellipse(PCloseShape):
    def __init__(self,*args):
        super().__init__()
        #相当于无参数的构造函数
        if len(args)==0:
            self.shapeType=SH_ELLIPSE
        #相当于带参的构造函数
        else:
            ellipse = args[0]
            self.pen=ellipse.pen
            self.brush=ellipse.brush
            self.path=ellipse.path
            self.rect=ellipse.rect
            self.shapeType=ellipse.shapeType
            self.isVisible=ellipse.isVisible
            self.isAdjusting=ellipse.isAdjusting
            self.isSelected=ellipse.isSelected
            self.gravity=ellipse.gravity

    def ptOnShape(self,point):
        if self.brush.Style()!=Qt.NoBrush:
            return self.path.contains(point)
        path1 = QPainterPath()
        path2 = QPainterPath()

        path1.addEllipse(QRect(QPoint(self.getRect().left()-self.gravity,self.getRect().top()-self.gravity),QPoint(self.getRect().right()+self.gravity,self.getRect().bottom()+self.gravity)))
        path2.addEllipse(QRect(QPoint(self.getRect().left()+self.gravity,self.getRect().top()+self.gravity),QPoint(self.getRect().right()-self.gravity,self.getRect().bottom()-self.gravity)))
        return path1.contains(point)^path2.contains(point)#判断点是否在两个椭圆形成的圆环内

    def ptInShape(self,point):
        return self.path.contains(point)
    

