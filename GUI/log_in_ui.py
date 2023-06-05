from khachhang import *
from nhanvien import *
from taixe import *
from doitac import *

class Login_UI():
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent, bg = '#dfe4fc')
        self.frame.grid(column=0, row=0)

        self.text_label = Label(self.frame,text='Login ui page',  fg="red", font=("Times New Roman", 30), bg = '#dfe4fc')
        self.text_label.grid(column = 0, row = 0, columnspan = 3, padx = 50, pady = 20)

        self.label_username = Label(self.frame,text='TÀI KHOẢN:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        self.label_username.grid(column = 0, row = 1, padx = 50, pady = 10)

        self.label_password = Label(self.frame,text='MẬT KHẨU:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        self.label_password.grid(column = 0, row = 2, padx = 50, pady = 10)

        self.entry_username = Entry(self.frame, fg="white", bg = "gray", width = 50)
        self.entry_username.grid(column = 1, row = 1, columnspan = 2, padx = 50, pady = 10)

        self.entry_password = Entry(self.frame, fg="white", bg = "gray", width = 50)
        self.entry_password.grid(column = 1, row = 2, columnspan = 2, padx = 50, pady = 10)

        self.button_login = Button(self.frame, text="ĐĂNG NHẬP", fg="white", bg="green", width= 30, command= self.login)
        self.button_login.grid(column = 0, row = 3, columnspan = 3, padx = 50, pady = 20)
        
    def login(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()

        if(self.username != '' and self.password != ''):
            #conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server}; Server=DESKTOP-8LHJRLR; Database=QLBanHangOnline; UID=' + self.username +'; PWD=' + self.password)
            conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server}; Server=LAPTOP-266LSHVI; Database=QLDatMon; UID=' + self.username +'; PWD=' + self.password)

            self.cursor = conn.cursor()
            for a in self.cursor.execute("select current_user"):
                if 'KH' in a[0]:
                    self.top_win = Toplevel()
                    self.top_win.parent = self
                    KH_Info_UI(self.top_win)
                    print(a[0])
                    self.parent.destroy()

                elif 'NV' in a[0]:
                    self.top_win = Toplevel()
                    self.top_win.parent = self
                    NV_Info_UI(self.top_win)
                    print(a[0])
                    self.parent.destroy()

                elif 'DT' in a[0]:
                    self.top_win = Toplevel()
                    self.top_win.parent = self
                    DT_Info_UI(self.top_win)
                    print(a[0])
                    self.parent.destroy()

                elif 'TX' in a[0]:
                    self.top_win = Toplevel()
                    self.top_win.parent = self
                    TX_Info_UI(self.top_win)
                    print(a[0])
                    self.parent.destroy()

                elif 'dbo' in a[0]:
                    self.top_win = Toplevel()
                    self.top_win.parent = self
                    KH_Info_UI(self.top_win)
                    print(a[0])
                    self.parent.destroy()

class KH_Login_UI(Login_UI):
    def __init__(self, parent):
        super().__init__(parent)
        self.text_label.configure(text = 'KHÁCH HÀNG')

class NV_Login_UI(Login_UI):
    def __init__(self, parent):
        super().__init__(parent)
        self.text_label.configure(text = 'NHÂN VIÊN')

class TX_Login_UI(Login_UI):
    def __init__(self, parent):
        super().__init__(parent)
        self.text_label.configure(text = 'TÀI XẾ')

class DT_Login_UI(Login_UI):
    def __init__(self, parent):
        super().__init__(parent)
        self.text_label.configure(text = 'ĐỐI TÁC')
        
        self.button_login.configure(width = 20)
        self.button_login.grid(row = 3, column = 0, columnspan = 1)
        self.button_signup = Button(self.frame, text="ĐĂNG KÍ", fg="white", bg="green", width= 20)
        self.button_signup.grid(row = 3, column = 2)