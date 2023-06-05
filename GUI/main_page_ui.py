from log_in_ui import *
import tkinter

class MainPage_UI():
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, bg='#dfe4fc')
        self.frame.grid(column = 0, row = 0)

        self.label_title = Label(self.frame, text="FOOD ORDER MANAGING PROGRAM", fg="red", font=("Times New Roman", 20), bg = "#dfe4fc")
        self.label_title.grid(column = 0, row = 0, columnspan = 2, rowspan = 2, padx = 50, pady = 10)

        self.button_login = Button(self.frame, text="KHÁCH HÀNG", fg="white", bg="green", width = 30, command=self.open_kh_window)
        self.button_login.grid(column = 0, row = 2, padx = 50, pady = 20)

        self.button_login = Button(self.frame, text="NHÂN VIÊN", fg="white", bg="green", width = 30, command=self.open_nv_window)
        self.button_login.grid(column = 0, row = 3, padx = 50, pady = 20)

        self.button_login = Button(self.frame, text="TÀI XẾ", fg="white", bg="green", width = 30, command=self.open_tx_window)
        self.button_login.grid(column = 1, row = 2, padx = 50, pady = 20)

        self.button_login = Button(self.frame, text="ĐỐI TÁC", fg="white", bg="green", width = 30, command=self.open_dt_window)
        self.button_login.grid(column = 1, row = 3, padx = 50, pady = 20)


    def open_kh_window(self):
        self.top_win = Toplevel()
        KH_Login_UI(self.top_win)

    def open_tx_window(self):
        self.top_win = Toplevel()
        TX_Login_UI(self.top_win)

    def open_nv_window(self):
        self.top_win = Toplevel()
        NV_Login_UI(self.top_win)

    def open_dt_window(self):
        self.top_win = Toplevel()
        DT_Login_UI(self.top_win)

win = Tk()
MainPage_UI(win)
win.mainloop()
