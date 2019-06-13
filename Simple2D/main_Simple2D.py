from mainwindow import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from simple2ddoc import *
from history import *

TOOL_NO       = 0
TOOL_SELECT   = 1
TOOL_ADJUST   = 2
TOOL_LINE     = 3
TOOL_POLYLINE = 4
TOOL_CURVE    = 5
TOOL_POLYGON  = 6
TOOL_RECT     = 7
TOOL_ELLIPSE  = 8
TOOL_INK      = 9
TOOL_POT      = 10
TOOL_STRAW    = 11
TOOL_SCARE    = 12
TOOL_ROTATE   = 13


OP_SHOW		=	1	#显示和隐藏图形，用于绘制和删除操作
OP_SELECT	=	2	#选取图形
OP_TRANSLATE=	3	#移动图形
OP_SCALE	=	4	#缩放图形
OP_ROTATE	=	5	#旋转图形
OP_TRACE	=	6	#描绘图形
OP_FILL		=	7	#填充图形
OP_FLIP		=	8	#翻转图形
OP_LAYER	=	9	#调整图形层次
OP_ADJUST	=   10	#调节控制点位置

ALT_TOP		=	2	#移到最高层
ALT_UP		=	1	#上移一层
ALT_DOWN	=  -1	#下移一层
ALT_BOTTOM	=  -2	#移到最低层

