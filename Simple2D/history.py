from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Pshape import *
import math


OP_SHOW = 1	            #显示和隐藏图形，用于绘制和删除操作
OP_SELECT = 2	        #选取图形
OP_TRANSLATE = 3	    #移动图形
OP_SCALE = 4	        #缩放图形
OP_ROTATE = 5	        #旋转图形
OP_TRACE = 6	        #描绘图形
OP_FILL = 7	            #填充图形
OP_FLIP = 8	            #翻转图形
OP_LAYER = 9	        #调整图形层次
OP_ADJUST = 10	        #调节控制点位置

ALT_TOP	= 2	        #移到最高层
ALT_UP = 1	        #上移一层
ALT_DOWN = -1	    #下移一层
ALT_BOTTOM = -2	    #移到最低层


class HISINFO_OPERATION(QObject):
    def __init__(self):
        super().__init__()
        self.operation = 0


class HISINFO_SHOW(HISINFO_OPERATION):
    def __init__(self):
        super().__init__()
        self.visible = True


class HISINFO_SELECT( HISINFO_OPERATION):
    def __init__(self):
        super().__init__()
        self.select = True


class HISINFO_TRANSLATE(HISINFO_OPERATION):
    def __init__(self):
        super().__init__()
        self.offset = QSize()


class HISINFO_SCALE(HISINFO_OPERATION):
    def __init__(self):
        super().__init__()
        self.origin = QPoint()  #缩放中心
        self.Sx = 0.0           #x缩放
        self.Sy = 0.0           #y缩放


class HISINFO_ROTATE(HISINFO_OPERATION):
    def __init__(self):
        super().__init__()
        self.origin = QPoint()
        self.theta = 0.0        #偏角


class HISINFO_TRACE(HISINFO_OPERATION):
    def __init__(self):
        super().__init__()
        self.pen = QPen()


class HISINFO_FILL(HISINFO_OPERATION):
    def __init__(self):
        super().__init__()
        self.isFill = True
        self.brush = QBrush()


class HISINFO_FLIP(HISINFO_OPERATION):
    def __init__(self):
        super().__init__()
        self.flipType = 0       #翻转方式，0为水平，1为垂直
        self.origin = QPoint()  #翻转中心


class HISINFO_LAYER(HISINFO_OPERATION):
    def __init__(self):
        super().__init__()
        self.layerType = 0
        self.currentLayer = 0


class HISINFO_ADJUST(HISINFO_OPERATION):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.oldPosition = QPoint()


class H_RECORD():
    def __init__(self):
        self.operation = HISINFO_OPERATION()
        self.shape = Pshape()


