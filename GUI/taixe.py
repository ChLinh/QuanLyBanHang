from info_ui import *

class TX_Info_UI(Info_UI):
    def __init__(self, parent):
        super().__init__(parent)

        self.label_text.configure(text='Tài xế')
        self.button_info1.configure(text='THÔNG TIN', command=self.thongtin)
        self.button_info2.configure(text='CHỌN ĐƠN HÀNG', command=self.chondonhang)
        self.button_info3.configure(text='XEM THU NHẬP', command=self.xemthunhap)
        self.button_info4 = Button(self.frame, text='DANH SÁCH ĐƠN HÀNG', fg="white", bg="green", width= 30, command=self.xemdanhsachdon)
        self.button_info4.grid(column = 3, row = 1, padx = 10, pady = 20)
        self.button_danggiao = None
        self.button_dagiao = None

        self.label_text.grid(column=0, row=0, columnspan=4)
        self.frame_info.grid(columnspan=4)

    def thongtin(self):
        self.frame_clear()
        for a in self.parent.parent.cursor.execute("exec usp_XemThongTinTaiXe"):#SUA LAI
            label_info = Label(self.frame_info, text='Mã tài xế: '+a[0], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=0, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Mã tài khoản ngân hàng: '+a[1], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=1, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Tên tài xế: '+a[2], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=2, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Số điện thoại: '+a[3], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=3, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Địa chỉ: '+a[4], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=4, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Email: '+a[5], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=5, padx=10, pady=10)
        pass

    def chondonhang(self):
        self.frame_clear()
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

        list_label_text = ['Mã đơn hàng', 'Tên khách hàng', 'Tên đối tác', 'Địa chỉ chi nhánh', 'Thời gian lập', 'Địa chỉ giao hàng',
                            'Trạng thái', 'Phí sản phẩm', 'Phí vận chuyển', 'Tổng tiền', 'Thanh toán', 'Thời gian giao', 'Chi tiết đơn hàng', 'Chọn đơn']
        for pos in range(len(list_label_text)):
            Label(self.scroll_frame, text=list_label_text[pos], bg='brown', fg='white', font=('Times New Roman', 20)).grid(column=pos, row=0)  

        i = 1
        list_info_label=[0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for a in self.parent.parent.cursor.execute(f"EXEC usp_XemDanhSachDHTheoKhuVuc"):
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

            button_them = Button(self.scroll_frame, text='Chọn', width=10, bg='teal', command=lambda madon = a[0]:self.xacnhandonhang(madon))
            button_them.grid(column=13, row=i, padx=10, pady=10)
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

    def xacnhandonhang(self, madh):
        sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
        sql = sql + f"EXEC @return_value = usp_ChonDonHang {madh}"
        sql = sql + "\nselect @return_value"
        try:
            check = int(self.parent.parent.cursor.execute(sql).fetchone()[0])
            self.parent.parent.cursor.commit()
        except:
            check = 0
        if check == 1:
            ctypes.windll.user32.MessageBoxW(0, "Chọn đơn hàng thành công", "Thông báo", 0)
            self.xemdanhsachdon()
        elif check == 0:
            ctypes.windll.user32.MessageBoxW(0, "Chọn đơn hàng thất bại", "Thông báo", 0)

    def xemthunhap(self):
        self.frame_clear()
        for a in self.parent.parent.cursor.execute(f'EXEC usp_XemTaiKhoanNganHang'):
            label_info = Label(self.frame_info, text='Mã tài khoản ngân hàng: ' + a[0], font=('Arial', 20), width= 50, bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=0, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Mã ngân hàng ' + a[1], font=('Arial', 20), width= 50, bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=1, padx=10, pady=10)
            if a[2] == None:
                a[2] = 'Null'
            label_info = Label(self.frame_info, text='Ngày lập: ' + a[2], font=('Arial', 20), width= 50, bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=2, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Số dư: ' + str(a[3]), font=('Arial', 20), width= 50, bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=3, padx=10, pady=10)
        pass

    def xemdanhsachdon(self):
        self.frame_clear()
        self.button_danggiao = Button(self.frame, text='DANH SÁCH ĐANG GIAO', fg="white", bg="violet", width= 60, command=self.danhsachdanggiao)
        self.button_danggiao.grid(column = 0, columnspan=2, row = 2, padx = 10, pady = 20)
        
        self.button_dagiao = Button(self.frame, text='DANH SÁCH ĐÃ GIAO', fg="white", bg="violet", width= 60, command=self.danhsachdagiao)
        self.button_dagiao.grid(column = 2, columnspan=2, row = 2, padx = 10, pady = 20)
        
        self.frame_info.grid(columnspan=4, row=3)
        pass

    def danhsachdanggiao(self):
        self.frame_clear1()
        self.frame_info.grid(columnspan=4, )
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

        list_label_text = ['Mã đơn hàng', 'Tên khách hàng', 'Tên đối tác', 'Địa chỉ chi nhánh', 'Thời gian lập', 'Địa chỉ giao hàng',
                            'Trạng thái', 'Phí sản phẩm', 'Phí vận chuyển', 'Tổng tiền', 'Thanh toán', 'Thời gian giao', 'Chi tiết đơn hàng', 'Xác nhận đã giao']
        for pos in range(len(list_label_text)):
            Label(self.scroll_frame, text=list_label_text[pos], bg='brown', fg='white', font=('Times New Roman', 20)).grid(column=pos, row=0)  

        i = 1
        list_info_label=[0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for a in self.parent.parent.cursor.execute(f"exec usp_XemDanhSachDHDangGiao"):
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

            button_xacnhan = Button(self.scroll_frame, text='Xác nhận', width=10, bg='teal', command=lambda madon = a[0]:self.chuyenQuaDaGiao(madon))
            button_xacnhan.grid(column=col+1, row=i, padx=10, pady=10)
            i += 1

        self.scrollbar_horizontal.pack(side='bottom', fill='x')
        self.scrollbar_vertical.pack(side='right', fill='y')
        self.canvas_frame.pack(side="left", fill="both", expand=True)
        pass

    def chuyenQuaDaGiao(self, madon):
        sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
        sql = sql + f"EXEC @return_value = usp_ChuyenThanhDaGiaoHang '{madon}'"
        sql = sql + "\nselect @return_value"
        print(sql)
        check = int(self.parent.parent.cursor.execute(sql).fetchone()[0])
        self.parent.parent.cursor.commit()
        if check == 1:
            ctypes.windll.user32.MessageBoxW(0, "Vận chuyển thành công", "Thông báo", 0)
            self.danhsachdagiao()
        elif check == 0:
            ctypes.windll.user32.MessageBoxW(0, "Vận chuyển không thành công", "Thông báo", 0)

    def danhsachdagiao(self):
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
        list_label_text = ['Mã đơn hàng', 'Tên khách hàng', 'Tên đối tác', 'Địa chỉ chi nhánh', 'Thời gian lập', 'Địa chỉ giao hàng',
                            'Trạng thái', 'Phí sản phẩm', 'Phí vận chuyển', 'Tổng tiền', 'Thanh toán', 'Thời gian giao', 'Chi tiết đơn hàng']
        for pos in range(len(list_label_text)):
            Label(self.scroll_frame, text=list_label_text[pos], bg='brown', fg='white', font=('Times New Roman', 20)).grid(column=pos, row=0)  

        i = 1
        list_info_label=[0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for a in self.parent.parent.cursor.execute(f"EXEC usp_XemDanhSachDHDaGiao"):
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

    def frame_clear(self):
        if self.button_danggiao != None and self.button_dagiao != None:
            if self.button_danggiao.winfo_exists():
                self.button_danggiao.destroy()

            if self.button_dagiao.winfo_exists():
                self.button_dagiao.destroy()

        return super().frame_clear()

    def frame_clear1(self):
        return super().frame_clear()
