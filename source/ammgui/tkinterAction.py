import tkinter
import customtkinter
import ttkbootstrap
import tkinter.messagebox as tkm

class TkinterAction():
    def __init__(self):
        pass
    def showinfo(self,message="message\nmessage2",title="title"):
        tkm.showinfo(message=message,title=title)
    def showerror(self,message="message\nmessage2",title="title"):
        tkm.showerror(message=message,title=title)
    def showwarning(self,message="message\nmessage2",title="title"):
        tkm.showwarning(message=message,title=title)

if __name__ == "__main__":
    TkAct = TkinterAction()
    TkAct.showinfo()