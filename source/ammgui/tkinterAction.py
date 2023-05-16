import tkinter as tk
import customtkinter as ctk
import ttkbootstrap as ttk
import tkinter.messagebox as tkm

class TkinterAction():
    def __init__(self):
        ctk.set_appearance_mode("Light")
    def showinfo(self,message="message\nmessage2",title="title"):
        tkm.showinfo(message=message,title=title)
    def showerror(self,message="message\nmessage2",title="title"):
        tkm.showerror(message=message,title=title)
    def showwarning(self,message="message\nmessage2",title="title"):
        tkm.showwarning(message=message,title=title)

if __name__ == "__main__":
    TkAct = TkinterAction()
    TkAct.showinfo()
    TkAct.showerror()
    TkAct.showwarning()