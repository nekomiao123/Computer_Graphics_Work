import abc

class File():
    number = 0
    def __init__(self):
        self.Mine = 'Mine'
        self.you = 'your'
    def read(self):
        print("a")
    
    def write(self):
        pass

    def abc(self):
        print("abc")

class Txt(File):  # 文本，具体实现read和write
    def __init__(self):
        super().__init__()
    def read(self,a,b,c):
        print("son"+a+b+c)
    def write(self):
        print(self.Mine)

class sonOfTxt(Txt):
    def __init__(self):
        super().__init__()
    def read(self):
        print(self.Mine)
        super().abc()

if __name__ == "__main__":
    a = sonOfTxt()
    a.read()