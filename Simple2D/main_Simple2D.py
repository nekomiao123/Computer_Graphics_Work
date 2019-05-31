from mainwindow import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
class MainWidget(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Simple2D")
if __name__=="__main__":
    app = QApplication(sys.argv)    #每个PyQt5应用都必须创建一个应用对象。sys.argv是一组命令行参数的列表。
    win = MainWidget()
    win.show()
    sys.exit(app.exec_())
