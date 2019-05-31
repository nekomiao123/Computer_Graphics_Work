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


     #序列化函数
    def serialize(self,data):
        super().serialize(data)
        data<<self.brush
    #反序列化函数
    def desSerialize(self,data):
        data>>self.brush
    #复合赋值位相关运算符重载
    #other对应QDataStream类型，pshape对应Pshape类型
    #左移<<
    def __lshift__(self, other,pshape):
        pshape.serialize(other)
        return other
    #右移>>
    def __rshift__(self, other,pshape):
        pshape.disSerialize(other)
        return other



    def draw(self,pt):
        if not self.isVisible:
            return
        pt.save()
        if self.isSelected:
            pt.setPen(Pshape.penBlueDot)
        else:
            pt.setPen(self.pen)
        pt.setBrush(self.brush)
        pt.drawPath(self.path)
        pt.restore()
        
    def drawFrame(self,pt):
        pt.save()
        pt.setPen(Pshape.penBlueSolid)
        pt.drawPath(self.path)
        pt.restore()

    def getBrush(self):
        return self.brush
    