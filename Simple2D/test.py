from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5.Qt
from demo import *

class te():
    def __init__(self):
        self.yao = "yao"
        self.hui = "hui"
        self.feng = "feng"

class son(File):
    def __init__(self,*args):
        super().__init__()
        if len(args)==0:
            self.Mine = "NewMine"
        else:
            te = args[0]   #te为一个tuple
            self.Mine = te.yao
            self.you = te.hui

    def read(self):
        print(self.Mine)
        print(self.you)

class sonOfson(son):
    def __init__(self):
        super().__init__()
    def read(self):
        print(self.Mine)
        print(self.you)

if __name__ == "__main__":
    t = te()
    a = son(t)
    a.read()
    b = sonOfson()
    b.read()

