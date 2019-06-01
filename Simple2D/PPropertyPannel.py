import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5
import queue
from Pshape import *
from PCloseShape import *
from PnonCloseShape import *
from history import *
from PropertyPannel import *

CH_PEN    = 1
CH_BRUSH  = 2
CH_ROTATE = 3
CH_MOVE   = 4
CH_SCALE  = 5


class PropertyPannel(QDialog,Ui_PropertyPannel):
    newOperation = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.queue = queue.Queue(0)  #队列大小没有限制
        self.rect = QRect()
        self.origin = 5
        self.pen = QPen()
        self.brush = QBrush()
        self.filled = False
        self.moveSize = QSizeF()
        self.scaleSize = QSizeF()
        self.rotateTheta = 0.0
        self.rotareCenter = QPoint()
        self.icons = []
        self.isIconChange = [True for i in range(4)]  
        self.setupUi(self)

        self.icons.append(QPixmap(self.pushButton_getpencolor.size()))
        self.icons.append(QPixmap(self.pushButton_getbrushcorol.size()))
        self.icons.append(QPixmap(self.label_showline.size()))
        self.icons.append(QPixmap(self.label_showBrush.size()))

        self.setFixedSize(self.size())
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("属性面板")


    def setCursorPosition(self,cur):
        self.label_X_down.setText(str(cur.x()))
        self.label_Y_down.setText(str(cur.y()))

    def setStrawColor(self,c):
        self.label_R.setText(str(c.red()))
        self.label_G.setText(str(c.green()))
        self.label_B.setText(str(c.blue()))
    

    def noSelect(self):
        self.tabWidget.setCurrentIndex(0)
        self.label_widget.setText("---")
        self.label_height.setText("---")
        self.label_X_up.setText("---")
        self.label_Y_up.setText("---")
        self.comboBox.setCurrentIndex(0)
        self.lineEdit_linewidth.setText("1")
        self.horizontalSlider.setValue(1)
        self.pushButton_getpencolor.setPalette(QPalette(QColor(Qt.gray)))
        self.comboBox_2.setCurrentIndex(0)
        self.update()
    
    def nextOperation(self):
        return self.queue.get()

    def queueIsEmpty(self):
        return self.queue.empty()

    def setSelectRect(self,r):
        self.rect=r
        self.label_widget.setText(str(r.width()))
        self.label_height.setText(str(r.height()))
        self.label_X_up.setText(str(r.center().x()))
        self.label_Y_up.setText(str(r.center().y()))

    def isRelation(self):
        return self.radioButton_relation.isChecked()
    
    def paintEvent(self,event):
        pt = QPainter()
        map_ = QPixmap()
        if self.isIconChange[0]:
            map_ = QPixmap(self.pushButton_getpencolor.iconSize())
            w = map_.size().width()
            h = map_.size().height()
            map_.fill()
            pt.begin(map_)
            pt.fillRect(2,2,w-4,h-4,self.pen.color())
            pt.end()
            self.pushButton_getpencolor.setIcon(QIcon(map_))
        if self.isIconChange[1]:
            map_ = QPixmap(self.pushButton_getbrushcorol.iconSize())
            w = map_.size().width()
            h = map_.size().height()
            map_.fill()
            pt.begin(map_)
            pt.fillRect(2,2,w-4,h-4,self.brush.color())
            pt.end()
            self.pushButton_getbrushcorol.setIcon(QIcon(map_))
        if self.isIconChange[2]:
            map_ = QPixmap(self.label_showBrush.size())
            w = map_.size().width()
            h = map_.size().height()
            map_.fill()
            pt.begin(map_)
            pt.fillRect(0,0,w,h,self.brush)
            pt.end()
            self.label_showBrush.setPixmap(map_)
        if self.isIconChange[3]:
            map_ = QPixmap(self.label_showline.size())
            w = map_.size().width()
            h = map_.size().height()
            map_.fill()
            pt.begin(map_)
            pt.setPen(self.pen)
            pt.drawLine(5,h/2,w-5,h/2)
            pt.end()
            self.label_showline.setPixmap(map_)

        for i in range(4):
            self.isIconChange[i] = False
    
    def getBrush(self):
        return self.brush

    def getPen(self):
        return self.pen
    
    def getFilled(self):
        return self.filled

    def getMoveSize(self):
        return self.moveSize

    def getScaleSize(self):
        return self.scaleSize

    def getRotateTheta(self):
        return self.rotateTheta

    def setRotareCenter(self,value):
        self.rotareCenter = value

    def getRotareCenter(self):
        return self.rotareCenter


    def on_pushButton_apply_clicked(self):
        i = 0
        ok = True
        if self.radioButton_translation.isChecked():
            if len(self.lineEdit_dx.text())==0:
                dx=0.0
            else:
                dx = self.lineEdit_dx.text().toDouble(ok)
                if not ok:
                    QMessageBox.about(None,"警告","请填入合法输入！")
                    return
                
            if len(self.lineEdit_dy.text())==0:
                dy = 0.0 
            else:
                dy = self.lineEdit_dy.text().toDouble(ok)
                if not ok:
                    QMessageBox.about(None,"警告","请填入合法输入！")
                    return
                
            self.moveSize.setWidth(dx)
            self.moveSize.setHeight(dy)
            self.queue.put(CH_MOVE)
            i = i+1

        if self.radioButton_scale.isChecked():
            if len(self.lineEdit_sx.text())==0:
                sx=1.0
            else:
                sx = self.lineEdit_sx.text().toDouble(ok)
                if not ok:
                    QMessageBox.about(None,"警告","请填入合法输入！")
                    return
                
            
            if len(self.lineEdit_sy.text())==0:
                sy=1.0
            else:
                sy=self.lineEdit_sy.text().toDouble(ok)
                if not ok:
                    QMessageBox.about(None,"警告","请填入合法输入！")
                    return
                
            
            self.scaleSize.setWidth(sx)
            self.scaleSize.setHeight(sy)
            self.queue.put(CH_SCALE)
            i = i + 1
        
        if self.radioButton_rotate.isChecked():
            
            if len(self.lineEdit_dthea.text())==0:
                thate=0.0
            else:
                thate=self.lineEdit_dthea.text().toDouble(ok)
                if not ok:
                    QMessageBox.about(None,"警告","请填入合法输入！")
                    return
                
                self.rotateTheta=thate
            i = i+1
            if self.origin == 1:
                self.rotareCenter = QPoint(-1,-1)
            elif self.origin == 2:
                self.rotareCenter = QPoint(0,-1)
            elif self.origin == 3:
                self.rotareCenter = QPoint(1,-1)
            elif self.origin == 4:
                self.rotareCenter = QPoint(-1,0)
            elif self.origin == 5:
                self.rotareCenter = QPoint(0,0)
            elif self.origin == 6:
                self.rotareCenter = QPoint(1,0)
            elif self.origin == 7:
                self.rotareCenter = QPoint(-1,-1)
            elif self.origin == 8:
                self.rotareCenter = QPoint(0,1)
            elif self.origin == 9:
                self.rotareCenter = QPoint(1,1)
            self.queue.put(CH_ROTATE)
        
        if i>0:
            self.newOperation.emit()

    def on_radioButton_tl_clicked(self):
        if self.radioButton_tl.isChecked():
            self.radioButton_t.setChecked(False)
            self.radioButton_tr.setChecked(False)
            self.radioButton_r.setChecked(False)
            self.radioButton_br.setChecked(False)
            self.radioButton_b.setChecked(False)
            self.radioButton_bl.setChecked(False)
            self.radioButton_l.setChecked(False)
            self.radioButton_c.setChecked(False)
            self.orgin=1
        else:
            self.radioButton_tl.setChecked(not self.radioButton_tl.isChecked())

    def on_radioButton_t_clicked(self):
        if self.radioButton_t.isChecked():
            self.radioButton_tl.setChecked(False)
            self.radioButton_tr.setChecked(False)
            self.radioButton_r.setChecked(False)
            self.radioButton_br.setChecked(False)
            self.radioButton_b.setChecked(False)
            self.radioButton_bl.setChecked(False)
            self.radioButton_l.setChecked(False)
            self.radioButton_c.setChecked(False)
            self.orgin=2
        else:
            self.radioButton_t.setChecked(not self.radioButton_t.isChecked())

    def on_radioButton_tr_clicked(self):
        if self.radioButton_tr.isChecked():
            self.radioButton_t.setChecked(False)
            self.radioButton_tl.setChecked(False)
            self.radioButton_r.setChecked(False)
            self.radioButton_br.setChecked(False)
            self.radioButton_b.setChecked(False)
            self.radioButton_bl.setChecked(False)
            self.radioButton_l.setChecked(False)
            self.radioButton_c.setChecked(False)
            self.orgin=3
        
        else:
            self.radioButton_tr.setChecked(not self.radioButton_tr.isChecked())

    def on_radioButton_l_clicked(self):
        if self.radioButton_l.isChecked():
            self.radioButton_t.setChecked(False)
            self.radioButton_tr.setChecked(False)
            self.radioButton_r.setChecked(False)
            self.radioButton_br.setChecked(False)
            self.radioButton_b.setChecked(False)
            self.radioButton_bl.setChecked(False)
            self.radioButton_tl.setChecked(False)
            self.radioButton_c.setChecked(False)
            self.orgin=4
        
        else:
            self.radioButton_l.setChecked( not self.radioButton_l.isChecked())

    def on_radioButton_c_clicked(self):
        if self.radioButton_c.isChecked():
            self.radioButton_t.setChecked(False)
            self.radioButton_tr.setChecked(False)
            self.radioButton_r.setChecked(False)
            self.radioButton_br.setChecked(False)
            self.radioButton_b.setChecked(False)
            self.radioButton_bl.setChecked(False)
            self.radioButton_l.setChecked(False)
            self.radioButton_tl.setChecked(False)
            self.orgin=5
        
        else:
            self.radioButton_c.setChecked( not self.radioButton_c.isChecked())


    def on_radioButton_r_clicked(self):
        if self.radioButton_r.isChecked():
            self.radioButton_t.setChecked(False)
            self.radioButton_tr.setChecked(False)
            self.radioButton_tl.setChecked(False)
            self.radioButton_br.setChecked(False)
            self.radioButton_b.setChecked(False)
            self.radioButton_bl.setChecked(False)
            self.radioButton_l.setChecked(False)
            self.radioButton_c.setChecked(False)
            self.orgin=6
        
        else:
            self.radioButton_r.setChecked( not self.radioButton_r.isChecked())


    def on_radioButton_bl_clicked(self):
        if self.radioButton_bl.isChecked():
            self.radioButton_t.setChecked(False)
            self.radioButton_tr.setChecked(False)
            self.radioButton_r.setChecked(False)
            self.radioButton_br.setChecked(False)
            self.radioButton_b.setChecked(False)
            self.radioButton_tl.setChecked(False)
            self.radioButton_l.setChecked(False)
            self.radioButton_c.setChecked(False)
            self.orgin=7
        
        else:
            self.radioButton_bl.setChecked( not self.radioButton_bl.isChecked())


    def on_radioButton_b_clicked(self):
        if self.radioButton_b.isChecked():
            self.radioButton_t.setChecked(False)
            self.radioButton_tr.setChecked(False)
            self.radioButton_r.setChecked(False)
            self.radioButton_br.setChecked(False)
            self.radioButton_tl.setChecked(False)
            self.radioButton_bl.setChecked(False)
            self.radioButton_l.setChecked(False)
            self.radioButton_c.setChecked(False)
            self.orgin=8
        
        else:
            self.radioButton_b.setChecked( not self.radioButton_b.isChecked())


    def on_radioButton_br_clicked(self):
        if self.radioButton_br.isChecked():
            self.radioButton_t.setChecked(False)
            self.radioButton_tr.setChecked(False)
            self.radioButton_r.setChecked(False)
            self.radioButton_tl.setChecked(False)
            self.radioButton_b.setChecked(False)
            self.radioButton_bl.setChecked(False)
            self.radioButton_l.setChecked(False)
            self.radioButton_c.setChecked(False)
            self.orgin=9
        
        else:
            self.radioButton_br.setChecked( not self.radioButton_br.isChecked())


    def on_comboBox_currentIndexChanged(self,index):
        if index == 0:
            self.pen.setStyle(Qt.SolidLine)
        elif index == 1:
            self.pen.setStyle(Qt.DotLine)
        elif index == 2:
            self.pen.setStyle(Qt.DashLine)
        elif index == 3:
            self.pen.setStyle(Qt.DashDotLine)
        elif index == 4:
            self.pen.setStyle(Qt.DashDotDotLine)
        self.isIconChange[3] = True
        self.repaint()
        self.queue.put(CH_PEN)
        self.newOperation.emit() 

    def on_horizontalSlider_valueChanged(self,value):
        self.lineEdit_linewidth.setText(str(value))
        self.pen.setWidth(value)

        self.isIconChange[3]=true
        self.update()

        self.queue.put(CH_PEN)
        self.newOperation.emit()
    def on_pushButton_getpencolor_clicked(self):
        color = QColor()
        color=QColorDialog.getColor()
        self.pen.setColor(color)
        self.pushButton_getpencolor.setPalette(color)

        self.isIconChange[3]=True
        self.isIconChange[0]=True
        self.repaint()

        self.queue.put(CH_PEN)
        self.newOperation.emit()

    def on_lineEdit_linewidth_textChanged(self,arg1):
        ok = False
        if arg1.isEmpty():
            return
        value=arg1.toInt(ok,10)

        if (not ok) or (value>self.horizontalSlider.maximum()) or (value<1):
            self.lineEdit_linewidth.setText(str(pen.width()))
        
        else:
            self.pen.setWidth(value)
            self.horizontalSlider.setValue(value)

            self.isIconChange[3]=True
            self.repaint()

            self.queue.put(CH_PEN)
            self.newOperation.emit()

    def on_comboBox_2_currentIndexChanged(self,index):
        if index == 0:
            self.brush.setStyle(Qt.NoBrush)
        elif index == 1:
            self.brush.setStyle(Qt.SolidPattern)
        elif index == 2:
            self.brush.setStyle(Qt.Dense1Pattern)
        elif index == 3:
            self.brush.setStyle(Qt.Dense2Pattern)
        elif index == 4:
            self.brush.setStyle(Qt.Dense3Pattern)
        elif index == 5:
            self.brush.setStyle(Qt.Dense4Pattern)
        elif index == 6:
            self.brush.setStyle(Qt.Dense5Pattern)
        elif index == 7:
            self.brush.setStyle(Qt.Dense6Pattern)
        elif index == 8:
            self.brush.setStyle(Qt.Dense7Pattern)
        elif index == 9:
            self.brush.setStyle(Qt.HorPattern)
        elif index == 10:
            self.brush.setStyle(Qt.VerPattern)
        elif index == 11:
            self.brush.setStyle(Qt.CrossPattern)
        elif index == 12:
            self.brush.setStyle(Qt.BDiagPattern)
        elif index == 13:
            self.brush.setStyle(Qt.FDiagPattern)
        elif index == 14:
            self.brush.setStyle(Qt.DiagCrossPattern)
        self.isIconChange[2] = True
        self.repaint()
        self.queue.put(CH_BRUSH)
        self.newOperation.emit()
    def on_pushButton_getbrushcorol_clicked(self):
        if self.comboBox_2.currentIndex()==0:
            return
        color = QColor()
        color=QColorDialog.getColor()
        self.brush.setColor(color)
        self.isIconChange[1]=true
        self.repaint()
        self.queue.put(CH_BRUSH)
        self.newOperation.emit()
    
    

    




