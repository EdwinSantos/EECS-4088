from tkinter import Tk, Frame
from tkinter.font import Font
#from colour import Color

class DesktopUI():
    screenW = 0
    screenH = 0
    win = 0
    framelist = []
    #top = Color("black")
    #bottom = Color("#001a35")
    #colours = list(top.range_to(bottom, 100))
    backgroundC = "#001a35"
    deffont = 0

    def __init__(self):
        self.win = Tk()
        screenWidth = self.win.winfo_screenwidth()
        screenHeight = self.win.winfo_screenheight()

        self.deffont = Font(family = "Times", size = int(screenHeight / 30)) 

        self.setscreen(screenWidth, screenHeight)

        SS = str(screenWidth) + "x" + str(screenHeight)
        self.win.geometry(SS)
        #self.win.attributes('-fullscreen', True) #make fullscreen
        self.win.focus_set() #focus on fullscreen
        self.win.configure(background = self.backgroundC)

        self.win.bind("<Escape>", lambda e: self.win.quit())        
    
    def setscreen(self, width, height):
        self.screenW = width
        self.screenH = height
    
    def reset (self):
        for i in self.framelist:
            i.destroy()
        del self.framelist[0:]
                
    def addFrame (self, fname):
        self.framelist.append(fname)

    @property
    def screen(self):
        return self.__screen

    @screen.setter
    def screen(self, value):
        self.__screen = value

    @screen.deleter
    def screen(self):
        del self.__screen   


