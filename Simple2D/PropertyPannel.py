# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Computer_Graphics_Work\Simple2D\PropertyPannel.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PropertyPannel(object):
    def setupUi(self, PropertyPannel):
        PropertyPannel.setObjectName("PropertyPannel")
        PropertyPannel.resize(336, 261)
        self.tabWidget = QtWidgets.QTabWidget(PropertyPannel)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 341, 261))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(20, 30, 41, 41))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icon/30.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(60, 20, 21, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(60, 60, 21, 16))
        self.label_3.setObjectName("label_3")
        self.label_widget = QtWidgets.QLabel(self.tab)
        self.label_widget.setGeometry(QtCore.QRect(80, 20, 51, 16))
        self.label_widget.setText("")
        self.label_widget.setObjectName("label_widget")
        self.label_height = QtWidgets.QLabel(self.tab)
        self.label_height.setGeometry(QtCore.QRect(80, 60, 51, 16))
        self.label_height.setText("")
        self.label_height.setObjectName("label_height")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(160, 30, 41, 41))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(":/icon/31.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(210, 20, 21, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(210, 60, 21, 16))
        self.label_6.setObjectName("label_6")
        self.label_X_up = QtWidgets.QLabel(self.tab)
        self.label_X_up.setGeometry(QtCore.QRect(230, 20, 51, 16))
        self.label_X_up.setText("")
        self.label_X_up.setObjectName("label_X_up")
        self.label_Y_up = QtWidgets.QLabel(self.tab)
        self.label_Y_up.setGeometry(QtCore.QRect(230, 60, 51, 16))
        self.label_Y_up.setText("")
        self.label_Y_up.setObjectName("label_Y_up")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(20, 150, 41, 41))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap(":/icon/2x_eyedroper.png"))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(60, 130, 21, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(60, 160, 21, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(60, 190, 21, 16))
        self.label_10.setObjectName("label_10")
        self.label_R = QtWidgets.QLabel(self.tab)
        self.label_R.setGeometry(QtCore.QRect(80, 130, 51, 16))
        self.label_R.setText("")
        self.label_R.setObjectName("label_R")
        self.label_G = QtWidgets.QLabel(self.tab)
        self.label_G.setGeometry(QtCore.QRect(80, 160, 51, 16))
        self.label_G.setText("")
        self.label_G.setObjectName("label_G")
        self.label_B = QtWidgets.QLabel(self.tab)
        self.label_B.setGeometry(QtCore.QRect(80, 190, 51, 16))
        self.label_B.setText("")
        self.label_B.setObjectName("label_B")
        self.label_11 = QtWidgets.QLabel(self.tab)
        self.label_11.setGeometry(QtCore.QRect(170, 150, 21, 31))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.tab)
        self.label_12.setGeometry(QtCore.QRect(210, 130, 16, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.tab)
        self.label_13.setGeometry(QtCore.QRect(210, 170, 21, 16))
        self.label_13.setObjectName("label_13")
        self.label_X_down = QtWidgets.QLabel(self.tab)
        self.label_X_down.setGeometry(QtCore.QRect(230, 130, 51, 16))
        self.label_X_down.setText("")
        self.label_X_down.setObjectName("label_X_down")
        self.label_Y_down = QtWidgets.QLabel(self.tab)
        self.label_Y_down.setGeometry(QtCore.QRect(230, 170, 61, 16))
        self.label_Y_down.setText("")
        self.label_Y_down.setObjectName("label_Y_down")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.radioButton_translation = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_translation.setGeometry(QtCore.QRect(20, 30, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(12)
        self.radioButton_translation.setFont(font)
        self.radioButton_translation.setAutoExclusive(False)
        self.radioButton_translation.setObjectName("radioButton_translation")
        self.radioButton_scale = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_scale.setGeometry(QtCore.QRect(20, 100, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(12)
        self.radioButton_scale.setFont(font)
        self.radioButton_scale.setAutoExclusive(False)
        self.radioButton_scale.setObjectName("radioButton_scale")
        self.radioButton_rotate = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_rotate.setGeometry(QtCore.QRect(20, 170, 101, 19))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(12)
        self.radioButton_rotate.setFont(font)
        self.radioButton_rotate.setAutoExclusive(False)
        self.radioButton_rotate.setObjectName("radioButton_rotate")
        self.lineEdit_dx = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_dx.setGeometry(QtCore.QRect(120, 30, 41, 21))
        self.lineEdit_dx.setObjectName("lineEdit_dx")
        self.label_14 = QtWidgets.QLabel(self.tab_2)
        self.label_14.setGeometry(QtCore.QRect(170, 30, 21, 21))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(12)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.lineEdit_sx = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_sx.setGeometry(QtCore.QRect(120, 100, 41, 21))
        self.lineEdit_sx.setObjectName("lineEdit_sx")
        self.label_15 = QtWidgets.QLabel(self.tab_2)
        self.label_15.setGeometry(QtCore.QRect(170, 95, 16, 31))
        self.label_15.setObjectName("label_15")
        self.lineEdit_sy = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_sy.setGeometry(QtCore.QRect(190, 100, 41, 21))
        self.lineEdit_sy.setObjectName("lineEdit_sy")
        self.lineEdit_dy = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_dy.setGeometry(QtCore.QRect(190, 30, 41, 21))
        self.lineEdit_dy.setObjectName("lineEdit_dy")
        self.lineEdit_dthea = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_dthea.setGeometry(QtCore.QRect(120, 170, 41, 21))
        self.lineEdit_dthea.setObjectName("lineEdit_dthea")
        self.radioButton_relation = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_relation.setGeometry(QtCore.QRect(240, 100, 61, 19))
        self.radioButton_relation.setAutoExclusive(False)
        self.radioButton_relation.setObjectName("radioButton_relation")
        self.pushButton_apply = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_apply.setGeometry(QtCore.QRect(260, 170, 61, 28))
        self.pushButton_apply.setObjectName("pushButton_apply")
        self.radioButton_tl = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_tl.setGeometry(QtCore.QRect(170, 140, 16, 19))
        self.radioButton_tl.setText("")
        self.radioButton_tl.setObjectName("radioButton_tl")
        self.radioButton_t = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_t.setGeometry(QtCore.QRect(200, 140, 16, 19))
        self.radioButton_t.setText("")
        self.radioButton_t.setObjectName("radioButton_t")
        self.radioButton_tr = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_tr.setGeometry(QtCore.QRect(230, 140, 16, 19))
        self.radioButton_tr.setText("")
        self.radioButton_tr.setObjectName("radioButton_tr")
        self.radioButton_bl = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_bl.setGeometry(QtCore.QRect(170, 200, 16, 19))
        self.radioButton_bl.setText("")
        self.radioButton_bl.setObjectName("radioButton_bl")
        self.radioButton_b = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_b.setGeometry(QtCore.QRect(200, 200, 16, 19))
        self.radioButton_b.setText("")
        self.radioButton_b.setObjectName("radioButton_b")
        self.radioButton_br = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_br.setGeometry(QtCore.QRect(230, 200, 16, 19))
        self.radioButton_br.setText("")
        self.radioButton_br.setObjectName("radioButton_br")
        self.radioButton_l = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_l.setGeometry(QtCore.QRect(170, 170, 16, 19))
        self.radioButton_l.setText("")
        self.radioButton_l.setObjectName("radioButton_l")
        self.radioButton_c = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_c.setGeometry(QtCore.QRect(200, 170, 16, 19))
        self.radioButton_c.setText("")
        self.radioButton_c.setChecked(True)
        self.radioButton_c.setObjectName("radioButton_c")
        self.radioButton_r = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_r.setGeometry(QtCore.QRect(230, 170, 16, 20))
        self.radioButton_r.setText("")
        self.radioButton_r.setObjectName("radioButton_r")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.comboBox = QtWidgets.QComboBox(self.tab_3)
        self.comboBox.setGeometry(QtCore.QRect(76, 30, 191, 22))
        self.comboBox.setIconSize(QtCore.QSize(190, 22))
        self.comboBox.setDuplicatesEnabled(False)
        self.comboBox.setObjectName("comboBox")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/line1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox.addItem(icon, "")
        self.comboBox.setItemText(0, "")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/line2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox.addItem(icon1, "")
        self.comboBox.setItemText(1, "")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/line3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox.addItem(icon2, "")
        self.comboBox.setItemText(2, "")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/line4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox.addItem(icon3, "")
        self.comboBox.setItemText(3, "")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/line5.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox.addItem(icon4, "")
        self.comboBox.setItemText(4, "")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icon/line6.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.comboBox.addItem(icon5, "")
        self.comboBox.setItemText(5, "")
        self.label_17 = QtWidgets.QLabel(self.tab_3)
        self.label_17.setGeometry(QtCore.QRect(20, 30, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(12)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.tab_3)
        self.label_18.setGeometry(QtCore.QRect(20, 80, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(12)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.lineEdit_linewidth = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_linewidth.setGeometry(QtCore.QRect(70, 80, 41, 21))
        self.lineEdit_linewidth.setObjectName("lineEdit_linewidth")
        self.horizontalSlider = QtWidgets.QSlider(self.tab_3)
        self.horizontalSlider.setGeometry(QtCore.QRect(120, 80, 141, 22))
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label_19 = QtWidgets.QLabel(self.tab_3)
        self.label_19.setGeometry(QtCore.QRect(20, 120, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.pushButton_getpencolor = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_getpencolor.setGeometry(QtCore.QRect(70, 120, 41, 28))
        self.pushButton_getpencolor.setAutoFillBackground(True)
        self.pushButton_getpencolor.setText("")
        self.pushButton_getpencolor.setIconSize(QtCore.QSize(41, 28))
        self.pushButton_getpencolor.setObjectName("pushButton_getpencolor")
        self.label_showline = QtWidgets.QLabel(self.tab_3)
        self.label_showline.setGeometry(QtCore.QRect(70, 160, 201, 41))
        self.label_showline.setText("")
        self.label_showline.setScaledContents(True)
        self.label_showline.setObjectName("label_showline")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.label_20 = QtWidgets.QLabel(self.tab_4)
        self.label_20.setGeometry(QtCore.QRect(40, 30, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.comboBox_2 = QtWidgets.QComboBox(self.tab_4)
        self.comboBox_2.setGeometry(QtCore.QRect(100, 30, 171, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_21 = QtWidgets.QLabel(self.tab_4)
        self.label_21.setGeometry(QtCore.QRect(40, 90, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.pushButton_getbrushcorol = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_getbrushcorol.setGeometry(QtCore.QRect(100, 90, 41, 28))
        self.pushButton_getbrushcorol.setAutoFillBackground(True)
        self.pushButton_getbrushcorol.setText("")
        self.pushButton_getbrushcorol.setIconSize(QtCore.QSize(41, 28))
        self.pushButton_getbrushcorol.setObjectName("pushButton_getbrushcorol")
        self.label_showBrush = QtWidgets.QLabel(self.tab_4)
        self.label_showBrush.setGeometry(QtCore.QRect(90, 150, 91, 51))
        self.label_showBrush.setText("")
        self.label_showBrush.setScaledContents(True)
        self.label_showBrush.setObjectName("label_showBrush")
        self.tabWidget.addTab(self.tab_4, "")

        self.retranslateUi(PropertyPannel)
        self.tabWidget.setCurrentIndex(3)
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PropertyPannel)

    def retranslateUi(self, PropertyPannel):
        _translate = QtCore.QCoreApplication.translate
        PropertyPannel.setWindowTitle(_translate("PropertyPannel", "Form"))
        self.label_2.setText(_translate("PropertyPannel", "W："))
        self.label_3.setText(_translate("PropertyPannel", "H:"))
        self.label_5.setText(_translate("PropertyPannel", "X:"))
        self.label_6.setText(_translate("PropertyPannel", "Y:"))
        self.label_8.setText(_translate("PropertyPannel", "R:"))
        self.label_9.setText(_translate("PropertyPannel", "G:"))
        self.label_10.setText(_translate("PropertyPannel", "B:"))
        self.label_11.setText(_translate("PropertyPannel", "<html><head/><body><p><span style=\" font-size:18pt; color:#0055ff;\">+</span></p></body></html>"))
        self.label_12.setText(_translate("PropertyPannel", "X:"))
        self.label_13.setText(_translate("PropertyPannel", "Y:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("PropertyPannel", "信息"))
        self.radioButton_translation.setText(_translate("PropertyPannel", "平移   dx："))
        self.radioButton_scale.setText(_translate("PropertyPannel", "缩放    ↔"))
        self.radioButton_rotate.setText(_translate("PropertyPannel", "旋转    ∠"))
        self.label_14.setText(_translate("PropertyPannel", "dy:"))
        self.label_15.setText(_translate("PropertyPannel", "<html><head/><body><p><span style=\" font-size:12pt;\">↕</span></p></body></html>"))
        self.radioButton_relation.setText(_translate("PropertyPannel", "关联"))
        self.pushButton_apply.setText(_translate("PropertyPannel", "应用"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("PropertyPannel", "转换"))
        self.label_17.setText(_translate("PropertyPannel", "线型："))
        self.label_18.setText(_translate("PropertyPannel", "线宽："))
        self.lineEdit_linewidth.setText(_translate("PropertyPannel", "1"))
        self.label_19.setText(_translate("PropertyPannel", "颜色:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("PropertyPannel", "描绘"))
        self.label_20.setText(_translate("PropertyPannel", "风格："))
        self.comboBox_2.setItemText(0, _translate("PropertyPannel", "没有"))
        self.comboBox_2.setItemText(1, _translate("PropertyPannel", "默认填充"))
        self.comboBox_2.setItemText(2, _translate("PropertyPannel", "密度填充93.75%"))
        self.comboBox_2.setItemText(3, _translate("PropertyPannel", "密度填充87.50%"))
        self.comboBox_2.setItemText(4, _translate("PropertyPannel", "密度填充62.50%"))
        self.comboBox_2.setItemText(5, _translate("PropertyPannel", "密度填充50.00%"))
        self.comboBox_2.setItemText(6, _translate("PropertyPannel", "密度填充37.50%"))
        self.comboBox_2.setItemText(7, _translate("PropertyPannel", "密度填充12.50%"))
        self.comboBox_2.setItemText(8, _translate("PropertyPannel", "密度填充06.25%"))
        self.comboBox_2.setItemText(9, _translate("PropertyPannel", "横线填充"))
        self.comboBox_2.setItemText(10, _translate("PropertyPannel", "竖线填充"))
        self.comboBox_2.setItemText(11, _translate("PropertyPannel", "网格填充"))
        self.comboBox_2.setItemText(12, _translate("PropertyPannel", "正斜线填充"))
        self.comboBox_2.setItemText(13, _translate("PropertyPannel", "反斜线填充"))
        self.comboBox_2.setItemText(14, _translate("PropertyPannel", "斜网格填充"))
        self.label_21.setText(_translate("PropertyPannel", "颜色："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("PropertyPannel", "填充"))

from icon import *
