from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Pcurve import *
from Pline import *
from Pshape import *
from Ppolyline import *
from Prectangle import *
from Pellipse import *
from Ppolygon import *
from PyQt5.QtPrintSupport import *
import PyQt5.Qt
class Simple2DDoc:
    @staticmethod
    def saveToDoc(pshape,fileName):
        file=QFile(fileName)
        file.open(QFileDevice.ReadWrite)
        data=QDataStream(file)
        p1=Prectangle()
        p2=Pellipse()
        p3=Pline()
        p4=Pcurve()
        p5=Ppolygon
        p6=Ppoliline()
        for i in range(len(pshape)):
            if not pshape[i].isVisible:
                continue
            if pshape[i].shapeType==SH_RECT:
                p1=Prectangle(pshape[i])
                p1.serialize(data)
            elif pshape[i].shapeType==SH_ELLIPSE:
                p2=Pellipse(pshape[i])
                p2.serialize(data)
            elif pshape[i].shapeType == SH_LINE:
                
                p3 = Pline(pshape[i])
                p3.serialize(data)
            elif pshape[i].shapeType==SH_CURVE:
                p4=Pcurve(pshape[i])
                p4.serialize(data)
            elif pshape[i].shapeType==SH_POLYGON:
                p5=Ppolygon(pshape[i])
                p5.serialize(data)
            elif pshape[i].shapeType==SH_POLYLINE:
                p6=Ppoliline(pshape[i])
                p6.serialize(data)
        file.close()
        return fileName
    @staticmethod
    def readDoc(filename):
        ret=[]
        file=QFile(filename)
        file.open(QFileDevice.ReadWrite)
        data=QDataStream(file)
        shap=Pshape()
        p1 = Prectangle()
        p2 = Pellipse()
        p3 = Pline()
        p4 = Pcurve()
        p5 = Ppolygon
        p6 = Ppoliline()
        while not data.atEnd():
            shap.desSerialize(data)
            if shap.shapeType==SH_RECT:
                p1=Prectangle()
                p1.pen=shap.pen
                p1.desSerialize(data)
                p1.isVisible=True
                p1.updatePath()
                tempshape = Pshape()
                tempshape.isVisible = p1.isVisible
                tempshape.isSelected = p1.isSelected
                tempshape.isAdjusting = p1.isAdjusting
                tempshape.shapeType = p1.shapeType
                tempshape.gravity = p1.gravity
                tempshape.pen = p1.pen
                tempshape.path = p1.path
                ret.append(tempshape)
            elif shap.shapeType==SH_ELLIPSE:
                pe=Pellipse()
                p2.pen=shap.pen
                p2.desSerialize(data)
                p2.isVisible=True
                p2.updatePath()
                tempshape = Pshape()
                tempshape.isVisible = p2.isVisible
                tempshape.isSelected = p2.isSelected
                tempshape.isAdjusting = p2.isAdjusting
                tempshape.shapeType = p2.shapeType
                tempshape.gravity = p2.gravity
                tempshape.pen = p2.pen
                tempshape.path = p2.path
                ret.append(tempshape)
            elif shap.shapeType==SH_LINE:
                p3=Pline()
                p3.pen=shap.pen
                p3.desSerialize(data)
                p3.isVisible=True
                p3.updatePath()
                tempshape = Pshape()
                tempshape.isVisible = p3.isVisible
                tempshape.isSelected = p3.isSelected
                tempshape.isAdjusting = p3.isAdjusting
                tempshape.shapeType = p3.shapeType
                tempshape.gravity = p3.gravity
                tempshape.pen = p3.pen
                tempshape.path = p3.path
                ret.append(tempshape)
            elif shap.shapeType==SH_CURVE:
                p4=Pcurve()
                p4.pen=shap.pen
                p4.desSerialize(data)
                p4.isVisible=True
                p4.updatePath()
                tempshape = Pshape()
                tempshape.isVisible = p4.isVisible
                tempshape.isSelected = p4.isSelected
                tempshape.isAdjusting = p4.isAdjusting
                tempshape.shapeType = p4.shapeType
                tempshape.gravity = p4.gravity
                tempshape.pen = p4.pen
                tempshape.path = p4.path
                ret.append(tempshape)
            elif shap.shapeType==SH_POLYGON:
                p5=Ppolygon()
                p5.pen=shap.pen
                p5.desSerialize(data)
                p5.isVisible=True
                p5.updatePath()
                tempshape = Pshape()
                tempshape.isVisible = p5.isVisible
                tempshape.isSelected = p5.isSelected
                tempshape.isAdjusting = p5.isAdjusting
                tempshape.shapeType = p5.shapeType
                tempshape.gravity = p5.gravity
                tempshape.pen = p5.pen
                tempshape.path = p5.path
                ret.append(tempshape)
            elif shap.shapeType==SH_POLYLINE:
                p6=Ppoliline()
                p6.pen=shap.pen
                p6.desSerialize(data)
                p6.isVisible=True
                p6.updatePath()
                tempshape = Pshape()
                tempshape.isVisible = p6.isVisible
                tempshape.isSelected = p6.isSelected
                tempshape.isAdjusting = p6.isAdjusting
                tempshape.shapeType = p6.shapeType
                tempshape.gravity = p6.gravity
                tempshape.pen = p6.pen
                tempshape.path = p6.path
                ret.append(tempshape)
        file.close()
        return ret
    @staticmethod
    def printer(v,size):
        printer=QPrinter()
        img=QImage(size,QImage.Format_ARGB32)
        printer.setPageSize(QPrinter.A4)
        printerName=printer.printerName()
        if len(printerName)==0:
            return False
        pt=QPainter()
        pt.begin(img)
        isselect=False
        isadjust=False
        for i in range(len(v)):
            isselect=v[i].isSelected
            isadjust=v[i].isAdjusting
            v[i].isSelected=False
            v[i].isAdjusting=False
            v[i].draw(pt)
            v[i].isSelected =isselect
            v[i].isAdjusting =isadjust
        pt.end()
        printDialog=QPrintDialog(printer)
        if printDialog.exec():
            painter=QPainter()
            matrix=QTransform()
            matrix.rotate(90)
            painter.begin(printer)
            img=img.transformed(matrix)
            rect=img.rect()
            rectV=painter.viewport()
            if rect.width()>rectV.width() or rect.height()>rectV.height():
                painter.drawImage(rectV,img)
            else:
                painter.drawImage(QRect((rectV.width()-rect.width())/2,(rectV.height()-rect.height())/2,rect.width(),rect.height()),img)
            painter.end()
        return True
    @staticmethod
    def saveToImage(v,imageSize,imgName):
        imgout=QImage(imageSize,QImage.Format_ARGB32)
        print("saveToImage")
        #print(imgName)
        pt=QPainter()
        pt.begin(imgout)
        pt.fillRect(imgout.rect(),QBrush(Qt.white))
        shape=Pshape()
        for i in range(len(v)):
            shape=v[i]
            if shape.isSelected:
                shape.isSelected = False
                if shape.isAdjusting:
                    shape.isAdjusting=False
                    shape.draw(pt)
                    shape.isAdjusting=True
                else:
                    shape.draw(pt)
                shape.isSelected=True
            else:
                shape.draw(pt)
        pt.end()
        imgout.save(imgName)
    @staticmethod
    def printPreview(v,size):
        pass
    @staticmethod
    def printSet():
        pass