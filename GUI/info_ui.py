from tkinter import *
from tkinter import messagebox
import pyodbc
import ctypes

class Info_UI:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, bg = '#dfe4fc')
        self.frame.pack()

        self.label_text = Label(self.frame,text='Info page',  fg="red", font=("Times New Roman", 30), bg = '#dfe4fc')
        self.label_text.grid(column = 0, row = 0, columnspan = 3, padx = 10, pady = 20)

        self.button_info1 = Button(self.frame, text="THÔNG TIN 1", fg="white", bg="green", width= 30)
        self.button_info1.grid(column = 0, row = 1, padx = 10, pady = 20)

        self.button_info2 = Button(self.frame, text="THÔNG TIN 2", fg="white", bg="green", width= 30)
        self.button_info2.grid(column = 1, row = 1, padx = 10, pady = 20)

        self.button_info3 = Button(self.frame, text="THÔNG TIN 3", fg="white", bg="green", width= 30)
        self.button_info3.grid(column = 2, row = 1, padx = 10, pady = 20)

        self.frame_info = Frame(self.frame, bg = '#ff7f50', )
        self.frame_info.grid(column = 0, row = 2, columnspan = 3, padx = 10, pady = 10)


        self.button_logout = Button(self.frame, text="ĐĂNG XUẤT", fg="white", bg="green", width= 30, command=self.dangxuat)
        self.button_logout.grid(column = 0, row = 4, padx = 10, pady = 20)

        pass

    def frame_clear(self):
        for widget in self.frame_info.winfo_children():
            widget.destroy()
        pass

    def dangxuat(self):
        self.frame_info.destroy()
        self.parent.destroy()
        pass