class MainWidget(QMainWindow,Ui_MainWindow):
    strawColorGet=pyqtSignal(QColor)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Simple2D")
        self.showMaximized()  #窗口最大化
        rect = QRect()
        rect = QApplication.desktop().availableGeometry()  #获取主屏幕大小
        #setWindowFlags(windowFlags()&~Qt::WindowMaximizeButtonHint);    # 禁止最大化按钮
        self.setFixedSize(rect.width(),rect.height())    #不能修改窗口大小
        self.widget.resize(self.width()-120,self.height()-180)
        '''
        connect(ui->widget,SIGNAL(strawColorGet(QColor)),this,SLOT(updataStrawColor(QColor)));
        connect(ui->dockWidget_3,&QDockWidget::visibilityChanged,this,&MainWindow::toolBoxCloseShow);
        '''
        self.widget.strawColorGet.connect(self.updataStrawColor)
        self.dockWidget_3.visibilityChanged.connect(self.toolBoxCloseShow)
        self.updataStrawColor(QColor(Qt.black))
        self.toolUsing = 0
        self.filePath = ""
        self.hasProgram = 0  #0无工程，1未保存，2已保存
        self.profile = ""


    def updataStrawColor(self,c):
        img = QPixmap(self.Button_lnkcolor.iconSize())
        pt = QPainter()
        pt.begin(img)
        pt.fillRect(img.rect(),c)
        pt.end()
        self.Button_lnkcolor.setIcon(QIcon(img))
        self.Button_potcolor.setIcon(QIcon(img))

    def toolBoxCloseShow(self,v):
        if v:
            self.action_toolbox.setChecked(True)
        else:
            self.action_toolbox.setChecked(False)
    
    def on_Button_selsct_clicked(self):#工具箱选择按钮
        self.on_action_select_triggered()

    #试着不用QString
    def on_action_save_as_triggered(self):#菜单另存为
        filename=QFileDialog.getSaveFileName(None,"另存为","文档/program.SPD","Simple2D Project Fill(*.SPD)")
        if len(filename)==0:
            return
        Simple2DDoc.saveToDoc(self.widget.getShapeList(),filename)

   
    def on_action_save_triggered(self): #菜单保存
        self.proNeedSave()
        if self.hasProgram==1:
            Simple2DDoc.saveToDoc(self.widget.getShapeList(),self.profile[0])
            QMessageBox.information(None,"保存成功","工程已保存！")
            self.hasProgram=2
            return
        if self.hasProgram == 2:
            QMessageBox.information(None,"保存成功","工程已保存！")
            return
        filename=QFileDialog.getSaveFileName(None,"保存","文档/program.SPD","Simple2D Project Fill(*.SPD)")
        if len(filename)==0:
            return
        Simple2DDoc.saveToDoc(self.widget.getShapeList(),filename[0])
        QMessageBox.information(None,"保存成功","工程已保存到"+filename[0])
        self.profile=filename
        self.hasProgram=2


    def on_action_open_triggered(self):#菜单打开项目
        self.proNeedSave()
        if self.hasProgram==1:
            if QMessageBox.question(None,"是否保存","当前工作尚未保存，是否保存？",QMessageBox.Yes,QMessageBox.No)==QMessageBox.Yes:
                self.on_action_save_triggered()    
        self.hasProgram = 2

        
        filename=QFileDialog.getOpenFileName(None,"选择工程","文档/program.SPD","Simple2D Project Fill(*.SPD)")
        print (filename[0])
        if len(filename)==0:
            return
        self.on_action_close_triggered()
        self.widget.anotherProgram(Simple2DDoc.readDoc(filename[0]))
        self.profile=filename
        self.hasProgram=2
    #这个可能有问题
    def on_action_close_triggered(self):#菜单关闭项目
        if self.hasProgram==1 or self.hasProgram==0:
            if QMessageBox.question(None,"是否保存","当前工作尚未保存，是否保存？",QMessageBox.Yes,QMessageBox.No)==QMessageBox.Yes:
                self.on_action_save_triggered()
            
        self.hasProgram=2

        #QVector<DMShape *> *p=ui->widget->getShapeList()
        p = self.widget.getShapeList()
        #DMShape * t
        while len(p)!=0:
            p.pop()
        
        #delete p
        self.hasProgram=0
        self.widget.closeProgram()
        
    def on_action_attribute_panel_triggered(self):#菜单打开属性面板
        self.widget.showAttributepanel()

    def on_action_newfile_triggered(self):#菜单打开新工程
        self.on_action_close_triggered()
        self.hasProgram=2   
        #QVector<DMShape*> *p=new QVector<DMShape*>()
        p = []
        self.widget.setShapeList(p)

    def on_action_print_triggered(self):#菜单打印功能
        if not Simple2DDoc.printer(self.widget.getShapeList(),self.widget.size()):
            QMessageBox.information(None,"提示","打印失败！")


    def on_action_select_triggered(self):#菜单选择工具
        self.widget.setTool(TOOL_SELECT)
        self.Button_rotate.setEnabled(True)
        self.Button_scale.setEnabled(True)

        self.action_ellipse.setChecked(False)
        self.action_rect.setChecked(False)
        self.action_adjust.setChecked(False)
        self.action_curve.setChecked(False)
        self.action_line.setChecked(False)
        self.action_polygon.setChecked(False)
        self.action_broken_line.setChecked(False)
        self.action_paint_pot.setChecked(False)
        self.action_ink_bottle.setChecked(False)
        self.action_straw.setChecked(False)
        self.action_select.setChecked(True)

        self.Button_selsct.setChecked(True)
        self.Button_adjust.setChecked(False)
        self.Button_curse.setChecked(False)
        self.Button_ellipse.setChecked(False)
        self.Button_line.setChecked(False)
        self.Button_polyline.setChecked(False)
        self.Button_rect.setChecked(False)
        self.Button_polygon.setChecked(False)
        self.Button_lnk.setChecked(False)
        self.Button_pot.setChecked(False)
        self.Button_straw.setChecked(False)

    def on_action_rect_triggered(self):#菜单矩形工具
        self.widget.setTool(TOOL_RECT)
        self.action_ellipse.setChecked(False)
        self.action_rect.setChecked(True)
        self.action_adjust.setChecked(False)
        self.action_curve.setChecked(False)
        self.action_line.setChecked(False)
        self.action_polygon.setChecked(False)
        self.action_broken_line.setChecked(False)
        self.action_paint_pot.setChecked(False)
        self.action_ink_bottle.setChecked(False)
        self.action_straw.setChecked(False)
        self.action_select.setChecked(False)

        self.Button_selsct.setChecked(False)
        self.Button_adjust.setChecked(False)
        self.Button_curse.setChecked(False)
        self.Button_ellipse.setChecked(False)
        self.Button_line.setChecked(False)
        self.Button_polyline.setChecked(False)
        self.Button_rect.setChecked(True)
        self.Button_polygon.setChecked(False)
        self.Button_lnk.setChecked(False)
        self.Button_pot.setChecked(False)
        self.Button_straw.setChecked(False)

    def on_Button_rect_clicked(self):#工具箱矩形工具
        self.on_action_rect_triggered()

    def on_Button_ellipse_clicked(self):#工具箱椭圆工具
        self.on_action_ellipse_triggered()

    def on_action_ellipse_triggered(self):#菜单椭圆工具
        self.widget.setTool(TOOL_ELLIPSE)
        self.action_ellipse.setChecked(True)
        self.action_rect.setChecked(False)
        self.action_adjust.setChecked(False)
        self.action_curve.setChecked(False)
        self.action_line.setChecked(False)
        self.action_polygon.setChecked(False)
        self.action_broken_line.setChecked(False)
        self.action_paint_pot.setChecked(False)
        self.action_ink_bottle.setChecked(False)
        self.action_straw.setChecked(False)
        self.action_select.setChecked(False)
        
        self.Button_selsct.setChecked(False)
        self.Button_adjust.setChecked(False)
        self.Button_curse.setChecked(False)
        self.Button_ellipse.setChecked(True)
        self.Button_line.setChecked(False)
        self.Button_polyline.setChecked(False)
        self.Button_rect.setChecked(False)
        self.Button_polygon.setChecked(False)
        self.Button_lnk.setChecked(False)
        self.Button_pot.setChecked(False)
        self.Button_straw.setChecked(False)

    def on_Button_line_clicked(self):#工具箱直线工具
        self.on_action_line_triggered()

    def on_action_line_triggered(self):#菜单直线工具
        self.widget.setTool(TOOL_LINE)
        self.action_ellipse.setChecked(False)
        self.action_rect.setChecked(False)
        self.action_adjust.setChecked(False)
        self.action_curve.setChecked(False)
        self.action_line.setChecked(True)
        self.action_polygon.setChecked(False)
        self.action_broken_line.setChecked(False)
        self.action_paint_pot.setChecked(False)
        self.action_ink_bottle.setChecked(False)
        self.action_straw.setChecked(False)
        self.action_select.setChecked(False)
        
        self.Button_selsct.setChecked(False)
        self.Button_adjust.setChecked(False)
        self.Button_curse.setChecked(False)
        self.Button_ellipse.setChecked(False)
        self.Button_line.setChecked(True)
        self.Button_polyline.setChecked(False)
        self.Button_rect.setChecked(False)
        self.Button_polygon.setChecked(False)
        self.Button_lnk.setChecked(False)
        self.Button_pot.setChecked(False)
        self.Button_straw.setChecked(False)

    def on_Button_polyline_clicked(self):#工具箱折线工具
        self.on_action_broken_line_triggered()

    def on_action_broken_line_triggered(self):#菜单折线工具
        self.widget.setTool(TOOL_POLYLINE)
        self.action_ellipse.setChecked(False)
        self.action_rect.setChecked(False)
        self.action_adjust.setChecked(False)
        self.action_curve.setChecked(False)
        self.action_line.setChecked(False)
        self.action_polygon.setChecked(False)
        self.action_broken_line.setChecked(True)
        self.action_paint_pot.setChecked(False)
        self.action_ink_bottle.setChecked(False)
        self.action_straw.setChecked(False)
        self.action_select.setChecked(False)
        
        self.Button_selsct.setChecked(False)
        self.Button_adjust.setChecked(False)
        self.Button_curse.setChecked(False)
        self.Button_ellipse.setChecked(False)
        self.Button_line.setChecked(False)
        self.Button_polyline.setChecked(True)
        self.Button_rect.setChecked(False)
        self.Button_polygon.setChecked(False)
        self.Button_lnk.setChecked(False)
        self.Button_pot.setChecked(False)
        self.Button_straw.setChecked(False)

    def on_Button_polygon_clicked(self):#工具箱多边形工具
        self.on_action_polygon_triggered()

    def on_action_polygon_triggered(self):#菜单多边形工具
        self.widget.setTool(TOOL_POLYGON)
        self.action_ellipse.setChecked(False)
        self.action_rect.setChecked(False)
        self.action_adjust.setChecked(False)
        self.action_curve.setChecked(False)
        self.action_line.setChecked(False)
        self.action_polygon.setChecked(True)
        self.action_broken_line.setChecked(False)
        self.action_paint_pot.setChecked(False)
        self.action_ink_bottle.setChecked(False)
        self.action_straw.setChecked(False)
        self.action_select.setChecked(False)
        
        self.Button_selsct.setChecked(False)
        self.Button_adjust.setChecked(False)
        self.Button_curse.setChecked(False)
        self.Button_ellipse.setChecked(False)
        self.Button_line.setChecked(False)
        self.Button_polyline.setChecked(False)
        self.Button_rect.setChecked(False)
        self.Button_polygon.setChecked(True)
        self.Button_lnk.setChecked(False)
        self.Button_pot.setChecked(False)
        self.Button_straw.setChecked(False)

    def on_Button_curse_clicked(self):#工具箱曲线工具
        self.on_action_curve_triggered()

    def on_action_curve_triggered(self):#菜单曲线工具
        self.widget.setTool(TOOL_CURVE)
        self.action_ellipse.setChecked(False)
        self.action_rect.setChecked(False)
        self.action_adjust.setChecked(False)
        self.action_curve.setChecked(True)
        self.action_line.setChecked(False)
        self.action_polygon.setChecked(False)
        self.action_broken_line.setChecked(False)
        self.action_paint_pot.setChecked(False)
        self.action_ink_bottle.setChecked(False)
        self.action_straw.setChecked(False)
        self.action_select.setChecked(False)
        
        self.Button_selsct.setChecked(False)
        self.Button_adjust.setChecked(False)
        self.Button_curse.setChecked(True)
        self.Button_ellipse.setChecked(False)
        self.Button_line.setChecked(False)
        self.Button_polyline.setChecked(False)
        self.Button_rect.setChecked(False)
        self.Button_polygon.setChecked(False)
        self.Button_lnk.setChecked(False)
        self.Button_pot.setChecked(False)
        self.Button_straw.setChecked(False)

    def on_Button_pot_clicked(self):#工具箱油漆桶工具
        self.on_action_paint_pot_triggered()

    def on_action_paint_pot_triggered(self):#菜单油漆桶工具
        self.widget.setTool(TOOL_POT)
        self.action_ellipse.setChecked(False)
        self.action_rect.setChecked(False)
        self.action_adjust.setChecked(False)
        self.action_curve.setChecked(False)
        self.action_line.setChecked(False)
        self.action_polygon.setChecked(False)
        self.action_broken_line.setChecked(False)
        self.action_paint_pot.setChecked(True)
        self.action_ink_bottle.setChecked(False)
        self.action_straw.setChecked(False)
        self.action_select.setChecked(False)
    
        self.Button_selsct.setChecked(False)
        self.Button_adjust.setChecked(False)
        self.Button_curse.setChecked(False)
        self.Button_ellipse.setChecked(False)
        self.Button_line.setChecked(False)
        self.Button_polyline.setChecked(False)
        self.Button_rect.setChecked(False)
        self.Button_polygon.setChecked(False)
        self.Button_lnk.setChecked(False)
        self.Button_pot.setChecked(True)
        self.Button_straw.setChecked(False)

    def on_Button_lnk_clicked(self):#工具箱墨水瓶工具
        self.on_action_ink_bottle_triggered()

    def on_action_ink_bottle_triggered(self):#菜单墨水瓶工具
        self.widget.setTool(TOOL_INK)
        self.action_ellipse.setChecked(False)
        self.action_rect.setChecked(False)
        self.action_adjust.setChecked(False)
        self.action_curve.setChecked(False)
        self.action_line.setChecked(False)
        self.action_polygon.setChecked(False)
        self.action_broken_line.setChecked(False)
        self.action_paint_pot.setChecked(False)
        self.action_ink_bottle.setChecked(True)
        self.action_straw.setChecked(False)
        self.action_select.setChecked(False)
        
        self.Button_selsct.setChecked(False)
        self.Button_adjust.setChecked(False)
        self.Button_curse.setChecked(False)
        self.Button_ellipse.setChecked(False)
        self.Button_line.setChecked(False)
        self.Button_polyline.setChecked(False)
        self.Button_rect.setChecked(False)
        self.Button_polygon.setChecked(False)
        self.Button_lnk.setChecked(True)
        self.Button_pot.setChecked(False)
        self.Button_straw.setChecked(False)

    def on_Button_straw_clicked(self):#工具箱吸管工具
        self.on_action_straw_triggered()

    def on_action_straw_triggered(self):#菜单吸管工具
        self.widget.setTool(TOOL_STRAW)
        self.action_ellipse.setChecked(False)
        self.action_rect.setChecked(False)
        self.action_adjust.setChecked(False)
        self.action_curve.setChecked(False)
        self.action_line.setChecked(False)
        self.action_polygon.setChecked(False)
        self.action_broken_line.setChecked(False)
        self.action_paint_pot.setChecked(False)
        self.action_ink_bottle.setChecked(False)
        self.action_straw.setChecked(True)
        self.action_select.setChecked(False)

        self.Button_selsct.setChecked(False)
        self.Button_adjust.setChecked(False)
        self.Button_curse.setChecked(False)
        self.Button_ellipse.setChecked(False)
        self.Button_line.setChecked(False)
        self.Button_polyline.setChecked(False)
        self.Button_rect.setChecked(False)
        self.Button_polygon.setChecked(False)
        self.Button_lnk.setChecked(False)
        self.Button_pot.setChecked(False)
        self.Button_straw.setChecked(True)

    def on_Button_lnkcolor_clicked(self):#选择墨水瓶描绘颜色
        color = QColor()
        color=QColorDialog.getColor(self.widget.getLnkColor(),None,"选择墨水瓶颜色")
        #print("test")
        pix = QPixmap(self.Button_lnkcolor.iconSize())
        pt = QPainter()
        pt.begin(pix)
        pt.fillRect(pix.rect(),color)
        pt.end()
        self.Button_lnkcolor.setIcon(QIcon(pix))
        self.widget.setLnkColor(color)

    def on_Button_potcolor_clicked(self):#选择油漆桶填充颜色
        color = QColor()
        color=QColorDialog.getColor(self.widget.getPotColor(),None,"选择墨水瓶颜色")
        pix = QPixmap(self.Button_potcolor.iconSize())
        pt=QPainter()
        pt.begin(pix)
        pt.fillRect(pix.rect(),color)
        pt.end()
        self.Button_potcolor.setIcon(QIcon(pix))
        self.widget.setPotColor(color)

    def on_Button_rotate_clicked(self):
        self.on_action_rotate_triggered()

    def on_action_rotate_triggered(self):
        self.widget.setTool(TOOL_ROTATE)
        if self.Button_selsct.isChecked():
            self.Button_rotate.setChecked(True)
            self.Button_scale.setChecked(False)
            self.Button_scale.setEnabled(False)

    def on_Button_scale_clicked(self):
        self.on_action_scale_triggered()

    def on_action_scale_triggered(self):
        self.widget.setTool(TOOL_SCARE)
        if self.Button_selsct.isChecked():
            self.Button_scale.setChecked(True)
            self.Button_rotate.setChecked(False)
            self.Button_rotate.setEnabled(False)

    def on_action_90_clockwise_triggered(self):
        self.widget.actionRotate(90)

    def on_action_90_anti_clockwise_triggered(self):
        self.widget.actionRotate(-90)

    def on_action_180rotate_triggered(self):
        self.widget.actionRotate(180)

    def on_action_horizontal_flip_triggered(self):
        self.widget.actionFlip(FT_HORIZONTAL)

    def on_action_vertical_flip_triggered(self):
        self.widget.actionFlip(FT_VERTICAL)

    def on_action_move_top_triggered(self):
        self.widget.actionMove(ALT_TOP)

    def on_action_move_up_triggered(self):
        self.widget.actionMove(ALT_UP)

    def on_action_move_down_triggered(self):
        self.widget.actionMove(ALT_DOWN)

    def on_action_move_bottom_triggered(self):
        self.widget.actionMove(ALT_BOTTOM)

    def on_action_use_triggered(self):
        QMessageBox.about(None,"使用","本软件是基于图元管理系统实现的简单作图系统,使用直线、折线、曲线、多边形、矩形、椭圆6种图元进行设计\r\n"
                                    "使用方法是模仿Photoshop、Flash等经典制图软件实现的,使用者不需要更改自己的使用习惯即可上手此软件\r\n")
        print("a")

    def on_action_about_triggered(self):
        QMessageBox.about(None,"关于",
                                    "软件暂定为1.0版本,截至目前软件还有诸多不完善的地方与bug,还请见谅\n\r"
                                    "未实现功能:打印预览、打印设置、窗口大小变换、工具栏与状态栏的隐现……")


    def on_action_out_image_triggered(self):
        #这个有问题
        savefilename=QFileDialog.getSaveFileName(None,"导出为","\home","PNG(*.png)JPEG(*.jpg*.jpeg*.jpe*.jfif)Bitmap(*.bmp)")
        if not savefilename.isEmpty():
            Simple2DDoc.saveToImage(self.widget.getShapeList(),self.widget.size(),savefilename)
        

    def on_action_delete_triggered(self):
        self.widget.actionDelete()

    def on_action_copy_triggered(self):
        self.widget.actionCopy()

    def on_action_shear_triggered(self):
        self.widget.actionCut()

    def on_action_paste_triggered(self):
        self.widget.actionPaste()

    def on_action_revoke_triggered(self):
        self.widget.revoke()

    def on_action_recovery_triggered(self):
        self.widget.recover()

    def on_Button_nocolor_clicked(self):
        self.on_action_no_color_triggered()

    def on_action_no_color_triggered(self):
        b = QBrush()
        b=self.widget.getBrushUsing()
        b.setStyle(Qt.NoBrush)
        self.widget.setBrushUsing(b)

    def on_action_default_color_triggered(self):
        b = QBrush()
        b=self.widget.getBrushUsing()
        b.setColor(Qt.black)
        self.widget.setBrushUsing(b)
        p = QPen()
        p = self.widget.getPenUsing()
        #QColor.setRgb(0,0,0)
        #p.setRgb(0,0,0)
        p.setColor(Qt.black)
        self.widget.setPenUsing(p)
        self.widget.setLnkColor(QColor(Qt.black))
        self.widget.setPenUsing(QColor(Qt.black))
    def on_Button_defaultcolor_clicked(self):
        self.on_action_default_color_triggered()
    def on_action_toolbar_triggered(self):
        pass

    def on_action_toolbox_triggered(self):
        if self.dockWidget_3.isHidden():
            self.dockWidget_3.show()
        else:
            self.dockWidget_3.close()

    def on_Button_adjust_clicked(self):
        self.on_action_adjust_triggered()

    def on_action_adjust_triggered(self):
        self.widget.setTool(TOOL_ADJUST)
        self.action_ellipse.setChecked(False)
        self.action_rect.setChecked(False)
        self.action_adjust.setChecked(True)
        self.action_curve.setChecked(False)
        self.action_line.setChecked(False)
        self.action_polygon.setChecked(False)
        self.action_broken_line.setChecked(False)
        self.action_paint_pot.setChecked(False)
        self.action_ink_bottle.setChecked(False)
        self.action_straw.setChecked(False)
        self.action_select.setChecked(False)
        
        self.Button_selsct.setChecked(False)
        self.Button_adjust.setChecked(True)
        self.Button_curse.setChecked(False)
        self.Button_ellipse.setChecked(False)
        self.Button_line.setChecked(False)
        self.Button_polyline.setChecked(False)
        self.Button_rect.setChecked(False)
        self.Button_polygon.setChecked(False)
        self.Button_lnk.setChecked(False)
        self.Button_pot.setChecked(False)
        self.Button_straw.setChecked(False)

    def on_action_print_preview_triggered(self):
        Simple2DDoc.printPreview(self.widget.getShapeList(),self.widget.size())

    def on_action_print_set_triggered(self):
        Simple2DDoc.printSet()

    def proNeedSave(self):
        h = History()
        h = self.widget.getHistory()
        if self.hasProgram == 2:
            if h.hadChange():
                self.hasProgram = 1


if __name__=="__main__":
    app = QApplication(sys.argv)    #每个PyQt5应用都必须创建一个应用对象。sys.argv是一组命令行参数的列表。
    win = MainWidget()
    win.show()
    sys.exit(app.exec_())