class History():
    def __init__(self):
        self.shapeList = []              #图形列表

        self.history = []           #历史纪录
        self.recoveryList = []      #待恢复的记录
                                    #类型为H_RECORD

        self.hint = []
        self.reint = []
        self.operation = 0          #当前操作,for all
        self.doShape = Pshape()     #当前操作的图形

        self.isSelect = False       #for select
        self.visible = True         #for show
        self.offset = QSize()       #for translate
        self.origin = QPoint()      #for scale,rotate,flip
        self.Sx = 0.0               #for scale
        self.Sy = 0.0               #for scale
        self.theta = 0.0            #for rotate
        self.pen = QPen()           #for trace

        self.brush = QBrush()       #for fill
        self.filled =False

        self.flipType = 0           #for flip

        self.layerType = 0              #for adjust layer
        self.currentLayer = 0           #for adjust layer
        self.index = 0                  #for adjust layer
        self.oldPosition = QPoint()     #for adjust layer


    def addRecord(self):
        self.reint.clear()
        while(len(self.recoveryList) > 0):
            ptrOP = self.recoveryList.pop()
            if ptrOP.operation.operation == OP_SHOW:
                if ptrOP.operation.visible:
                    self.shapeList.remove(ptrOP.shape)

        ptrOP = H_RECORD()
        if self.operation == OP_ADJUST:
            ptrAD=HISINFO_ADJUST()
            ptrAD.operation = self.operation
            ptrAD.index = self.index
            ptrAD.oldPosition = self.oldPosition
            ptrOP.operation = ptrAD
        elif self.operation == OP_FILL:
            ptrFL = HISINFO_FILL()
            ptrFL.brush = self.brush
            ptrFL.operation = self.operation
            ptrOP.operation = ptrFL
        elif self.operation == OP_FLIP:
            ptrFLP = HISINFO_FLIP()
            ptrFLP.flipType = self.flipType
            ptrFLP.operation = self.operation
            ptrFLP. origin = self.origin
            ptrOP.operation = ptrFLP
        elif self.operation == OP_LAYER:
            ptrLY = HISINFO_LAYER()
            ptrLY.currentLayer = self.currentLayer
            ptrLY.layerType = self.layerType
            ptrLY.operation = self.operation
            ptrOP.operation = ptrLY
        elif self.operation == OP_ROTATE:
            ptrRT = HISINFO_ROTATE()
            ptrRT.operation = self.operation
            ptrRT.origin = self.origin
            ptrRT.theta = self.theta
            ptrOP.operation = ptrRT
        elif self.operation == OP_SCALE:
            ptrSC = HISINFO_SCALE()
            ptrSC.operation = self.operation
            ptrSC.Sx = self.Sx
            ptrSC.Sy = self.Sy
            ptrSC.origin = self.origin
            ptrOP = ptrSC
        elif self.operation == OP_SELECT:
            ptrSL = HISINFO_SELECT()
            ptrSL.operation = self.operation
            ptrSL.select = self.isSelect
            ptrOP = ptrSL
        elif self.operation == OP_TRACE:
            ptrTRC = HISINFO_TRACE()
            ptrTRC.operation = self.operation
            ptrTRC.pen = self.pen
            ptrOP = ptrTRC
        elif self.operation == OP_TRANSLATE:
            ptrTR = HISINFO_TRANSLATE()
            ptrTR.operation = self.operation
            ptrTR.offset = self.offset
            ptrOP = ptrTR
        elif self.operation == OP_SHOW:
            ptrSH = HISINFO_SHOW()
            ptrSH.operation = self.operation
            ptrSH.visible = self.visible
            ptrOP = ptrSH
        ptrOP.shape = self.doShape
        self.recoveryList.append(ptrOP)
        self.redo()

    def canUndo(self):
        return len(self.history) != 0

    def canRedo(self):
        return len(self.recoveryList) != 0

    def undo(self):
        if not self.canUndo():
            return False
        ptrRec = self.history.pop()
        self.recoveryList.append(ptrRec)
        #将一步操作从历史记录列表中取出并转移到待恢复记录列表中

        if ptrRec.operation == OP_ADJUST:
            ptrAD = ptrRec.operation
            ptrRec.shape.isAdjusting = True
            self.oldPosition = ptrRec.shape.getContrlPoint(ptrAD.index)
            ptrRec.shape.adjust(ptrAD.oldPosition, ptrAD.index)
            ptrAD.oldPosition = self.oldPosition

        elif ptrRec.operation == OP_FILL:
            ptrFL = ptrRec.operation
            if ptrRec.shape.shapeType == SH_ELLIPSE or ptrRec.shape.shapeType == SH_RECT or ptrRec.shape.shapeType == SH_POLYGON:
                ptrShape = ptrRec.shape
                self.brush = ptrShape.brush
                ptrShape.brush=ptrFL.brush
                ptrFL.brush = self.brush

        elif ptrRec.operation == OP_FLIP:
            ptrFLP = ptrRec.operation
            ptrRec.shape.flip(ptrFLP.flipType, ptrFLP.origin)
        elif ptrRec.operation == OP_LAYER:
            ptrLY = ptrRec.operation
            ptrLY.currentLayer = self.shapeList.index(ptrRec.shape)
            nowindex = self.shapeList.index(ptrRec.shape)
            if ptrLY.layerType == ALT_TOP:
                ptr = self.shapeList.pop(nowindex)
                self.shapeList.insert(len(self.shapeList) - 1, ptr)
            elif ptrLY.layerType == ALT_UP:
                ptr = self.shapeList.pop(nowindex)
                self.shapeList.insert(nowindex + 1, ptr)
            elif ptrLY.layerType == ALT_DOWN:
                ptr = self.shapeList.pop(nowindex)
                self.shapeList.insert(nowindex - 1, ptr)
            elif ptrLY.layerType == ALT_BOTTOM:
                ptr = self.shapeList.pop(nowindex)
                self.shapeList.insert(0, ptr)
        elif ptrRec.operation == OP_ROTATE:
            ptrRT = ptrRec.operation
            ptrRec.shape.rotate(-ptrRT.theta, ptrRT.origin)
        elif ptrRec.operation == OP_SCALE:
            ptrSC = ptrRec.operation
            ptrRec.shape.scale(1/ptrSC.Sx, 1/ptrSC.Sy, ptrSC.origin)
        elif ptrRec.operation == OP_SELECT:
            ptrSL = ptrRec.operation
            ptrRec.shape.isSelected = not ptrSL.select
        elif ptrRec.operation == OP_TRACE:
            ptrTRC = ptrRec.operation
            ptrRec.shape.isAdjusting = False
            self.pen = ptrRec.shape.pen
            ptrRec.shape.pen = ptrTRC.pen
            ptrTRC.pen = self.pen
        elif ptrRec.operation == OP_TRANSLATE:
            ptrTR =ptrRec.operation
            ptrRec.shape.translate(QPoint(-ptrTR.offset.width(),-ptrTR.offset.height()))
        elif ptrRec.operation == OP_SHOW:
            ptrSH = ptrRec.operation
            ptrRec.shape.isVisible = not ptrSH.visible
        return True

    def redo(self):
        if not self.canRedo():
            return False
        ptrRec = self.recoveryList.pop()
        self.history.append(ptrRec)
        # 将一步操作从待恢复记录列表中取出并转移到历史记录列表中

        if ptrRec.operation.operation == OP_ADJUST:
            ptrAD = ptrRec.operation
            ptrRec.shape.isAdjusting = True
            self.oldPosition = ptrRec.shape.getContrlPoint(ptrAD.index)
            ptrRec.shape.adjust(ptrAD.oldPosition, ptrAD.index)
            ptrAD.oldPosition= self.oldPosition
        elif ptrRec.operation.operation == OP_FILL:
            ptrFL = ptrRec.operation
            if ptrRec.shape.shapeType in [SH_ELLIPSE, SH_RECT, SH_POLYGON]:
                ptrShape = ptrRec.shape
                self.brush = ptrShape.brush
                ptrShape.brush = ptrFL.brush
                ptrFL.brush = self.brush
        elif ptrRec.operation.operation == OP_FLIP:
            ptrFLP = ptrRec.operation
            ptrRec.shape.flip(ptrFLP.flipType, ptrFLP.origin)
        elif ptrRec.operation.operation == OP_LAYER:
            ptrLY = ptrRec.operation
            nowpos = self.shapeList.index(ptrRec.shape)
            if ptrLY.layerType in [ALT_UP, ALT_BOTTOM, ALT_TOP, ALT_DOWN]:
                ptr = self.shapeList.pop(nowpos)
                self.shapeList.insert(ptrLY.currentLayer, ptr)
        elif ptrRec.operation.operation == OP_ROTATE:
            ptrRT = ptrRec.operation
            ptrRec.shape.rotate(ptrRT.theta, ptrRT.origin)
        elif ptrRec.operation.operation == OP_SCALE:
            ptrSC = ptrRec.operation
            ptrRec.shape.scale(ptrSC.Sx, ptrSC.Sy, ptrSC.origin)
        elif ptrRec.operation.operation == OP_SELECT:
            ptrSL = ptrRec.operation
            ptrRec.shape.isSelected = ptrSL.select
        elif ptrRec.operation.operation == OP_SHOW:
            ptrSH = ptrRec.operation
            ptrRec.shape.isVisible = ptrSH.visible
        elif ptrRec.operation.operation == OP_TRACE:
            ptrTRC = ptrRec.operation
            ptrRec.shape.isAdjusting = False
            self.pen = ptrRec.shape.pen
            ptrRec.shape.pen = ptrTRC.pen
            ptrTRC.pen = self.pen
        elif ptrRec.operation.operation == OP_TRANSLATE:
            ptrTR = ptrRec.operation
            ptrRec.shape.tranlate(QPoint(ptrTR.offset.width(), ptrTR.offset.height()))
        return True

    def clearHistory(self):
        self.history.clear()
        self.recoveryList.clear()

    def hadChange(self):
        if len(self.history) == 0:
            return False
        for i in range(len(self.history)):
            if self.history[i].operation.operation != OP_SELECT:
                return True
        return False
