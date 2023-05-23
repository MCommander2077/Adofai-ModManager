import tkinter as tk
import customtkinter as ctk
import ttkbootstrap as ttk
import tkinter.messagebox as tkm


class TkinterAction():
    def __init__(self):
        ctk.set_appearance_mode("Light")

    def showinfo(self, message="message\nmessage2", title="title"):
        tkm.showinfo(message=message, title=title)

    def showerror(self, message="message\nmessage2", title="title"):
        tkm.showerror(message=message, title=title)

    def showwarning(self, message="message\nmessage2", title="title"):
        tkm.showwarning(message=message, title=title)

    def ctkWindow_setup(self,title="title",weight="800",height="600"):
        self.ctkwindow_root = ctk.CTk()
        self.ctkwindow_root.geometry(f"{weight}x{height}")
        self.ctkwindow_root.title(title)

if __name__ == "__main__":
    TkAct = TkinterAction()
    TkAct.ctkWindow_setup()
    TkAct.showinfo()
    TkAct.showerror()
    TkAct.showwarning()
