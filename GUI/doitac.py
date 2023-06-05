from info_ui import *

class DT_Info_UI(Info_UI):
    def __init__(self, parent):
        super().__init__(parent)

        self.label_text.configure(text='Đối tác')
        self.button_info1.configure(text='THÔNG TIN', command=self.thongtin)
        self.button_info2.configure(text='CỬA HÀNG', command=self.cuahang)
        self.button_info3.configure(text='THỰC ĐƠN', command=self.thucdon)
        self.button_info4 = Button(self.frame, text='ĐƠN HÀNG', fg="white", bg="green", width= 30, command=self.danhsachdonhang)
        self.button_info4.grid(column = 3, row = 1, padx = 10, pady = 20)

        self.label_text.grid(column=0, row=0, columnspan=4)
        self.frame_info.grid(columnspan=4)

        self.button_hopdong = None
        self.button_thongtin = None

        self.button_themcuahang = None
        self.button_xoacuahang = None
        
        self.button_themmon = None
        self.button_xoamon = None

        self.button_danggiao = None 
        self.button_dagiao = None 
        self.button_cho = None 
        self.button_dahuy = None

    def thongtin(self):
        self.frame_clear()

        self.button_hopdong = Button(self.frame, text='HỢP ĐỒNG', fg="white", bg="#6390a1", width= 20, command=self.xemHopDong)
        self.button_hopdong.grid(column = 0, columnspan=2, row = 2, padx = 10, pady = 20)
        
        self.button_thongtin = Button(self.frame, text='THÔNG TIN', fg="white", bg="#6390a1", width= 20, command=self.xemThongTin)
        self.button_thongtin.grid(column = 2, columnspan=2, row = 2, padx = 10, pady = 20)
        
        self.frame_info.grid(columnspan=4, row=3)
        

    def xemThongTin(self):
        self.frame_clear1()
        for a in self.parent.parent.cursor.execute("usp_XemThongTinDoiTac"):
            label_info = Label(self.frame_info, text='Mã đối tác: ' + a[0], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=0, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Mã hợp đồng: ' + a[1], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=1, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Mã tài khoản ngân hàng: ' + a[2], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=2, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Tên quán: ' + a[3], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=3, padx=10, pady=10)

    def xemHopDong(self):
        self.frame_clear1()
        #self.frame_info.grid(columnspan=4)
        
        self.frame_info.configure()
        
        #scrollbar
        self.canvas_frame = Canvas(self.frame_info, width=500, height=300)
        self.scrollbar_vertical = Scrollbar(self.frame_info, orient=VERTICAL, command=self.canvas_frame.yview)
        self.scrollbar_horizontal = Scrollbar(self.frame_info, orient=HORIZONTAL, command=self.canvas_frame.xview)
        self.scroll_frame = Frame(self.canvas_frame)
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")
            )
        )

        self.canvas_frame.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas_frame.configure(yscrollcommand=self.scrollbar_vertical.set, xscrollcommand=self.scrollbar_horizontal.set)
        for a in self.parent.parent.cursor.execute("usp_XemHopDong"):
            label_info = Label(self.scroll_frame, text='Mã hợp đồng: ' + a[0], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=0, padx=10, pady=10)
            label_info = Label(self.scroll_frame, text='Mã ngân hàng: ' + a[1], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=1, padx=10, pady=10)
            label_info = Label(self.scroll_frame, text='Địa chỉ chi nhánh ngân hàng: ' + a[2], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=2, padx=10, pady=10)
            label_info = Label(self.scroll_frame, text='Mã tài khoản ngân hàng: ' + a[3], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=3, padx=10, pady=10)
            label_info = Label(self.scroll_frame, text='Mã nhân viên lập hợp đồng: ' + a[4], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=4, padx=10, pady=10)
            label_info = Label(self.scroll_frame, text='Ngày lập: ' + a[5].strftime("%m/%d/%Y, %H:%M:%S"), font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=5, padx=10, pady=10)
            label_info = Label(self.scroll_frame, text='Ngày hết hạn: ' + a[6].strftime("%m/%d/%Y, %H:%M:%S"), font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=6, padx=10, pady=10)
            label_info = Label(self.scroll_frame, text='Mã thuế: ' + a[7], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=7, padx=10, pady=10)
            label_info = Label(self.scroll_frame, text='Tên người đại diện: ' + a[8], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=8, padx=10, pady=10)
            label_info = Label(self.scroll_frame, text='Số chi nhánh: ' + str(a[9]), font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=9, padx=10, pady=10)
            label_info = Label(self.scroll_frame, text='Phần trăm hoa hồng: ' + str(a[10]), font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=10, padx=10, pady=10)
        
        self.scrollbar_horizontal.pack(side='bottom', fill='x')
        self.scrollbar_vertical.pack(side='right', fill='y')
        self.canvas_frame.pack(side="left", fill="both", expand=True)

    def cuahang(self):
        self.frame_clear()

        self.button_themcuahang = Button(self.frame, text='THÊM CỬA HÀNG', fg="white", bg="#6390a1", width= 40, command=self.themCuaHang)
        self.button_themcuahang.grid(column = 0, columnspan=2, row = 2, padx = 10, pady = 20)
        
        self.button_xoacuahang = Button(self.frame, text='XÓA CỬA HÀNG', fg="white", bg="#6390a1", width= 40, command=self.xoaCuaHang)
        self.button_xoacuahang.grid(column = 2, columnspan=2, row = 2, padx = 10, pady = 20)
        
        self.frame_info.grid(columnspan=4, row=3)
        self.frame_info.grid(columnspan=4)
        i = 0
        
        self.frame_info.configure()
        
        self.frame_info.grid(columnspan=4)
        i = 0
        
        self.frame_info.configure()
        
        #scrollbar
        self.canvas_frame = Canvas(self.frame_info, width=900, height=200)
        self.scrollbar_vertical = Scrollbar(self.frame_info, orient=VERTICAL, command=self.canvas_frame.yview)
        self.scrollbar_horizontal = Scrollbar(self.frame_info, orient=HORIZONTAL, command=self.canvas_frame.xview)
        self.scroll_frame = Frame(self.canvas_frame, bg='brown')
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")
            )
        )

        self.canvas_frame.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas_frame.configure(yscrollcommand=self.scrollbar_vertical.set, xscrollcommand=self.scrollbar_horizontal.set)
           
        label_monan = Label(self.scroll_frame, text='Tên cửa hàng', bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=0, row=0)
                
        label_monan = Label(self.scroll_frame, text='Địa chỉ của hàng', bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=1, row=0)

        label_monan = Label(self.scroll_frame, text='Thời gian mở cửa', bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=2, row=0)

        label_monan = Label(self.scroll_frame, text='Thời gian đóng cửa', bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=3, row=0)
        
        label_monan = Label(self.scroll_frame, text='Tình trạng', bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=4, row=0)

        i = 1

        for a in self.parent.parent.cursor.execute(f'EXEC usp_XemCuaHangChiNhanh NULL'):    
            label_monan = Label(self.scroll_frame, text=a[2], bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=0, row=i)
            
            label_monan = Label(self.scroll_frame, text=a[1], bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=1, row=i)

            label_monan = Label(self.scroll_frame, text=a[3], bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=2, row=i)

            label_monan = Label(self.scroll_frame, text=a[4], bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=3, row=i)

            if a[5] == 1:
                a[5] = 'Mở cửa'
            elif a[5] == 0:
                a[5] = 'Tạm nghỉ'
            elif a[5] == -1:
                a[5] = 'Đóng cửa'

            label_monan = Label(self.scroll_frame, text=a[5], bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=4, row=i)
            i += 1
        
        self.scrollbar_horizontal.pack(side='bottom', fill='x')
        self.scrollbar_vertical.pack(side='right', fill='y')
        self.canvas_frame.pack(side="left", fill="both", expand=True)

    def themCuaHang(self):
        themcuahang_win = Toplevel()
        frame = Frame(themcuahang_win, bg = '#dfe4fc')

        frame.grid(column=0, row=0)

        text_label = Label(frame,text='Thêm cửa hàng',  fg="red", font=("Times New Roman", 30), bg = '#dfe4fc')
        text_label.grid(column = 0, row = 0, columnspan = 3, padx = 50, pady = 20)

        label_diachi = Label(frame,text='Địa chỉ:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        label_diachi.grid(column = 0, row = 1, padx = 50, pady = 10)

        self.entry_diachi = Entry(frame, fg="white", bg = "gray", width = 50)
        self.entry_diachi.grid(column = 1, row = 1, columnspan = 2, padx = 50, pady = 10)
        
        label_otime = Label(frame,text='Thời gian mở cửa:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        label_otime.grid(column = 0, row = 2, padx = 50, pady = 10)

        self.entry_otime = Entry(frame, fg="white", bg = "gray", width = 50)
        self.entry_otime.grid(column = 2, row = 2, columnspan = 2, padx = 50, pady = 10)
        
        label_ctime = Label(frame,text='Thời gian đóng cửa:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        label_ctime.grid(column = 0, row = 3, padx = 50, pady = 10)

        self.entry_ctime = Entry(frame, fg="white", bg = "gray", width = 50)
        self.entry_ctime.grid(column = 1, row = 3, columnspan = 2, padx = 50, pady = 10)
        
        label_tinhtrang = Label(frame,text='Tình trạng:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        label_tinhtrang.grid(column = 0, row = 4, padx = 50, pady = 10)

        self.entry_tinhtrang = Entry(frame, fg="white", bg = "gray", width = 50)
        self.entry_tinhtrang.grid(column = 1, row = 4, columnspan = 2, padx = 50, pady = 10)

        button_xacnhan = Button(frame, text="Thêm", fg="white", bg="green", width= 30, command=lambda:self.xacNhanThemCuaHang(themcuahang_win))
        button_xacnhan.grid(column = 0, row = 5, columnspan = 3, padx = 50, pady = 20)

    def xacNhanThemCuaHang(self, Win):
        arr=[]
        arr.append(self.entry_diachi.get())
        arr.append(self.entry_otime.get())
        arr.append(self.entry_ctime.get())
        arr.append(self.entry_tinhtrang.get())
        print(arr)

        sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
        sql = sql + f"EXEC @return_value = usp_ThemCuaHangChiNhanh N'{arr[0]}', '{arr[1]}', '{arr[2]}', N'{arr[3]}'"
        sql = sql + "\nselect @return_value"
        print(sql)
        check = int(self.parent.parent.cursor.execute(sql).fetchone()[0])
        self.parent.parent.cursor.commit()
        if check == 1:
            ctypes.windll.user32.MessageBoxW(0, "Thêm thành công", "Thông báo", 0)
            Win.destroy()
            self.cuahang()

    def xoaCuaHang(self):
        xoacuahang_win = Toplevel()
        frame = Frame(xoacuahang_win, bg = '#dfe4fc')

        frame.grid(column=0, row=0)

        text_label = Label(frame,text='Xóa chi nhánh cửa hàng',  fg="red", font=("Times New Roman", 30), bg = '#dfe4fc')
        text_label.grid(column = 0, row = 0, columnspan = 3, padx = 50, pady = 20)

        label_tenmon = Label(frame,text='Địa chỉ:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        label_tenmon.grid(column = 0, row = 1, padx = 50, pady = 10)

        self.entry_tenmon = Entry(frame, fg="white", bg = "gray", width = 50)
        self.entry_tenmon.grid(column = 1, row = 1, columnspan = 2, padx = 50, pady = 10)

        button_xacnhan = Button(frame, text="Xóa", fg="white", bg="green", width= 30, command=lambda:self.xacNhanXoaCuaHang(xoacuahang_win))
        button_xacnhan.grid(column = 0, row = 6, columnspan = 3, padx = 50, pady = 20)

    def xacNhanXoaCuaHang(self, Win):
        arr=[]
        arr.append(self.entry_tenmon.get())
        print(arr)

        sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
        sql = sql + f"EXEC @return_value = usp_XoaCuaHangChiNhanh N'{arr[0]}'"
        sql = sql + "\nselect @return_value"
        print(sql)
        try:
            check = int(self.parent.parent.cursor.execute(sql).fetchone()[0])
            self.parent.parent.cursor.commit()
        except: 
            check = 0
        if check == 1:
            ctypes.windll.user32.MessageBoxW(0, "Xóa thành công", "Thông báo", 0)
            Win.destroy()
            self.cuahang()
        elif check == 0:
            ctypes.windll.user32.MessageBoxW(0, "Xóa không thành công", "Thông báo", 0)

    def thucdon(self):
        self.frame_clear()

        self.button_themmon = Button(self.frame, text='THÊM MÓN', fg="white", bg="#6390a1", width= 40, command=self.themMonAn)
        self.button_themmon.grid(column = 0, columnspan=2, row = 2, padx = 10, pady = 20)
        
        self.button_xoamon = Button(self.frame, text='XÓA MÓN', fg="white", bg="#6390a1", width= 40, command=self.xoaMonAn)
        self.button_xoamon.grid(column = 2, columnspan=2, row = 2, padx = 10, pady = 20)
        
        self.frame_info.grid(columnspan=4, row=3)
        self.frame_info.grid(columnspan=4)
        i = 0
        
        self.frame_info.configure()
        
        #scrollbar
        self.canvas_frame = Canvas(self.frame_info, width=900, height=200)
        self.scrollbar_vertical = Scrollbar(self.frame_info, orient=VERTICAL, command=self.canvas_frame.yview)
        self.scrollbar_horizontal = Scrollbar(self.frame_info, orient=HORIZONTAL, command=self.canvas_frame.xview)
        self.scroll_frame = Frame(self.canvas_frame, bg='brown')
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")
            )
        )

        self.canvas_frame.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas_frame.configure(yscrollcommand=self.scrollbar_vertical.set, xscrollcommand=self.scrollbar_horizontal.set)

        list_label_text = ['Tên món', 'Miêu tả món', 'Giá', 'Tình trạng', 'Số lượng hiện có', 'Sửa giá', 'Sửa số lượng hiện có', 'Sửa tình trạng']
        for pos in range(len(list_label_text)):
            Label(self.scroll_frame, text=list_label_text[pos], bg='brown', fg='white', font=('Times New Roman', 20)).grid(column=pos, row=0)  

        i = 1
        list_info_label=[1, 2, 3, 4, 5]
        for a in self.parent.parent.cursor.execute(f"EXEC usp_XemThucDon"):
            print(a)
            col = 0
            for pos in range(len(list_info_label)): 
                if list_info_label[pos] == 4:
                    if a[list_info_label[pos]] == 1:
                        a[list_info_label[pos]] = 'Có bán'
                    elif a[list_info_label[pos]] == 0:
                        a[list_info_label[pos]] = 'Hết hàng'
                    if a[list_info_label[pos]] == -1:
                        a[list_info_label[pos]] = 'Tạm ngưng'
                label = Label(self.scroll_frame, text=a[list_info_label[pos]], bg='#ff7f50', font=('Times New Roman', 20))
                label.grid(column=pos, row=i)
                col = pos + 1

            button_gia = Button(self.scroll_frame, text='Sửa', width=10, bg='teal', command=lambda tenmon = a[1]:self.suaGia(tenmon))
            button_gia.grid(column=col, row=i, padx=10, pady=10)

            button_soluong = Button(self.scroll_frame, text='Sửa', width=10, bg='teal', command=lambda tenmon = a[1]:self.suaSoLuong(tenmon))
            button_soluong.grid(column=col+1, row=i, padx=10, pady=10)
            
            button_tinhtrang = Button(self.scroll_frame, text='Sửa', width=10, bg='teal', command=lambda tenmon = a[1]:self.suaTinhTrang(tenmon))
            button_tinhtrang.grid(column=col+2, row=i, padx=10, pady=10)
            i += 1
        
        self.scrollbar_horizontal.pack(side='bottom', fill='x')
        self.scrollbar_vertical.pack(side='right', fill='y')
        self.canvas_frame.pack(side="left", fill="both", expand=True)

    def themMonAn(self):
        themmon_win = Toplevel()
        frame = Frame(themmon_win, bg = '#dfe4fc')

        frame.grid(column=0, row=0)

        text_label = Label(frame,text='Thêm món ăn',  fg="red", font=("Times New Roman", 30), bg = '#dfe4fc')
        text_label.grid(column = 0, row = 0, columnspan = 3, padx = 50, pady = 20)

        label_tenmon = Label(frame,text='Tên  món:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        label_tenmon.grid(column = 0, row = 1, padx = 50, pady = 10)

        self.entry_tenmon = Entry(frame, fg="white", bg = "gray", width = 50)
        self.entry_tenmon.grid(column = 1, row = 1, columnspan = 2, padx = 50, pady = 10)
        
        label_mieuta = Label(frame,text='Miêu tả món:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        label_mieuta.grid(column = 0, row = 2, padx = 50, pady = 10)

        self.entry_mieuta = Entry(frame, fg="white", bg = "gray", width = 50)
        self.entry_mieuta.grid(column = 2, row = 2, columnspan = 2, padx = 50, pady = 10)
        
        label_gia = Label(frame,text='Giá:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        label_gia.grid(column = 0, row = 3, padx = 50, pady = 10)

        self.entry_gia = Entry(frame, fg="white", bg = "gray", width = 50)
        self.entry_gia.grid(column = 1, row = 3, columnspan = 2, padx = 50, pady = 10)
        
        label_soluong = Label(frame,text='Số lượng:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        label_soluong.grid(column = 0, row = 4, padx = 50, pady = 10)

        self.entry_soluong = Entry(frame, fg="white", bg = "gray", width = 50)
        self.entry_soluong.grid(column = 1, row = 4, columnspan = 2, padx = 50, pady = 10)
        
        label_tinhtrang = Label(frame,text='Tình trạng:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        label_tinhtrang.grid(column = 0, row = 5, padx = 50, pady = 10)

        self.entry_tinhtrang = Entry(frame, fg="white", bg = "gray", width = 50)
        self.entry_tinhtrang.grid(column = 1, row = 5, columnspan = 2, padx = 50, pady = 10)

        button_xacnhan = Button(frame, text="Thêm", fg="white", bg="green", width= 30, command=lambda:self.xacNhanThem(themmon_win))
        button_xacnhan.grid(column = 0, row = 6, columnspan = 3, padx = 50, pady = 20)

    def xacNhanThem(self, Win):
        arr=[]
        arr.append(self.entry_tenmon.get())
        arr.append(self.entry_mieuta.get())
        arr.append(self.entry_gia.get())
        arr.append(self.entry_soluong.get())
        arr.append(self.entry_tinhtrang.get())
        print(arr)

        sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
        sql = sql + f"EXEC @return_value = usp_ThemMonAn N'{arr[0]}', N'{arr[1]}', {arr[2]}, N'{arr[4]}', {arr[3]}"
        sql = sql + "\nselect @return_value"
        print(sql)
        check = int(self.parent.parent.cursor.execute(sql).fetchone()[0])
        self.parent.parent.cursor.commit()
        if check == 1:
            ctypes.windll.user32.MessageBoxW(0, "Thêm thành công", "Thông báo", 0)
            Win.destroy()
            self.thucdon()

    def xoaMonAn(self):
        xoamon_win = Toplevel()
        frame = Frame(xoamon_win, bg = '#dfe4fc')

        frame.grid(column=0, row=0)

        text_label = Label(frame,text='Xóa món ăn',  fg="red", font=("Times New Roman", 30), bg = '#dfe4fc')
        text_label.grid(column = 0, row = 0, columnspan = 3, padx = 50, pady = 20)

        label_tenmon = Label(frame,text='Tên  món:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        label_tenmon.grid(column = 0, row = 1, padx = 50, pady = 10)

        self.entry_tenmon = Entry(frame, fg="white", bg = "gray", width = 50)
        self.entry_tenmon.grid(column = 1, row = 1, columnspan = 2, padx = 50, pady = 10)

        button_xacnhan = Button(frame, text="Xóa", fg="white", bg="green", width= 30, command=lambda:self.xacNhanXoa(xoamon_win))
        button_xacnhan.grid(column = 0, row = 6, columnspan = 3, padx = 50, pady = 20)

    def xacNhanXoa(self, Win):
        arr=[]
        arr.append(self.entry_tenmon.get())
        print(arr)

        sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
        sql = sql + f"EXEC @return_value = usp_XoaMonAn N'{arr[0]}'"
        sql = sql + "\nselect @return_value"
        print(sql)
        check = int(self.parent.parent.cursor.execute(sql).fetchone()[0])
        self.parent.parent.cursor.commit()
        if check == 1:
            ctypes.windll.user32.MessageBoxW(0, "Xóa thành công", "Thông báo", 0)
            Win.destroy()
            self.thucdon()

    def suaTinhTrang(self, TenMon):
        sua_win = Toplevel()
        frame = Frame(sua_win, bg = '#dfe4fc')

        frame.grid(column=0, row=0)

        text_label = Label(frame,text='Sửa tình trạng',  fg="red", font=("Times New Roman", 30), bg = '#dfe4fc')
        text_label.grid(column = 0, row = 0, columnspan = 3, padx = 50, pady = 20)

        label_tenmon = Label(frame,text='Tình trạng:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        label_tenmon.grid(column = 0, row = 1, padx = 50, pady = 10)

        self.entry_tinhtrang = Entry(frame, fg="white", bg = "gray", width = 50)
        self.entry_tinhtrang.grid(column = 1, row = 1, columnspan = 2, padx = 50, pady = 10)

        button_sua = Button(frame, text="Sửa", fg="white", bg="green", width= 30, command=lambda tinhtrang = self.entry_tinhtrang.get():self.xacNhanSuaTinhTrang(sua_win, TenMon, tinhtrang))
        button_sua.grid(column = 0, row = 3, columnspan = 3, padx = 50, pady = 20)

    def xacNhanSuaTinhTrang(self, Win, TenMon, TinhTrang):
        TinhTrang = self.entry_tinhtrang.get()
        sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
        sql = sql + f"EXEC @return_value = usp_SuaTinhTrangMonAn N'{TenMon}', N'{TinhTrang}'"
        sql = sql + "\nselect @return_value"
        print(sql)
        try:
            check = int(self.parent.parent.cursor.execute(sql).fetchone()[0])
            self.parent.parent.cursor.commit()
        except:
            check = 0
            
        if check == 1:
            ctypes.windll.user32.MessageBoxW(0, "Sửa thành công", "Thông báo", 0)
            Win.destroy()
            self.thucdon()
        elif check == 0:
            ctypes.windll.user32.MessageBoxW(0, "Sửa không thành công", "Thông báo", 0)

    def suaGia(self, TenMon):
        sua_win = Toplevel()
        frame = Frame(sua_win, bg = '#dfe4fc')

        frame.grid(column=0, row=0)

        text_label = Label(frame,text='Sửa giá',  fg="red", font=("Times New Roman", 30), bg = '#dfe4fc')
        text_label.grid(column = 0, row = 0, columnspan = 3, padx = 50, pady = 20)

        label_tenmon = Label(frame,text='Giá:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        label_tenmon.grid(column = 0, row = 1, padx = 50, pady = 10)

        self.entry_gia = Entry(frame, fg="white", bg = "gray", width = 50)
        self.entry_gia.grid(column = 1, row = 1, columnspan = 2, padx = 50, pady = 10)

        button_sua = Button(frame, text="Sửa", fg="white", bg="green", width= 30, command=lambda gia = self.entry_gia.get():self.xacNhanSuaGia(sua_win, TenMon, gia))
        button_sua.grid(column = 0, row = 3, columnspan = 3, padx = 50, pady = 20)

    def xacNhanSuaGia(self, Win, TenMon, Gia):
        Gia = int(self.entry_gia.get())
        sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
        sql = sql + f"EXEC @return_value = usp_SuaGiaMonAn N'{TenMon}', {Gia}"
        sql = sql + "\nselect @return_value"
        print(sql)
        check = int(self.parent.parent.cursor.execute(sql).fetchone()[0])
        self.parent.parent.cursor.commit()
        if check == 1:
            ctypes.windll.user32.MessageBoxW(0, "Sửa thành công", "Thông báo", 0)
        Win.destroy()
        self.thucdon()

    def suaSoLuong(self, TenMon):
        sua_win = Toplevel()
        frame = Frame(sua_win, bg = '#dfe4fc')

        frame.grid(column=0, row=0)

        text_label = Label(frame,text='Sửa số lượng',  fg="red", font=("Times New Roman", 30), bg = '#dfe4fc')
        text_label.grid(column = 0, row = 0, columnspan = 3, padx = 50, pady = 20)

        label_tenmon = Label(frame,text='Giá:',  fg="black", font=("Times New Roman", 13), bg = '#dfe4fc')
        label_tenmon.grid(column = 0, row = 1, padx = 50, pady = 10)

        self.entry_soluong = Entry(frame, fg="white", bg = "gray", width = 50)
        self.entry_soluong.grid(column = 1, row = 1, columnspan = 2, padx = 50, pady = 10)

        button_sua = Button(frame, text="Sửa", fg="white", bg="green", width= 30, command=lambda soluong = self.entry_soluong.get():self.xacNhanSuaSoLuong(sua_win, TenMon, soluong))
        button_sua.grid(column = 0, row = 3, columnspan = 3, padx = 50, pady = 20)

    def xacNhanSuaSoLuong(self, Win, TenMon, SoLuong):
        SoLuong = int(self.entry_soluong.get())
        sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
        sql = sql + f"EXEC @return_value = usp_SuaSoLuong1MonAn_DT N'{TenMon}', {SoLuong}"
        sql = sql + "\nselect @return_value"
        print(sql)
        check = int(self.parent.parent.cursor.execute(sql).fetchone()[0])
        self.parent.parent.cursor.commit()
        if check == 1:
            ctypes.windll.user32.MessageBoxW(0, "Sửa thành công", "Thông báo", 0)
        Win.destroy()
        self.thucdon()

    def danhsachdonhang(self):
        self.frame_clear()

        self.button_cho = Button(self.frame, text='ĐANG CHỜ', fg="white", bg="violet", width= 20, command=self.dsdangcho)
        self.button_cho.grid(column = 0, row = 2, padx = 10, pady = 20)

        self.button_danggiao = Button(self.frame, text='ĐANG GIAO', fg="white", bg="violet", width= 20, command=self.dsdanggiao)
        self.button_danggiao.grid(column = 1, row = 2, padx = 10, pady = 20)
        
        self.button_dagiao = Button(self.frame, text='ĐÃ GIAO', fg="white", bg="violet", width= 20, command=self.dsdagiao)
        self.button_dagiao.grid(column = 2, row = 2, padx = 10, pady = 20)
        
        self.button_dahuy = Button(self.frame, text='ĐÃ HỦY', fg="white", bg="violet", width= 20, command=self.dsdahuy)
        self.button_dahuy.grid(column = 3, row = 2, padx = 10, pady = 20)
        
        self.frame_info.grid(columnspan=4, row=3)
        self.button_logout.grid(row=4)

    def dsdangcho(self):
        self.frame_clear1()
        self.frame_info.grid(columnspan=4)
        i = 0
        
        self.frame_info.configure()
        
        #scrollbar
        self.canvas_frame = Canvas(self.frame_info, width=900, height=300)
        self.scrollbar_vertical = Scrollbar(self.frame_info, orient=VERTICAL, command=self.canvas_frame.yview)
        self.scrollbar_horizontal = Scrollbar(self.frame_info, orient=HORIZONTAL, command=self.canvas_frame.xview)
        self.scroll_frame = Frame(self.canvas_frame, bg='brown')
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")
            )
        )

        self.canvas_frame.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas_frame.configure(yscrollcommand=self.scrollbar_vertical.set, xscrollcommand=self.scrollbar_horizontal.set)
        
        #Đặt các nhãn cần in thông tin
        list_label_text = ['Mã đơn hàng', 'Tên khách hàng', 'Tên đối tác', 'Địa chỉ chi nhánh', 'Thời gian lập', 'Địa chỉ giao hàng',
                            'Trạng thái', 'Phí sản phẩm', 'Phí vận chuyển', 'Tổng tiền', 'Thanh toán', 'Thời gian giao', 'Chi tiết đơn hàng']
        for pos in range(len(list_label_text)):
            Label(self.scroll_frame, text=list_label_text[pos], bg='brown', fg='white', font=('Times New Roman', 20)).grid(column=pos, row=0)  

        i = 1
        list_info_label=[0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for a in self.parent.parent.cursor.execute(f"EXEC usp_Xem_DS_DonHang @trangthai = 1"):
            print(a)
            col = 0
            for pos in range(len(list_info_label)): 
                if list_info_label[pos] == 7:
                    if a[list_info_label[pos]] == -1:
                        a[list_info_label[pos]] = 'Đã hủy'
                    elif a[list_info_label[pos]] == 1:
                        a[list_info_label[pos]] = 'Đang chờ tiếp nhận'
                    if a[list_info_label[pos]] == 2:
                        a[list_info_label[pos]] = 'Đang vận chuyển'
                    if a[list_info_label[pos]] == 3:
                        a[list_info_label[pos]] = 'Đã giao hàng'
                label = Label(self.scroll_frame, text=a[list_info_label[pos]], bg='#ff7f50', font=('Times New Roman', 20))
                label.grid(column=pos, row=i)
                col = pos + 1

            button_xacnhan = Button(self.scroll_frame, text='Chi tiết', width=10, bg='teal', command=lambda madon = a[0]:self.chitiet(madon))
            button_xacnhan.grid(column=col, row=i, padx=10, pady=10)
            i += 1

        self.scrollbar_horizontal.pack(side='bottom', fill='x')
        self.scrollbar_vertical.pack(side='right', fill='y')
        self.canvas_frame.pack(side="left", fill="both", expand=True)

    def chitiet(self, madon):
        chitiet_win = Toplevel()
        label_tenmon = Label(chitiet_win, text=madon, font=('Times New Roman', 20), fg='red')
        label_tenmon.pack()

        #scrollbar
        canvas_frame = Canvas(chitiet_win, width=900)
        scrollbar_vertical = Scrollbar(chitiet_win, orient='vertical', command=canvas_frame.yview)
        scroll_frame = Frame(canvas_frame)
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas_frame.configure(
                scrollregion=canvas_frame.bbox("all")
            )
        )

        canvas_frame.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas_frame.configure(yscrollcommand=scrollbar_vertical.set)
           
        label_monan = Label(scroll_frame, text='Mã đối tác', width=10, bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=0, row=0)

        label_monan = Label(scroll_frame, text='Tên món', width=10, bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=1, row=0)
                
        label_monan = Label(scroll_frame, text='Mã đơn', width=10, bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=2, row=0)

        label_monan = Label(scroll_frame, text='Số lượng', width=10, bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=3, row=0)

        label_monan = Label(scroll_frame, text='Tổng giá', width=10, bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=4, row=0)

        i = 1

        for a in self.parent.parent.cursor.execute(f'USP_XEMCHITIETDONHANG {madon}'):      
            label_monan = Label(scroll_frame, text=a[0], width=10, bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=0, row=i)

            label_monan = Label(scroll_frame, text=a[1], width=10, bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=1, row=i)
            
            label_monan = Label(scroll_frame, text=a[2], width=10, bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=2, row=i)

            label_monan = Label(scroll_frame, text=a[3], width=10, bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=3, row=i)

            label_monan = Label(scroll_frame, text=a[4], width=10, bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=4, row=i)

            i += 1
        
        canvas_frame.pack(side="left", fill="both", expand=True)
        scrollbar_vertical.pack(side='right', fill='y')

    def dsdahuy(self):
        self.frame_clear1()
        self.frame_info.grid(columnspan=4)
        
        self.frame_info.configure()
        
        #scrollbar
        self.canvas_frame = Canvas(self.frame_info, width=900, height=300)
        self.scrollbar_vertical = Scrollbar(self.frame_info, orient=VERTICAL, command=self.canvas_frame.yview)
        self.scrollbar_horizontal = Scrollbar(self.frame_info, orient=HORIZONTAL, command=self.canvas_frame.xview)
        self.scroll_frame = Frame(self.canvas_frame, bg='brown')
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")
            )
        )

        self.canvas_frame.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas_frame.configure(yscrollcommand=self.scrollbar_vertical.set, xscrollcommand=self.scrollbar_horizontal.set)
        
         #Đặt các nhãn cần in thông tin
        list_label_text = ['Mã đơn hàng', 'Tên khách hàng', 'Tên đối tác', 'Địa chỉ chi nhánh', 'Thời gian lập', 'Địa chỉ giao hàng',
                            'Trạng thái', 'Phí sản phẩm', 'Phí vận chuyển', 'Tổng tiền', 'Thanh toán', 'Thời gian giao', 'Chi tiết đơn hàng']
        for pos in range(len(list_label_text)):
            Label(self.scroll_frame, text=list_label_text[pos], bg='brown', fg='white', font=('Times New Roman', 20)).grid(column=pos, row=0)  

        i = 1
        list_info_label=[0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for a in self.parent.parent.cursor.execute(f"EXEC usp_Xem_DS_DonHang @trangthai = -1"):
            print(a)
            col = 0
            for pos in range(len(list_info_label)): 
                if list_info_label[pos] == 7:
                    if a[list_info_label[pos]] == -1:
                        a[list_info_label[pos]] = 'Đã hủy'
                    elif a[list_info_label[pos]] == 1:
                        a[list_info_label[pos]] = 'Đang chờ tiếp nhận'
                    if a[list_info_label[pos]] == 2:
                        a[list_info_label[pos]] = 'Đang vận chuyển'
                    if a[list_info_label[pos]] == 3:
                        a[list_info_label[pos]] = 'Đã giao hàng'
                label = Label(self.scroll_frame, text=a[list_info_label[pos]], bg='#ff7f50', font=('Times New Roman', 20))
                label.grid(column=pos, row=i)
                col = pos + 1

            button_xacnhan = Button(self.scroll_frame, text='Chi tiết', width=10, bg='teal', command=lambda madon = a[0]:self.chitiet(madon))
            button_xacnhan.grid(column=col, row=i, padx=10, pady=10)
            i += 1

        self.scrollbar_horizontal.pack(side='bottom', fill='x')
        self.scrollbar_vertical.pack(side='right', fill='y')
        self.canvas_frame.pack(side="left", fill="both", expand=True)
        pass

    def dsdagiao(self):
        self.frame_clear1()
        self.frame_info.grid(columnspan=4)
        i = 0
        
        self.frame_info.configure()
        
        #scrollbar
        self.canvas_frame = Canvas(self.frame_info, width=900, height=300)
        self.scrollbar_vertical = Scrollbar(self.frame_info, orient=VERTICAL, command=self.canvas_frame.yview)
        self.scrollbar_horizontal = Scrollbar(self.frame_info, orient=HORIZONTAL, command=self.canvas_frame.xview)
        self.scroll_frame = Frame(self.canvas_frame, bg='brown')
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")
            )
        )

        self.canvas_frame.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas_frame.configure(yscrollcommand=self.scrollbar_vertical.set, xscrollcommand=self.scrollbar_horizontal.set)
           
         #Đặt các nhãn cần in thông tin
        list_label_text = ['Mã đơn hàng', 'Tên khách hàng', 'Tên tài xế', 'Tên đối tác', 'Địa chỉ chi nhánh', 'Thời gian lập', 'Địa chỉ giao hàng',
                            'Trạng thái', 'Phí sản phẩm', 'Phí vận chuyển', 'Tổng tiền', 'Thanh toán', 'Thời gian giao', 'Chi tiết đơn hàng']
        for pos in range(len(list_label_text)):
            Label(self.scroll_frame, text=list_label_text[pos], bg='brown', fg='white', font=('Times New Roman', 20)).grid(column=pos, row=0)  

        i = 1
        list_info_label=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for a in self.parent.parent.cursor.execute(f"EXEC usp_Xem_DS_DonHang @trangthai = 3"):
            print(a)
            col = 0
            for pos in range(len(list_info_label)): 
                if list_info_label[pos] == 7:
                    if a[list_info_label[pos]] == -1:
                        a[list_info_label[pos]] = 'Đã hủy'
                    elif a[list_info_label[pos]] == 1:
                        a[list_info_label[pos]] = 'Đang chờ tiếp nhận'
                    if a[list_info_label[pos]] == 2:
                        a[list_info_label[pos]] = 'Đang vận chuyển'
                    if a[list_info_label[pos]] == 3:
                        a[list_info_label[pos]] = 'Đã giao hàng'
                label = Label(self.scroll_frame, text=a[list_info_label[pos]], bg='#ff7f50', font=('Times New Roman', 20))
                label.grid(column=pos, row=i)
                col = pos + 1

            button_xacnhan = Button(self.scroll_frame, text='Chi tiết', width=10, bg='teal', command=lambda madon = a[0]:self.chitiet(madon))
            button_xacnhan.grid(column=col, row=i, padx=10, pady=10)
            i += 1


        self.scrollbar_horizontal.pack(side='bottom', fill='x')
        self.scrollbar_vertical.pack(side='right', fill='y')
        self.canvas_frame.pack(side="left", fill="both", expand=True)
        pass

    def dsdanggiao(self):
        self.frame_clear1()
        self.frame_info.grid(columnspan=4)
        self.frame_info.configure()
        
        #scrollbar
        self.canvas_frame = Canvas(self.frame_info, width=900, height=300)
        self.scrollbar_vertical = Scrollbar(self.frame_info, orient=VERTICAL, command=self.canvas_frame.yview)
        self.scrollbar_horizontal = Scrollbar(self.frame_info, orient=HORIZONTAL, command=self.canvas_frame.xview)
        self.scroll_frame = Frame(self.canvas_frame, bg='brown')
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")
            )
        )

        self.canvas_frame.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas_frame.configure(yscrollcommand=self.scrollbar_vertical.set, xscrollcommand=self.scrollbar_horizontal.set)

         #Đặt các nhãn cần in thông tin
        list_label_text = ['Mã đơn hàng', 'Tên khách hàng', 'Tên tài xế', 'Tên đối tác', 'Địa chỉ chi nhánh', 'Thời gian lập', 'Địa chỉ giao hàng',
                            'Trạng thái', 'Phí sản phẩm', 'Phí vận chuyển', 'Tổng tiền', 'Thanh toán', 'Thời gian giao', 'Chi tiết đơn hàng']
        for pos in range(len(list_label_text)):
            Label(self.scroll_frame, text=list_label_text[pos], bg='brown', fg='white', font=('Times New Roman', 20)).grid(column=pos, row=0)  

        i = 1
        list_info_label=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for a in self.parent.parent.cursor.execute(f"EXEC usp_Xem_DS_DonHang @trangthai = 2"):
            print(a)
            col = 0
            for pos in range(len(list_info_label)): 
                if list_info_label[pos] == 7:
                    if a[list_info_label[pos]] == -1:
                        a[list_info_label[pos]] = 'Đã hủy'
                    elif a[list_info_label[pos]] == 1:
                        a[list_info_label[pos]] = 'Đang chờ tiếp nhận'
                    if a[list_info_label[pos]] == 2:
                        a[list_info_label[pos]] = 'Đang vận chuyển'
                    if a[list_info_label[pos]] == 3:
                        a[list_info_label[pos]] = 'Đã giao hàng'
                label = Label(self.scroll_frame, text=a[list_info_label[pos]], bg='#ff7f50', font=('Times New Roman', 20))
                label.grid(column=pos, row=i)
                col = pos + 1

            button_xacnhan = Button(self.scroll_frame, text='Chi tiết', width=10, bg='teal', command=lambda madon = a[0]:self.chitiet(madon))
            button_xacnhan.grid(column=col, row=i, padx=10, pady=10)
            i += 1


        self.scrollbar_horizontal.pack(side='bottom', fill='x')
        self.scrollbar_vertical.pack(side='right', fill='y')
        self.canvas_frame.pack(side="left", fill="both", expand=True)

    def frame_clear(self):
        if self.button_thongtin != None and self.button_hopdong != None:
            if self.button_thongtin.winfo_exists():
                self.button_thongtin.destroy()

            if self.button_hopdong.winfo_exists():
                self.button_hopdong.destroy()
        
        if self.button_themmon != None and self.button_xoamon != None:
            if self.button_themmon.winfo_exists():
                self.button_themmon.destroy()

            if self.button_xoamon.winfo_exists():
                self.button_xoamon.destroy()
       
        if self.button_themcuahang != None and self.button_xoacuahang != None:
            if self.button_themcuahang.winfo_exists():
                self.button_themcuahang.destroy()

            if self.button_xoacuahang.winfo_exists():
                self.button_xoacuahang.destroy()

        if self.button_danggiao != None and self.button_dagiao != None and self.button_cho != None and self.button_dahuy != None:
            if self.button_danggiao.winfo_exists():
                self.button_danggiao.destroy()

            if self.button_dagiao.winfo_exists():
                self.button_dagiao.destroy()

            if self.button_dahuy.winfo_exists():
                self.button_dahuy.destroy()

            if self.button_cho.winfo_exists():
                self.button_cho.destroy()

        return super().frame_clear()

    def frame_clear1(self):
        return super().frame_clear()
