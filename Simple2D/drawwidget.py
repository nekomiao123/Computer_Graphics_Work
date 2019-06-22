from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PPropertyPannel import *
from Pshape import *
from Pcurve import *
from Pline import *
from Ppolyline import *
from Prectangle import *
from Pellipse import *
from Ppolygon import *
from history import *
import math
import PyQt5.Qt
TOOL_N0=0 #没有工具
TOOL_SELECT=1#鼠标拖动，画矩形
TOOL_ADJUST=2#调节
TOOL_LINE=3#鼠标拖动，画直线
TOOL_POLYLINE=4
TOOL_CURVE=5
TOOL_POLYGON=6
TOOL_RECT=7
TOOL_ELLIPSE=8
TOOL_INK=9
TOOL_POT=10
TOOL_STRAW=11
TOOL_SCARE=12
TOOL_ROTATE=13
class DrawWidget(QWidget):
    #定义带QColor参数的信号
    strawColorGet=pyqtSignal(QColor)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setPalette(QPalette(QColor(Qt.white)))
        self.rrr = 0
        self.selectRect = QRect()  # 选择框
        self.selectPoly = QPolygon()  # 选择框的多边形形式
        self.scaleRect = QRect()
        self.hist=History()
        self.penUsing=QPen()
        self.brushUsing=QBrush()
        self.controlRect=[]#选择框的控制点
        self.mouseclick=False
        self.rotateCircleCenter=QPoint()
        self.rotateCircleCenterOld=QPoint()
        self.scarePoint=QPoint()
        self.scaleControlRectIndex=0
        self.scalintControlRectIndex=0
        self.adjustControlRectIndex=0
        self.adjustingControlRectIndex=0
        self.movingControlRectIndex=0
        self.posMousePress=QPoint()
        self.oldRotateThate=0.0
        self.scaleCenter=QPoint()
        self.sx=0.0
        self.sy=0.0
        self.copyList=[]
        self.oldPosCopy=QPoint()
        self.mousePos=QPoint()
        self.pshapeList=[]
        self.hist.shapeList = self.pshapeList
        self.isDriectional=False
        self.PRPN=PropertyPannel()
        self.PRPN.hide()
        self.PRPN.newOperation.connect(self.doOpFromAtt)
        self.tool=0
        self.PR=None
        self.PC=None
        self.PL=None
        self.PE=None
        self.PPG=None
        self.PPL=None
        self.pointShape=None#点选择的图元
        self.pointShapeShow=None
        self.potColor=QColor(Qt.black)
        self.lnkColor=QColor(Qt.black)
        self.strawColorGet.emit(self.potColor)
        self.rotateIconBlue=QImage()
        self.rotateIconBlue.load("://icon/2x_anti-reload.png")
        self.rotateIconBlack = QImage()
        self.rotateIconBlack.load("://icon/rotateblack.png")
        img=QImage()
        img.load("://icon/2x_paint.png")
        self.potMouseIcon=QPixmap()
        self.potMouseIcon=QPixmap.fromImage(img.scaled(30,30))
        img.load("://icon/2x_ink.png")
        self.lnkMouseIcon = QPixmap()
        self.lnkMouseIcon = QPixmap.fromImage(img.scaled(30, 30))
        img.load("://icon/2x_eyedroper.png")
        self.strawMouseIcon=QPixmap()
        self.strawMouseIcon=QPixmap.fromImage(img.scaled(30,30))
        self.mouseOnRotateIcon = False
        self.mouseOnScaleRect = False
        self.mouseOnMoveArea = False
        #self.mouseOnScaleRect = False
        self.mouseOnAdjustRect = False
        self.selectMode=False
        self.rotateThate=90.0
        self.moving = False
        self.scaling = False
        self.rotating = False
        self.adjusting = False
        self.selectPshape=[]
        self.selectPshapeShow=[]
    def getShapeList(self):
        return self.pshapeList
    def setShapeList(self,value):
        self.pshapeList=value
    def paintEvent(self, QPaintEvent):
        pt=QPainter(self)
        if (self.tool==TOOL_SELECT or self.tool==TOOL_ROTATE or self.tool==TOOL_SCARE)and self.selectMode:
            pt.save()
            pt.setPen(Pshape.penBlueDot)
            pt.drawPolygon(self.selectPoly)
            pt.restore()
        if self.tool==TOOL_ADJUST and self.selectMode:
            pt.save()
            pt.setPen(Pshape.penBlueSolid)
            pt.drawRects(self.controlRect)
            pt.setPen(Pshape.penBlueDot)
            i=1
            while i<len(self.controlRect)-2:
                pt.drawLine(self.controlRect[i].center(),self.controlRect[i+2].center())
                i=i+3
            pt.drawLine(self.controlRect[len(self.controlRect)-1].center(),self.controlRect[len(self.controlRect)-2].center())
            pt.drawLine(self.controlRect[0].center(),self.controlRect[1].center())
            pt.restore()
        #如果是用选择工具，则把选择矩形用蓝色虚线画出来
        if self.tool==TOOL_ROTATE and self.selectMode:
            if self.mouseOnRotateIcon:
                pt.drawImage(QRect(self.rotateCircleCenter.x()-30,self.rotateCircleCenter.y()-30,60,60),self.rotateIconBlue)
            else:
                pt.drawImage(QRect(self.rotateCircleCenter.x() - 30, self.rotateCircleCenter.y() - 30, 60, 60),
                             self.rotateIconBlack)
        if self.tool==TOOL_SCARE and self.selectMode:
            for i in range(len(self.controlRect)):
                pt.drawRect(self.controlRect[i])
        #矩形工具用蓝色实线画还没有完成的矩形
        if self.tool==TOOL_RECT and self.PR !=None:
            self.PR.drawFrame(pt)
        #椭圆工具，蓝色实线画还没有完成的椭圆
        if self.tool == TOOL_ELLIPSE and self.PE != None:
            self.PE.drawFrame(pt)
        # 直线工具，蓝色实线画还没有完成的直线
        if self.tool == TOOL_LINE and self.PL != None:
                self.PL.drawFrame(pt)
        # 折线工具，蓝色实线画还没有完成的折线
        if self.tool == TOOL_POLYLINE and  self.PPL != None:
            self.PPL.drawFrame(pt)
        # 多边形工具，蓝色实线画还没有完成的多边形
        if self.tool == TOOL_POLYGON and  self.PPG != None:
            self.PPG.drawFrame(pt)
        if self.tool == TOOL_CURVE and  self.PC != None:
            self.PC.drawFrame(pt)
        #调用图形的绘图函数画图
        if self.pshapeList:
            for i in range(len(self.pshapeList)):
                if self.pshapeList[i].isSelected:
                    if not(self.moving or self.scaling or self.rotating or self.adjusting):
                        self.pshapeList[i].draw(pt)
                else:
                    self.pshapeList[i].draw(pt)
        if (self.pointShapeShow and (self.moving or self.scaling or self.rotating or self.adjusting)):
            self.pointShapeShow.draw(pt)
        for i in range(len(self.selectPshapeShow)):
            self.selectPshapeShow[i].draw(pt)
    def mouseMoveEvent(self, QMouseEvent):
        pos=QMouseEvent.pos()
        self.PRPN.setCursorPosition(pos)
        if self.tool==TOOL_SELECT and self.selectMode:
            if self.selectRect.contains(QMouseEvent.pos()):
                self.setCursor(Qt.SizeAllCursor)
                self.mouseOnMoveArea=True
            else:
                self.setCursor(Qt.ArrowCursor)
                self.mouseOnMoveArea=False
        elif self.tool==TOOL_SCARE:
            posret=-1
            for k in range(8):
                if self.controlRect[k].contains(pos):
                    posret=k
                    break
            self.scaleControlRectIndex=posret
            if posret==-1:
                self.setCursor(Qt.ArrowCursor)
            elif posret==0 or posret==4 :
                self.setCursor(Qt.SizeFDiagCursor)
            elif posret==1 or posret==5 :
                self.setCursor(Qt.SizeVerCursor)
            elif posret==2 or posret==6 :
                self.setCursor(Qt.SizeBDiagCursor)
            elif posret==3 or posret==7 :
                self.setCursor(Qt.SizeHorCursor)
            if posret==-1:
                self.mouseOnScaleRect=False
            else:
                self.mouseOnScaleRect=True
        elif self.tool==TOOL_ROTATE:
            if QPoint.dotProduct(self.rotateCircleCenter-pos,self.rotateCircleCenter-pos)<400:
                self.mouseOnRotateIcon=True
                
                self.setCursor(QCursor(QPixmap("://icon/rotatemouseicon.png")))
            else:
                self.mouseOnRotateIcon=False
                self.setCursor(Qt.ArrowCursor)
        elif self.tool==TOOL_ADJUST:
            if self.pointShapeShow:

                if not self.pointShape.ptOnContrlPoint(pos):
                    self.setCursor(Qt.ArrowCursor)
                    self.mouseOnAdjustRect=False
                else:
                    self.setCursor(Qt.SizeAllCursor)
                    self.mouseOnAdjustRect=True

                    self.adjustControlRectIndex=self.pointShape.getCurrentContrlPoint(pos)
        if not self.mouseclick:
            return

        if self.tool==TOOL_N0:
            pass
        elif self.tool==TOOL_SELECT:
            if self.moving:
                if len(self.selectPshape)!=0:
                    shape=Pshape()
                    self.selectPshapeShow.clear()
                    for i in range(len(self.selectPshape)):
                        shape=self.copyFromPshape(self.selectPshape[i])
                    
                        shape.translate(pos-self.posMousePress)
                    
                        self.selectPshapeShow.append(shape)
                elif self.pointShape:
                 
                    self.pointShapeShow=self.copyFromPshape(self.pointShape)
                    
                    self.pointShapeShow.translate(pos-self.posMousePress)
                self.selectPoly=QPolygon(self.selectRect.translated(pos-self.posMousePress))
            else:
                self.selectRect.setBottomRight(QMouseEvent.pos())
        elif self.tool==TOOL_ROTATE:
            if self.rotating:
                pointthate=QMouseEvent.pos()-self.selectRect.center()
                nowThate=180*math.atan2(pointthate.y(),pointthate.x())/math.pi
                self.rotateThate=nowThate
                shape=Pshape()
                c = self.selectRect.center()
                if len(self.selectPshape)!=0:
                   
                    self.selectPshapeShow.clear()
                    for i in range(len(self.selectPshape)):
                        shape=self.copyFromPshape(self.selectPshape[i])
                        shape.rotate(nowThate-self.oldRotateThate,c)
                     
                        self.selectPshapeShow.append(shape)
              
                elif not self.pointShape:
                  
                    self.pointShapeShow=self.copyFromPshape(self.pointShape)
                    self.pointShapeShow.rotate(nowThate-self.oldRotateThate,c)
                mat=QTransform(1,0,0, 0,1,0, 0,0,1)
                mat1=mat
              
                mat.translate(-self.selectRect.center().x(),-self.selectRect.center().y())
                mat1.rotate(nowThate+90)
                mat=mat*mat1
                mat1.setMatrix(1,0,0, 0,1,0, 0,0,1)
                mat1.translate(self.selectRect.center().x(),self.selectRect.center().y())
                mat=mat*mat1
            
                self.selectPoly=mat.map(QPolygon(self.selectRect))
                self.rotateCircleCenter=mat.map(self.rotateCircleCenterOld)
            else:
                self.selectRect.setBottomRight(QMouseEvent.pos())
        elif self.tool==TOOL_SCARE:
            if self.scaling:
                if self.scalintControlRectIndex==0:
                    self.scaleRect.setTopLeft(pos)
                elif self.scalintControlRectIndex==1:
                    self.scaleRect.setTop(pos.y())
                elif self.scalintControlRectIndex==2:
                    self.scaleRect.setTopRight(pos)
                elif self.scalintControlRectIndex==3:
                    self.scaleRect.setRight(pos.x())
                elif self.scalintControlRectIndex==4:
                    self.scaleRect.setBottomRight(pos)
                elif self.scalintControlRectIndex==5:
                    self.scaleRect.setBottom(pos.y())
                elif self.scalintControlRectIndex==6:
                    self.scaleRect.setBottomLeft(pos)
                elif self.scalintControlRectIndex==7:
                    self.scaleRect.setLeft(pos.x())
                self.selectPoly=QPolygon(self.scaleRect)
                self.controlRect=self.setControlRect(self.scaleRect)
         
                self.sx=float(self.scaleRect.width())/self.selectRect.width()
                self.sy=float(self.scaleRect.height())/self.selectRect.height()
                shape=Pshape()
                psc=self.scaleRect.topLeft()
                if len(self.selectPshape)!=0:
                   
                    self.selectPshapeShow.clear()
                    for i in range(len(self.selectPshape)):
                        shape=self.copyFromPshape(self.selectPshape[i])
                        shape.translate(self.scaleRect.topLeft()-self.selectRect.topLeft())
                        shape.scale(self.sx,self.sy,psc)
                       
                        self.selectPshapeShow.append(shape)
                  
                elif not self.pointShape:
                    if not self.pointShapeShow:
                        del  self.pointShapeShow
                    self.pointShapeShow=self.copyFromPshape(self.pointShape)
                    self.pointShapeShow.translate(self.scaleRect.topLeft()-self.selectRect.topLeft())
                    self.pointShapeShow.scale(self.sx,self.sy,psc)
            else:
                self.selectRect.setBottomRight(QMouseEvent.pos())
        elif self.tool==TOOL_ADJUST:
            if self.adjusting:
                if self.pointShape:
                    if self.pointShapeShow:
                        del self.pointShapeShow
                    self.pointShapeShow=self.copyFromPshape(self.pointShape)
                    self.pointShapeShow.adjust(pos,self.adjustingControlRectIndex)
                    self.controlRect=self.pointShapeShow.getAllContrlRect()
        elif self.tool==TOOL_RECT:
            self.PR.setBottomRight(QMouseEvent.pos(),self.isDriectional)
        elif self.tool==TOOL_ELLIPSE:
            self.PE.setBottomRight(QMouseEvent.pos(),self.isDriectional)
        elif self.tool==TOOL_LINE:
            self.PL.setEnd(QMouseEvent.pos(),self.isDriectional)
        elif self.tool==TOOL_POLYLINE:
            if self.PPL:
                self.PPL.setLastPoint(QMouseEvent.pos())
        elif self.tool==TOOL_POLYGON:
            if self.PPG:
                self.PPG.setLastPoint(QMouseEvent.pos())
        elif self.tool==TOOL_CURVE:
            if self.PC.getPointArrayLength()>1:
                self.PC.setLastContrlPoint(QMouseEvent.pos())
        self.repaint()
    def mousePressEvent(self, event):
        k=0
        self.mouseclick=True
     
        if self.tool==TOOL_N0:
            pass
        elif self.tool==TOOL_SELECT:
            if self.mouseOnMoveArea:
                self.moving=True
                self.posMousePress=event.pos()
            else:
                if len(self.selectPshape)!=0:
                  
                    self.selectPshape.clear()
                    self.selectPshapeShow.clear()
                if not self.pointShape:
                    if not self.pointShapeShow:
                        del self.pointShapeShow
                
                    self.pointShape=None
                    self.pointShapeShow=None
                self.selectRect.setTopLeft(event.pos())
                self.selectRect.setSize(QSize(0,0))
                k=0
                for i in range(len(self.pshapeList)):
                    if self.pshapeList[i].isSelected:
                        self.hist.operation = OP_SELECT
                        self.hist.doShape = self.pshapeList[i]
                        self.hist.isSelect =False
                        self.hist.addRecord()
                        k+=1
                self.hist.hint.append(k)
        elif self.tool==TOOL_SCARE:
            if self.mouseOnScaleRect:
                self.posMousePress=event.pos()
                self.scaling=True
                self.scalintControlRectIndex=self.scaleControlRectIndex
                self.scaleRect=self.selectRect
            else:
                if len(self.selectPshapeShow)!=0:
                    
                    self.selectPshape.clear()
                    self.selectPshapeShow.clear()
                if not self.pointShape:
                    if not self.pointShapeShow:
                        del self.pointShapeShow
                  
                    self.pointShape = None
                    self.pointShapeShow = None
                self.selectRect.setTopLeft(event.pos())
                self.selectRect.setSize(QSize(0, 0))
                k = 0
                for i in range(len(self.pshapeList)):
                     if self.pshapeList[i].isSelected:
                          self.hist.operation = OP_SELECT
                          self.hist.doShape = self.pshapeList[i]
                          self.hist.isSelect =False
                          self.hist.addRecord()
                          k+=1
                self.hist.hint.append(k)
        elif self.tool==TOOL_ROTATE:
            if self.mouseOnRotateIcon:
                self.posMousePress=event.pos()
                self.oldRotateThate=self.rotateThate
                self.rotating=True
            else:
                if len(self.selectPshapeShow)!=0:
                    
                    self.selectPshape.clear()
                    self.selectPshapeShow.clear()
                if not self.pointShape:
                    if not self.pointShapeShow:
                        del self.pointShapeShow
                
                    self.pointShape = None
                    self.pointShapeShow = None
                self.selectRect.setTopLeft(event.pos())
                self.selectRect.setSize(QSize(0, 0))
                k=0
                for i in range(len(self.pshapeList)):
                    if self.pshapeList[i].isSelected:
                        self.hist.operation = OP_SELECT
                        self.hist.doShape = self.pshapeList[i]
                        self.hist.isSelect =False
                        self.hist.addRecord()
                        k+=1
                self.hist.hint.append(k)
        elif self.tool==TOOL_ADJUST:
            if self.mouseOnAdjustRect:
                self.posMousePress=event.pos()
                self.adjusting=True
                self.adjustingControlRectIndex=self.adjustControlRectIndex
            else:
                if self.pointShape:
                    if self.pointShapeShow:
                        del self.pointShapeShow
            
                    self.pointShape=None
                    self.pointShapeShow=None
                self.hist.operation = OP_SELECT
                self.hist.isSelect =False
                for i in range(len(self.pshapeList)):
                    if self.pshapeList[i].isSelected:
                        self.hist.doShape = self.pshapeList[i]
                        self.hist.addRecord()
                        self.hist.hint.append(1)
                self.hist.isSelect =True
                i=len(self.pshapeList)-1
                while i>=0:
                    if self.pshapeList[i].shapeType==SH_CURVE and self.pshapeList[i].ptOnShape(event.pos()):
                        self.hist.doShape = self.pshapeList[i]
                        self.hist.addRecord()
                        self.hist.hint.append(1)
                        self.pointShape=self.hist.doShape
                        self.controlRect=self.pointShape.getAllContrlRect()
                        self.pointShapeShow=self.copyFromPshape(self.pointShape)
                        self.selectMode=True
                        break
                    self.selectMode=False
                    i-=1
        elif self.tool==TOOL_RECT:
            self.PR=Prectangle()
            self.pshapeList.append(self.PR)
            self.PR.setTopLeft(event.pos())
            self.PR.pen = self.penUsing
            self.PR.brush = self.brushUsing
        elif self.tool==TOOL_ELLIPSE:
            self.PE = Pellipse()
            self.pshapeList.append(self.PE)
            self.PE.setTopLeft(event.pos())
            self.PE.pen = self.penUsing
            self.PE.brush = self.brushUsing
        elif self.tool==TOOL_LINE:
            self.PL = Pline()
            self.pshapeList.append(self.PL)
            self.PL.setStart(event.pos())
            self.PL.pen = self.penUsing
        elif self.tool==TOOL_POLYLINE:
           
            if self.PPL == None:
                self.PPL=Ppoliline()
                self.pshapeList.append(self.PPL)
                self.PPL.addPoint(event.pos())
                self.PPL.pen=self.penUsing
            self.PPL.addPoint(event.pos())
        elif self.tool==TOOL_POLYGON:
            if self.PPG == None:
                self.PPG=Ppolygon()
                self.pshapeList.append(self.PPG)
                self.PPG.addPoint(event.pos())
                self.PPG.pen=self.penUsing
            self.PPG.addPoint(event.pos())
        elif self.tool==TOOL_CURVE:
            if self.PC == None:
                self.PC =Pcurve()
                self.pshapeList.append(self.PC)
                self.PC.addPoint(event.pos())
                self.PC.pen = self.penUsing
            else:
                self.PC.addPoint(event.pos())
        elif self.tool==TOOL_POT:
            self.pot(event.pos())
        elif self.tool==TOOL_INK:
            self.lnk(event.pos())
        elif self.tool==TOOL_STRAW:
            self.straw(event.pos())
    def mouseReleaseEvent(self, event):
        k=0
        pos=event.pos()
        self.mouseclick=False
        if self.tool==TOOL_N0:
            pass
        if self.tool==TOOL_SELECT:
            if self.moving:
                self.moving=False
                self.hist.operation=OP_TRANSLATE
                self.hist.offset=QSize(pos.x()-self.posMousePress.x(),pos.y()-self.posMousePress.y())
                if len(self.selectPshape)!=0:
                    for i in range(len(self.selectPshape)):
                        self.hist.doShape = self.selectPshape[i]
                        self.hist.addRecord()
                    self.hist.hint.append(len(self.selectPshape))
                elif self.pointShape:
                    self.hist.doShape = self.pointShape
                    self.hist.addRecord()
                    self.hist.hint.append(1)
                self.selectRect.translate(pos-self.posMousePress)
                self.selectPoly=QPolygon(self.selectPoly)
            else:
                self.selectRect.setBottomRight(event.pos())
                self.selectRect=self.getRectR(self.selectRect)
                hadShapeSelected=False
                if self.selectRect.width()<5 and self.selectRect.height()<5:
                    index=len(self.pshapeList)-1
                    while index>=0:
                        if self.pshapeList[index].ptOnShape(event.pos()) and self.pshapeList[index].isVisible:
                            self.hist.operation = OP_SELECT
                            self.hist.isSelect = True
                            self.hist.doShape = self.pshapeList[index]
                            self.selectPshape.append(self.pshapeList[index])
                            self.hist.addRecord()
                            self.hist.hint.append(1)
                            hadShapeSelected = True
                            self.pointShape = self.pshapeList[index]
                            self.selectRect = self.pointShape.getBoundingRect()
                            self.PRPN.setSelectRect(self.selectRect)
                            self.selectPoly = QPolygon(self.selectRect)
                            self.oldRotateThate = -90
                            self.controlRect = self.setControlRect(self.selectRect)
                            break
                        index-=1
                    if hadShapeSelected:
                        self.selectMode=True
                    else:
                        self.selectMode=False
                    self.oldRotateThate=-90
                else:
                   
                    self.pointShapeShow=None
                    self.pointShape=None
                    self.PRPN.setSelectRect(self.selectRect)
                    k=0
                    self.hist.operation = OP_SELECT
                    self.hist.isSelect = True
                    for i in  range(len(self.pshapeList)):
                        if self.pshapeList[i].isInRect(self.selectRect) and self.pshapeList[i].isVisible:
                            self.hist.doShape = self.pshapeList[i]
                            self.selectPshape.append(self.pshapeList[i])
                            self.hist.addRecord()
                            k+=1
                    self.hist.hint.append(k)
                    self.selectMode=True
                    self.oldRotateThate=-90
                    for i in range(len(self.selectPshape)):
                        self.selectPshapeShow.append(self.copyFromPshape(self.selectPshape[i]))
                self.selectPoly=QPolygon(self.selectRect)
                self.controlRect=self.setControlRect(self.selectRect)
                self.rotateCircleCenter=(self.selectRect.topLeft()+self.selectRect.topRight())/2+QPoint(0,-40)
                self.rotateCircleCenterOld=self.rotateCircleCenter
        elif self.tool==TOOL_SCARE:
            if self.scaling:
             
                self.scaling=False
                self.hist.origin = self.scaleRect.topLeft()
                self.hist.Sx = self.sx
                self.hist.Sy = self.sy
                poi = self.scaleRect.topLeft() - self.selectRect.topLeft()
                self.hist.offset = QSize(poi.x(), poi.y())
                if len(self.selectPshape)!=0:
                    for i in range(len(self.selectPshape)):
                        self.hist.operation = OP_TRANSLATE
                        self.hist.doShape = self.selectPshape[i]
                        self.hist.addRecord()
                        self.hist.operation = OP_SCALE
                        self.hist.addRecord()
                    self.hist.hint.append(len(self.selectPshape) * 2)
                elif self.pointShape:
                    self.hist.operation = OP_TRANSLATE
                    self.hist.doShape = self.pointShape
                    self.hist.addRecord()
                    self.hist.operation = OP_SCALE
                    self.hist.addRecord()
                    self.hist.hint.append(2)
                self.selectRect=self.scaleRect
                self.controlRect=self.setControlRect(self.selectRect)
            else:
                self.selectRect.setBottomRight(event.pos())
                self.selectRect=self.getRectR(self.selectRect)
                hadShapeSelected=False
                if self.selectRect.width() < 5 and self.selectRect.height() < 5:
                    index=len(self.pshapeList)-1
                    while index>=0:
                        if self.pshapeList[index].ptOnShape(pos) and self.pshapeList[index].isVisible:
                            self.hist.operation = OP_SELECT
                            self.hist.isSelect = True
                            self.hist.doShape = self.pshapeList[index]
                            self.selectPshape.append(self.pshapeList[index])
                            self.hist.addRecord()
                            self.hist.hint.append(1)
                            hadShapeSelected = True
                            self.pointShape = self.pshapeList[index]
                            self.selectRect = self.pointShape.getBoundingRect()
                            self.PRPN.setSelectRect(self.selectRect)
                            self.selectPoly = QPolygon(self.selectRect)
                            self.oldRotateThate = -90
                            self.controlRect = self.setControlRect(self.selectRect)
                            break
                        index-=1
                    if hadShapeSelected:
                        self.selectMode=True
                    else:
                        self.selectMode=False
                    self.oldRotateThate=-90
                else:
                 
                    self.pointShapeShow = None
                    self.pointShape = None
                    self.PRPN.setSelectRect(self.selectRect)
                    k = 0
                    self.hist.operation = OP_SELECT
                    self.hist.isSelect = True
                    for i in  range(len(self.pshapeList)):
                        if self.pshapeList[i].isInRect(self.selectRect) and self.pshapeList[i].isVisible:
                            self.hist.doShape = self.pshapeList[i]
                            self.selectPshape.append(self.pshapeList[i])
                            self.hist.addRecord()
                            k+=1
                    self.hist.hint.append(k)
                    self.selectMode = True
                    self.oldRotateThate = -90
                    for i in range(len(self.selectPshape)):
                        self.selectPshapeShow.append(self.copyFromPshape(self.selectPshape[i]))
                self.selectPoly = QPolygon(self.selectRect)
                self.controlRect = self.setControlRect(self.selectRect)
                self.rotateCircleCenter = (self.selectRect.topLeft() + self.selectRect.topRight()) / 2 + QPoint(0, -40)
                self.rotateCircleCenterOld = self.rotateCircleCenter
        elif self.tool==TOOL_ROTATE:
            if self.rotating:
                self.rotating=False
                self.hist.operation=OP_ROTATE
                self.hist.origin = self.selectRect.center()
                self.hist.theta = self.rotateThate - self.oldRotateThate
                if len(self.selectPshape)!=0:
                    for i in range(len(self.selectPshape)):
                        self.hist.doShape=self.selectPshape[i]
                        self.hist.addRecord()
                    self.hist.hint.append(len(self.selectPshape))
                elif not self.pointShape:
                    self.hist.doShape=self.pointShape
                    self.hist.addRecord()
            else:
                self.selectRect.setBottomRight(event.pos())
                self.selectRect = self.getRectR(self.selectRect)
                hadShapeSelected = False
                if self.selectRect.width() < 5 and self.selectRect.height() < 5:
                    index = len(self.pshapeList) - 1
                    while index >= 0:
                        if self.pshapeList[index].ptOnShape(pos) and self.pshapeList[index].isVisible:
                            self.hist.operation = OP_SELECT
                            self.hist.isSelect = True
                            self.hist.doShape = self.pshapeList[index]
                            self.selectPshape.append(self.pshapeList[index])
                            self.hist.addRecord()
                            self.hist.hint.append(1)
                            hadShapeSelected = True
                            self.pointShape = self.pshapeList[index]
                            self.selectRect = self.pointShape.getBoundingRect()
                            self.PRPN.setSelectRect(self.selectRect)
                            self.selectPoly = QPolygon(self.selectRect)
                            self.controlRect = self.setControlRect(self.selectRect)
                            break
                        index -= 1
                    if hadShapeSelected:
                        self.selectMode = True
                    else:
                        self.selectMode = False
                    self.oldRotateThate = -90
                else:
             
                    self.pointShapeShow = None
                    self.pointShape = None
                    self.PRPN.setSelectRect(self.selectRect)
                    k = 0
                    self.hist.operation = OP_SELECT
                    self.hist.isSelect = True
                    for i in range(len(self.pshapeList)):
                        if self.pshapeList[i].isInRect(self.selectRect) and self.pshapeList[i].isVisible:
                            self.hist.doShape = self.pshapeList[i]
                            self.selectPshape.append(self.pshapeList[i])
                            self.hist.addRecord()
                            k+=1
                    self.hist.hint.append(k)
                    self.selectMode = True
                    self.oldRotateThate = -90
                    for i in range(len(self.selectPshape)):
                        self.selectPshapeShow.append(self.copyFromPshape(self.selectPshape[i]))
                self.selectPoly = QPolygon(self.selectRect)
                self.controlRect = self.setControlRect(self.selectRect)
                self.rotateCircleCenter = (self.selectRect.topLeft() + self.selectRect.topRight()) / 2 + QPoint(0, -40)
                self.rotateCircleCenterOld = self.rotateCircleCenter
        elif self.tool==TOOL_ADJUST:
            if self.adjusting:
                self.adjusting=False
                if self.pointShape:
                    self.hist.operation = OP_ADJUST
                    self.hist.doShape = self.pointShape
                    self.hist.index = self.adjustingControlRectIndex
                    self.hist.oldPosition = pos
                    self.hist.addRecord()
                    self.hist.hint.append(1)
                    if self.pointShapeShow:
                        del self.pointShapeShow
                    self.pointShapeShow = self.copyFromPshape(self.pointShape)
                    self.controlRect = self.pointShapeShow.getAllContrlRect()
        elif self.tool==TOOL_RECT:
            if self.PR == None:
                return
            self.PR.setBottomRight(pos,self.isDriectional)
            self.hist.operation = OP_SHOW
            self.hist.doShape = self.PR
            self.hist.visible = True
            self.hist.hint.append(1)
            self.hist.addRecord()
            self.PR =None
        elif self.tool==TOOL_ELLIPSE:
            if self.PE == None:
                return
            self.PE.setBottomRight(event.pos(),self.isDriectional)
            self.hist.operation = OP_SHOW
            self.hist.doShape = self.PE
            self.hist.visible = True
            self.hist.hint.append(1)
            self.hist.addRecord()
            self.PE = None
        elif self.tool==TOOL_LINE:
            if self.PL == None:
                return
            self.PL.setEnd(event.pos(), self.isDriectional)
            self.hist.operation = OP_SHOW
            self.hist.doShape = self.PL
            self.hist.visible = True
            self.hist.hint.append(1)
            self.hist.addRecord()
            self.PL = None
        elif self.tool==TOOL_POLYLINE:
            if self.PPL:
                self.PPL.setLastPoint(event.pos())
        elif self.tool==TOOL_POLYGON:
            if self.PPG:
                self.PPG.setLastPoint(event.pos())
        elif self.tool==TOOL_CURVE:
            if self.PC:
                if self.PC.getPointArrayLength() > 1:
                    self.PC.setLastContrlPoint(event.pos())
        self.update()
    def mouseDoubleClickEvent(self, event):
        if self.tool == TOOL_POLYLINE and self.PPL is not None:
            self.PPL.setLastPoint(event.pos())
            self.hist.operation=OP_SHOW
            self.hist.doShape=self.PPL
            self.hist.visible=True
            self.hist.hint.append(1)
            self.hist.addRecord()
            self.PPL=None
        if self.tool == TOOL_POLYGON and self.PPG is not  None:
            self.PPG.setLastPoint(event.pos())
            self.PPG.setFinished(True)
            self.hist.operation=OP_SHOW
            self.hist.doShape=self.PPG
            self.hist.visible=True
            self.hist.hint.append(1)
            self.hist.addRecord()
            self.PPG=None
        if self.tool == TOOL_CURVE and self.PC is not None:
            self.hist.operation=OP_SHOW
            self.hist.doShape=self.PC
            self.hist.visible=True
            self.hist.hint.append(1)
            self.hist.addRecord()
            self.PC=None
        self.update()
    def keyPressEvent(self, event):
        if (self.tool == TOOL_LINE or self.tool == TOOL_RECT) and (event.key() == (Qt.SHIFT | Qt.TaskButton)):
            self.isDriectional = True
    def keyReleaseEvent(self, event):
        if (self.tool == TOOL_LINE or self.tool == TOOL_RECT) and (event.key() == (Qt.SHIFT | Qt.TaskButton)):
            self.isDriectional = False
    def showAttributepanel(self):
        self.PRPN.show()
    def revoke(self):
        if len(self.hist.hint)==0:
            return
       
        for i in range(self.hist.hint[-1]):
            self.hist.undo()
        self.hist.reint.append(self.hist.hint.pop())
        self.update()
    def recover(self):
        if len(self.hist.reint)==0:
            return
      
        for i in range(self.hist.reint[-1]):
            self.hist.redo()
        self.hist.hint.append(self.hist.reint.pop())
        self.update()
    def setTool(self,tl):
        if self.tool == TOOL_SELECT and tl == TOOL_ADJUST:
            if self.selectMode:
                self.hist.operation = OP_SELECT
                self.hist.isSelect = False
                self.selectRect = QRect()
                self.selectMode = False
                k = 0
                if self.pshapeList:
                    for i in range(len(self.pshapeList)):
                        if self.pshapeList[i].isSelected:
                            self.hist.doShape=self.pshapeList[i]
                            self.hist.addRecord()
                            k+=1
                if k < 0:
                    self.hist.hint.append(k)
        self.tool=tl
        if self.tool==TOOL_SELECT:
            self.scaleRect = QRect(0, 0, 0, 0)
            self.selectRect=self.scaleRect
            self.selectMode = False
            self.selectPoly = QPolygon(self.selectRect)
        if self.tool == TOOL_INK:
            self.setCursor(QCursor(self.lnkMouseIcon))
        elif self.tool == TOOL_POT:
            self.setCursor(QCursor(self.potMouseIcon))
        elif self.tool == TOOL_STRAW:
            self.setCursor(QCursor(self.strawMouseIcon))
        else:
            self.setCursor(Qt.ArrowCursor)
        self.update()
    def closeProgram(self):
        self.pshapeList = None
        self.hist.clearHistory()
        self.selectRect = QRect()
        self.tool = 0
    def anotherProgram(self,shape):
        self.closeProgram()
        self.pshapeList = shape
        self.hist.shapeList = shape
        self.update()
    def doOpFromAtt(self):
        p=Pshape()
        while not self.PRPN.queueIsEmpty():
            temp = self.PRPN.nextOperation()
            if temp == CH_PEN:
                self.penUsing = self.PRPN.getPen()
            elif temp == CH_BRUSH:
                self.brushUsing = self.PRPN.getBrush()
            elif temp == CH_MOVE:
                if self.tool == TOOL_SELECT:
                    k = 0
                    for i in range(len(self.pshapeList)):
                        p=self.pshapeList[i]
                        if p.isVisible and p.isSelected:
                            self.hist.operation=OP_TRANSLATE
                            self.hist.offset=self.PRPN.getMoveSize().toSize()
                            self.hist.doShape=p
                            self.hist.addRecord()
                            k+=1
                    self.hist.hint.append(k)
            elif temp == CH_SCALE:
                if self.tool == TOOL_SELECT:
                    k = 0
                    for i in range(len(self.pshapeList)):
                        p=self.pshapeList[i]
                        if p.isVisible and p.isSelected:
                            self.hist.operation=OP_SCALE
                            self.hist.Sx=self.PRPN.getScaleSize().width()
                            self.hist.Sy=self.PRPN.getScaleSize().height()
                            if self.PRPN.getRotareCenter() == QPoint(-1, -1):
                                if self.PRPN.isRelation():
                                    self.hist.origin=self.getRectR(self.selectRect).topLeft()
                                else:
                                    self.hist.origin=p.getBoundingRect().topLeft()
                            elif self.PRPN.getRotareCenter() == QPoint(-1, 1):
                                if self.PRPN.isRelation():
                                    self.hist.origin=self.getRectR(self.selectRect).bottomLeft()
                                else:
                                    self.hist.origin=p.getBoundingRect().bottomLeft()
                            elif self.PRPN.getRotareCenter() == QPoint(1, 1):
                                if self.PRPN.isRelation():
                                    self.hist.origin=self.getRectR(self.selectRect).bottomRight()
                                else:
                                    self.hist.origin=p.getBoundingRect().bottomRight()
                            elif self.PRPN.getRotareCenter() == QPoint(1, -1):
                                if self.PRPN.isRelation():
                                    self.hist.origin=self.getRectR(self.selectRect).topRight()
                                else:
                                    self.hist.origin=p.getBoundingRect().topRight()
                            elif self.PRPN.getRotareCenter() == QPoint(0, -1):
                                if self.PRPN.isRelation():
                                    self.hist.origin=(self.getRectR(self.selectRect).topRight()+self.getRectR(self.selectRect).topLeft()) / 2
                                else:
                                    self.hist.origin=(p.getBoundingRect().topLeft() + p.getBoundingRect().topRight()) / 2
                            elif self.PRPN.getRotareCenter() == QPoint(-1, 0):
                                if self.PRPN.isRelation():
                                    self.hist.origin=(self.getRectR(self.selectRect).topLeft()+self.getRectR(self.selectRect).bottomLeft()) / 2
                                else:
                                    self.hist.origin=(p.getBoundingRect().topLeft() + p.getBoundingRect().bottomLeft()) / 2
                            elif self.PRPN.getRotareCenter() == QPoint(1, 0):
                                if self.PRPN.isRelation():
                                    self.hist.origin=(self.getRectR(self.selectRect).topRight()+self.getRectR(self.selectRect).bottomRight()) / 2
                                else:
                                    self.hist.origin=(p.getBoundingRect().topRight() + p.getBoundingRect().bottomRight()) / 2
                            elif self.PRPN.getRotareCenter() == QPoint(0, 1):
                                if self.PRPN.isRelation():
                                    self.hist.origin=(self.getRectR(self.selectRect).bottomLeft()+self.getRectR(self.selectRect).bottomRight()) / 2
                                else:
                                    self.hist.origin=(p.getBoundingRect().bottomRight() + p.getBoundingRect().bottomLeft()) / 2
                            elif self.PRPN.getRotareCenter() == QPoint(0, 0):
                                if self.PRPN.isRelation():
                                    self.hist.origin=self.getRectR(self.selectRect).center()
                                else:
                                    self.hist.origin=p.getBoundingRect().center()
                            self.hist.doShape = p
                            self.hist.addRecord()
                            k+=1
                    self.hist.hint.append(k)
            elif temp == CH_ROTATE:
                if self.tool == TOOL_SELECT:
                    k = 0
                    for i in range(len(self.pshapeList)):
                        p=self.pshapeList[i]
                        if p.isVisible and p.isSelected:
                            self.hist.operation=OP_ROTATE
                            self.hist.theta=self.PRPN.getRotateTheta()
                            if self.PRPN.getRotareCenter() == QPoint(-1, -1):
                                if self.PRPN.isRelation():
                                    self.hist.origin=self.getRectR(self.selectRect).topLeft()
                                else:
                                    self.hist.origin=p.getBoundingRect().topLeft()
                            elif self.PRPN.getRotareCenter() == QPoint(-1, 1):
                                if self.PRPN.isRelation():
                                    self.hist.origin=self.getRectR(self.selectRect).bottomLeft()
                                else:
                                    self.hist.origin=p.getBoundingRect().bottomLeft()
                            elif self.PRPN.getRotareCenter() == QPoint(1, 1):
                                if self.PRPN.isRelation():
                                    self.hist.origin=self.getRectR(self.selectRect).bottomRight()
                                else:
                                    self.hist.origin=p.getBoundingRect().bottomRight()
                            elif self.PRPN.getRotareCenter() == QPoint(1, -1):
                                if self.PRPN.isRelation():
                                    self.hist.origin=self.getRectR(self.selectRect).topRight()
                                else:
                                    self.hist.origin=p.getBoundingRect().topRight()
                            elif self.PRPN.getRotareCenter() == QPoint(0, -1):
                                if self.PRPN.isRelation():
                                    self.hist.origin=(self.getRectR(self.selectRect).topRight()+self.getRectR(self.selectRect).topLeft()) / 2
                                else:
                                    self.hist.origin=(p.getBoundingRect().topLeft() + p.getBoundingRect().topRight()) / 2
                            elif self.PRPN.getRotareCenter() == QPoint(-1, 0):
                                if self.PRPN.isRelation():
                                    self.hist.origin=(self.getRectR(self.selectRect).topLeft()+self.getRectR(self.selectRect).bottomLeft()) / 2
                                else:
                                    self.hist.origin=(p.getBoundingRect().topLeft() + p.getBoundingRect().bottomLeft()) / 2
                            elif self.PRPN.getRotareCenter() == QPoint(1, 0):
                                if self.PRPN.isRelation():
                                    self.hist.origin=(self.getRectR(self.selectRect).topRight()+self.getRectR(self.selectRect).bottomRight()) / 2
                                else:
                                    self.hist.origin=(p.getBoundingRect().topRight() + p.getBoundingRect().bottomRight()) / 2
                            elif self.PRPN.getRotareCenter() == QPoint(0, 1):
                                if self.PRPN.isRelation():
                                    self.hist.origin=(self.getRectR(self.selectRect).bottomLeft()+self.getRectR(self.selectRect).bottomRight()) / 2
                                else:
                                    self.hist.origin=(p.getBoundingRect().bottomRight() + p.getBoundingRect().bottomLeft()) / 2
                            elif self.PRPN.getRotareCenter() == QPoint(0, 0):
                                if self.PRPN.isRelation():
                                    self.hist.origin=self.getRectR(self.selectRect).center()
                                else:
                                    self.hist.origin=p.getBoundingRect().center()
                            self.hist.doShape = p
                            self.hist.addRecord()
                            k+=1
                    self.hist.hint.append(k)
        self.update()
 
    def getBrushUsing(self):
        return self.brushUsing
    def getHistory(self):
        return self.hist
    def getPenUsing(self):
        return self.penUsing
    def setControlRect(self,r):
        v=[]
        v.append(QRect(r.left()-5,r.top()-5,10,10))
        v.append(QRect(r.center().x()-5,r.top()-5,10,10))
        v.append(QRect(r.right()-5,r.top()-5,10,10))
        v.append(QRect(r.right()-5,r.center().y()-5,10,10))
        v.append(QRect(r.right()-5,r.bottom()-5,10,10))
        v.append(QRect(r.center().x()-5,r.bottom()-5,10,10))
        v.append( QRect(r.left()-5,r.bottom()-5,10,10))
        v.append(QRect(r.left()-5,r.center().y()-5,10,10))
        return v

    def copyFromPshape(self,s):
        r=Pshape()
       
        if s.shapeType==SH_LINE:
            self.PL=Pline(s)
            r=self.PL
            self.PL=None
        elif s.shapeType==SH_POLYGON:
            self.PPG = Ppolygon(s)
            r =self.PPG
            self.PPG =None
        elif s.shapeType ==SH_POLYLINE:
            self.PPL =Ppoliline(s)
            r =self.PPL
            self.PPL =None
        elif s.shapeType==SH_RECT:
            self.PR = Prectangle(s)
            r = self.PR
            self.PR = None
        elif s.shapeType==SH_CURVE:
            self.PC =Pcurve(s)
            r = self.PC
            self.PC = None
        elif s.shapeType ==SH_ELLIPSE:
            self.PE =Pellipse(s)
            r = self.PE
            self.PE =None
        return  r
    def getPotColor(self):
        return self.potColor
    def setPotColor(self,value):
        self.potColor=value
    def getRectR(self,r):
        if r.width() < 0 and r.height() < 0:
            return QRect(r.bottomRight(), r.topLeft())
        if r.width() > 0 and  r.height() < 0:
            return QRect(r.bottomLeft(), r.topRight())
        if r.width() < 0 and  r.height() > 0:
            return QRect(r.topRight(), r.bottomLeft())
        return r
    def actionRotate(self,theta):
        c = self.selectRect.center()
        self.hist.operation = OP_ROTATE
        self.hist.origin = c
        self.hist.theta = theta

        if len(self.selectPshape)!=0:
            for i in range(len(self.selectPshapeShow)):
                del self.selectPshapeShow[i]
            self.selectPshapeShow.clear()
            for i in range(len(self.selectPshape)):
                self.hist.doShape=self.selectPshape[i]
                self.hist.addRecord()
                self.selectPshapeShow.append(self.copyFromPshape(self.selectPshape[i]))
            self.hist.hint.append(len(self.selectPshape))
        self.update()
    def actionFlip(self,type):
        self.hist.operation = OP_FLIP
        self.hist.flipType = type
        if  len(self.selectPshape)!=0:
            for i in range(len(self.selectPshapeShow)):
                del self.selectPshapeShow[i]
            self.selectPshapeShow.clear()
            for i in range(len(self.selectPshape)):
                self.hist.doShape = self.selectPshape[i]
                self.hist.addRecord()
                self.selectPshapeShow.append(self.copyFromPshape(self.selectPshape[i]))
            self.hist.hint.append(len(self.selectPshape))
        elif not self.pointShape:
            self.hist.doShape = self.pointShape
            self.hist.addRecord()
            self.hist.hint.append(1)
        self.update()
    def actionMove(self,type):
        if not self.pointShape:
            self.hist.operation=OP_LAYER
            self.hist.currentLayer=self.pshapeList.index(self.pointShape)
            self.hist.layerType=type
            self.hist.addRecord()
            self.hist.hint.append(1)
            del self.pointShapeShow
            self.pointShapeShow=self.copyFrompShape(self.pointShape)
            self.update()
    def actionDelete(self):
        if len(self.selectPshape) == 0:
            return
        self.hist.operation = OP_SHOW
        self.hist.visible = False
        if len(self.selectPshape) != 0:
            
            self.selectPshapeShow.clear()
            for i in range(len(self.selectPshape)):
                self.hist.doShape = self.selectPshape[i]
                self.hist.addRecord()
                self.selectPshapeShow.append(self.copyFromPshape(self.selectPshape[i]))
            self.hist.hint.append(len(self.selectPshape))
        elif not self.pointShape:
            self.hist.doShape = self.pointShape
            self.hist.addRecord()
            self.hist.hint.append(1)
        self.update()
    def actionCopy(self):
        self.copyList.clear()
        self.oldPosCopy=self.mousePos
        if len(self.selectPshape)!=0:
            self.copyList+=self.selectPshape
        elif not self.pointShape:
            self.copyList.append(self.pointShape)
    def actionCut(self):
        self.actionCopy()
        self.actionDelete()
    def actionPaste(self):
        self.hist.operation = OP_SHOW
        self.hist.visible = True
        shape = Pshape()
        if len(self.selectPshape)!=0:
            for i in range(len(self.selectPshape)):
                shape=self.copyFromPshape(self.selectPshape[i])
                shape.translate(self.mousePos-self.oldPosCopy)
                self.hist.doShape=shape
                self.hist.addRecord()
                self.pshapeList.append(shape)
            self.hist.hint.append(len(self.selectPshape))
        elif not self.pointShape:
            shape = self.copyFromPshape(self.pointShape)
            shape.translate(self.mousePos - self.oldPosCopy)
            self.hist.doShape = shape
            self.hist.addRecord()
            self.hist.hint.append(1)
            self.pshapeList.append(shape)
    def getLnkColor(self):
        return self.lnkColor
    def setLnkColor(self,value):
        self.lnkColor=value
    def pot(self,point):
        p=Pshape()
        for i in range(len(self.pshapeList)):
            p = self.pshapeList[i]
            if (p.shapeType == SH_ELLIPSE or p.shapeType == SH_RECT or p.shapeType == SH_POLYGON) and p.ptInShape(point):
                self.hist.operation=OP_FILL
                self.hist.filled=True
                self.hist.brush=QBrush(self.potColor)
                self.hist.doShape=p
                self.hist.addRecord()
    def lnk(self,point):
        p=Pshape()
        lenth = len(self.pshapeList)
        for i in range(lenth):
            p = self.pshapeList[i]
            if p.ptOnShape(point):
                self.hist.operation=OP_TRACE
                pen1=self.penUsing
                pen1.setColor(self.lnkColor)
                self.hist.pen=pen1
                self.hist.doShape=p
                self.hist.addRecord()
    def straw(self,point):
        imag=self.grab(self.rect()).toImage()
        self.lnkColor=imag.pixelColor(point)
        self.potColor=self.lnkColor
        self.strawColorGet.emit(self.potColor)
    def setBrushUsing(self,value):
        self.brushUsing=value
    def setPenUsing(self,value):
        self.penUsing=value


