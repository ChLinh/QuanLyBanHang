from info_ui import *

class KH_Info_UI(Info_UI):
    def __init__(self, parent):
        super().__init__(parent)

        self.button_cart = None
        self.button_return = None
        
        self.button_danggiao = None
        self.button_dagiao = None
        self.button_cho = None
        self.button_dahuy = None

        self.label_text.configure(text='Khách hàng')
        self.button_info1.configure(text='THÔNG TIN', command=self.thongtin)
        self.button_info2.configure(text='ĐẶT ĐỒ ĂN', command=self.datdoan)
        self.button_info3.configure(text='ĐƠN HÀNG', command=self.danhsachdonhang)

    def thongtin(self):
        self.frame_clear()
        for a in self.parent.parent.cursor.execute(f'EXEC USP_XEMKHACHHANG'):
            label_info = Label(self.frame_info, text='Mã khách hàng: ' + a[0], font=('Arial', 20), width= 50, bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=0, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Mã tài khoản ngân hàng: ' + a[1], font=('Arial', 20), width= 50, bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=1, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Tên khách hàng: ' + a[2], font=('Arial', 20), width= 50, bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=2, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Số điện thoại: ' + a[3], font=('Arial', 20), width= 50, bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=3, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Địa chỉ: ' + a[4], font=('Arial', 20), width= 50, bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=4, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Email: ' + a[5], font=('Arial', 20), width= 50, bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=5, padx=10, pady=10)
        pass

    def datdoan(self):
        self.frame_clear()

        self.frame_info.grid(columnspan=3)
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


        list_label_text = ['Tên cửa hàng', 'Địa chỉ cửa hàng', 'Thời gian mở cửa', 'Thời gian đóng cửa', 'Tình trạng', 'Chọn']

        for pos in range(len(list_label_text)):
            Label(self.scroll_frame, text=list_label_text[pos], bg='brown', fg='white', font=('Times New Roman', 20)).grid(column=pos, row=0)  

        i = 1
        list_info_label=[2, 1, 3, 4, 5]
        count = 100
        for a in self.parent.parent.cursor.execute(f"exec USP_XEMDANHSACHCUAHANG"):
            check = 1
            col = 0
            for pos in range(len(list_info_label)): 
                if list_info_label[pos] == 5:
                    if a[list_info_label[pos]] == 1:
                        a[list_info_label[pos]] = 'Mở cửa'
                    elif a[list_info_label[pos]] == 0:
                        a[list_info_label[pos]] = 'Tạm nghỉ'
                        check = 0
                    if a[list_info_label[pos]] == -1:
                        a[list_info_label[pos]] = 'Đóng cửa'
                        check = 0
                label = Label(self.scroll_frame, text=a[list_info_label[pos]], bg='#ff7f50', font=('Times New Roman', 20))
                label.grid(column=pos, row=i)
                col = pos + 1

            if check == 1:
                button_xacnhan = Button(self.scroll_frame, text="Chọn", bg='green', fg="white", width=20, command=lambda madt=a[0], diachi=a[1]:self.thucdon(madt, diachi))
                button_xacnhan.grid(column=col, row=i, padx=10, pady=10)
            else:
                button_xacnhan = Button(self.scroll_frame, state=DISABLED, text="Chọn", bg='green', fg="white", width=20, command=lambda madt=a[0], diachi=a[1]:self.thucdon(madt, diachi))
                button_xacnhan.grid(column=col, row=i, padx=10, pady=10)
            i += 1

            count -= 1
            if count == 0: 
                break

        self.scrollbar_horizontal.pack(side='bottom', fill='x')
        self.scrollbar_vertical.pack(side='right', fill='y')
        self.canvas_frame.pack(side="left", fill="both", expand=True)

    def thucdon(self, madt, diachi):
        self.frame_clear()
        self.frame_info.grid(columnspan=3)
        i = 0
        
        print(f'usp_TaoDonHang {madt}, N\'{diachi}\'')
        self.parent.parent.cursor.execute(f'usp_TaoDonHang {madt}, N\'{diachi}\'')
        self.parent.parent.cursor.commit

        # Lấy ra mã đơn hàng
        for a in self.parent.parent.cursor.execute(f'USP_XEMDANHSACHDONHANG @trangthai = 0'):    
            madon = a[0]
        print(madon)
        self.parent.parent.cursor.commit()

        self.frame_info.configure()
        #scrollbar
        self.canvas_frame = Canvas(self.frame_info, width=800)
        self.scrollbar_vertical = Scrollbar(self.frame_info, orient='vertical', command=self.canvas_frame.yview)
        self.scroll_frame = Frame(self.canvas_frame)
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas_frame.configure(
                scrollregion=self.canvas_frame.bbox("all")
            )
        )

        self.canvas_frame.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas_frame.configure(yscrollcommand=self.scrollbar_vertical.set)
           
        label_monan = Label(self.scroll_frame, text='Tên món', width=10, bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=0, row=0)

        label_monan = Label(self.scroll_frame, text='Giá', width=10, bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=1, row=0)
                
        label_monan = Label(self.scroll_frame, text='Tình trạng', width=10, bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=2, row=0)

        label_monan = Label(self.scroll_frame, text='Số lượng', width=10, bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=3, row=0)

        label_monan = Label(self.scroll_frame, text='Chọn món', width=10, bg='brown', fg='white', font=('Times New Roman', 20))
        label_monan.grid(column=4, row=0)

        i = 1

        buttons = []
        for a in self.parent.parent.cursor.execute(f'USP_THUCDON {madt}'):       
            label_monan = Label(self.scroll_frame, text=a[1], width=10, bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=0, row=i)

            label_monan = Label(self.scroll_frame, text=a[3], width=10, bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=1, row=i)

            if a[4] == 1:
                stri = 'Có bán'
            elif a[4] == 0:
                stri = 'Hết hàng'
            if a[4] == -1:
                stri = 'Tạm ngưng'
            
            label_monan = Label(self.scroll_frame, text=stri, width=10, bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=2, row=i)

            label_monan = Label(self.scroll_frame, text=a[5], width=10, bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=3, row=i)

            button_them = Button(self.scroll_frame, text='Chọn món ăn', width=10, bg='teal')
            button_them.grid(column=4, row=i, padx=10, pady=10)
            button_them.configure(command=lambda monan = a[1], btn_id = button_them:self.chonmonan(madt,monan, madon, btn_id))
            buttons.append([button_them, a[1]])
            i += 1
        
        
        self.canvas_frame.pack(side="left", fill="both", expand=True)
        self.scrollbar_vertical.pack(side='right', fill='y')

        self.button_cart = Button(self.frame, text="GIỎ HÀNG", fg="white", bg="green", width= 30, command=lambda: self.xemchitietdonhang(madon, buttons))
        self.button_cart.grid(column = 1, row = 4, padx = 10, pady = 20)
        
        self.button_return = Button(self.frame, text="QUAY VỀ", fg="white", bg="green", width= 30, command=lambda: self.xoadonhangvaquayve(madon))
        self.button_return.grid(column = 2, row = 4, padx = 10, pady = 20)

    def xoadonhangvaquayve(self, madon):
        sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
        sql = sql + f"EXEC @return_value = usp_Xoa1DonHang_KH {madon}"
        sql = sql + "\nselect @return_value"
        print(sql)
        check = int(self.parent.parent.cursor.execute(sql).fetchone()[0])
        self.parent.parent.cursor.commit()
        if check == 1:
            print('Xóa thành công')
        elif check == 0:
            print('Xóa không thành công')
        self.datdoan()

    def xemchitietdonhang(self, madon, btns):
        donhang_win = Toplevel()
        label_tenmon = Label(donhang_win, text=madon, font=('Times New Roman', 20), fg='red')
        label_tenmon.pack()

        #scrollbar
        canvas_frame = Canvas(donhang_win, width=900)
        scrollbar_vertical = Scrollbar(donhang_win, orient='vertical', command=canvas_frame.yview)
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

            label_monan = Label(scroll_frame, text=a[4], width=10, bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=3, row=i)

            label_monan = Label(scroll_frame, text=a[5], width=10, bg='#ff7f50', font=('Times New Roman', 20))
            label_monan.grid(column=4, row=i)

            label_monan = Button(scroll_frame, text='Xóa món ăn', width=10, bg='teal', fg='white', 
                command=lambda madt = a[1], tenmon = a[2], madon = a[0]:self.xoamonan(donhang_win, madt, tenmon, madon, btns))
            label_monan.grid(column=5, row=i)

            i += 1
        
        canvas_frame.pack(side="left", fill="both", expand=True)
        scrollbar_vertical.pack(side='right', fill='y')

        button_xacnhan = Button(donhang_win, text='Xác nhận', width=10, bg='teal', command=lambda: self.xacnhandonhang(donhang_win, madon, i))
        button_xacnhan.pack(side='bottom', fill='x')
    
    def xoamonan(self, parent,madt, tenmon, madon, btns):
        sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
        sql = sql + f"EXEC @return_value = usp_XoaMonAnKhoiDonHang_KH {madt}, N'{tenmon}', {madon}"
        sql = sql + "\nselect @return_value"
        print(sql)
        check = int(self.parent.parent.cursor.execute(sql).fetchone()[0])
        print(check)
        self.parent.parent.cursor.commit()
        if check == 1:
            ctypes.windll.user32.MessageBoxW(0, "Xóa món ăn thành công", "Thông báo", 0)
        elif check == 0:
            ctypes.windll.user32.MessageBoxW(0, "Xóa món ăn không thành công", "Thông báo", 0)
        print(check)

        for btn in btns:
            if btn[1] == tenmon:
                btn[0].configure(state='normal')
                parent.destroy()
                self.xemchitietdonhang(madon, btns)
                break

    def xacnhandonhang(self, parent, madon, count):
        if count == 1:
            ctypes.windll.user32.MessageBoxW(0, "Không có gì trong giỏ hàng", "Thông báo", 0)
            return 0
        sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
        sql = sql + f"EXEC @return_value = USP_DATDONHANG {madon}, N'Chuyển khoản', NULL"
        sql = sql + "\nselect @return_value"
        check = int(self.parent.parent.cursor.execute(sql).fetchone()[0])
        self.parent.parent.cursor.commit()
        if check == 1:
            ctypes.windll.user32.MessageBoxW(0, "Đặt đơn hàng thành công", "Thông báo", 0)
        elif check == 2:
            ctypes.windll.user32.MessageBoxW(0, "Đã xảy ra lỗi khi đặt đơn hàng", "Thông báo", 0)
        
        parent.destroy()
        self.datdoan()

    def chonmonan(self, madt, tenmon, madon, btn):
        chonmonan_win = Toplevel()
        self.soluongmonan = 1
        label_tenmon = Label(chonmonan_win, text=tenmon, font=('Times New Roman', 20), fg='red')
        label_tenmon.grid(column=0, row=0)

        label_soluong = Label(chonmonan_win, text="Số lượng: " + str(self.soluongmonan), font=('Times New Roman', 20), fg='black')
        label_soluong.grid(column=1, row=0)

        button_them = Button(chonmonan_win, text='+', width=10, bg='teal', command=lambda:self.tangsoluong(label_soluong))
        button_them.grid(column=0, row=1, padx=10)

        button_xoa = Button(chonmonan_win, text='-', width=10, bg='teal', command=lambda:self.giamsoluong(label_soluong))
        button_xoa.grid(column=1, row=1, padx=10)

        button_xacnhan = Button(chonmonan_win, text='Xác nhận', width=10, bg='teal', command=lambda: [self.xacnhanmonan(chonmonan_win, madt, tenmon, madon), btn.configure(state='disabled')])
        button_xacnhan.grid(column=0, row=2, columnspan=2, padx=10, pady=10)
        
        pass

    def tangsoluong(self, label):
        self.soluongmonan += 1
        label.configure(text="Số lượng: " + str(self.soluongmonan))
        pass

    def giamsoluong(self, label):
        if(self.soluongmonan > 1):
            self.soluongmonan -= 1
            label.configure(text="Số lượng: " + str(self.soluongmonan))
        pass

    def xacnhanmonan(self, parent, madt, tenmon, madon):
        sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
        sql = sql + f"EXEC @return_value = usp_ThemMonAnVaoDonHang {madt}, N'{tenmon}', {madon}, {self.soluongmonan}"
        sql = sql + "\nselect @return_value"
        check = int(self.parent.parent.cursor.execute(sql).fetchone()[0])
        self.parent.parent.cursor.commit()
        if check == 1:
            ctypes.windll.user32.MessageBoxW(0, "Xác nhận món ăn thành công", "Thông báo", 0)
        print(check)
        parent.destroy()

    def danhsachdonhang(self):
        self.frame_clear()

        self.button_cho = Button(self.frame, text='ĐANG CHỜ', fg="white", bg="violet", width= 20, command=self.dsdangcho)
        self.button_cho.grid(column = 0, row = 2, padx = 10, pady = 20)

        self.button_danggiao = Button(self.frame, text='ĐANG GIAO', fg="white", bg="violet", width= 20, command=self.dsdanggiao)
        self.button_danggiao.grid(column = 0, row = 3, padx = 10, pady = 20)
        
        self.button_dagiao = Button(self.frame, text='ĐÃ GIAO', fg="white", bg="violet", width= 20, command=self.dsdagiao)
        self.button_dagiao.grid(column = 2, row = 2, padx = 10, pady = 20)
        
        self.button_dahuy = Button(self.frame, text='ĐÃ HỦY', fg="white", bg="violet", width= 20, command=self.dsdahuy)
        self.button_dahuy.grid(column = 2, row = 3, padx = 10, pady = 20)
        
        self.frame_info.grid(columnspan=3, row=4)
        self.button_logout.grid(row=5)

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

        list_label_text = ['Mã đơn hàng', 'Tên khách hàng', 'Tên đối tác', 'Địa chỉ chi nhánh', 'Thời gian lập', 'Địa chỉ giao hàng',
                            'Trạng thái', 'Phí sản phẩm', 'Phí vận chuyển', 'Tổng tiền', 'Thanh toán', 'Thời gian giao', 'Chi tiết đơn hàng', 'Hủy đơn']
        for pos in range(len(list_label_text)):
            Label(self.scroll_frame, text=list_label_text[pos], bg='brown', fg='white', font=('Times New Roman', 20)).grid(column=pos, row=0)  

        i = 1
        list_info_label=[0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for a in self.parent.parent.cursor.execute(f"EXEC USP_XEMDANHSACHDONHANG @trangthai = 1"):
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

            button_xacnhan = Button(self.scroll_frame, text='Hủy', width=10, bg='teal', command=lambda madon = a[0]:self.huyDon(madon))
            button_xacnhan.grid(column=col+1, row=i, padx=10, pady=10)
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

    def huyDon(self, madon):
        sql = f"SET NOCOUNT ON\ndeclare @return_value int\n"
        sql = sql + f"EXEC @return_value = usp_HuyDonHang_KH {madon}"
        sql = sql + "\nselect @return_value"
        try:
            check = int(self.parent.parent.cursor.execute(sql).fetchone()[0])
            self.parent.parent.cursor.commit()
        except:
            check = 0
        if check == 1:
            ctypes.windll.user32.MessageBoxW(0, "Hủy đơn thành công", "Thông báo", 0)
            self.dsdahuy()
        elif check == 0: 
            ctypes.windll.user32.MessageBoxW(0, "Hủy không đơn thành công", "Thông báo", 0)

    def dsdahuy(self):
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
        for a in self.parent.parent.cursor.execute(f"EXEC USP_XEMDANHSACHDONHANG @trangthai = -1"):
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

        list_label_text = ['Mã đơn hàng', 'Tên khách hàng', 'Tên tài xế', 'Tên đối tác', 'Địa chỉ chi nhánh', 'Thời gian lập', 'Địa chỉ giao hàng',
                            'Trạng thái', 'Phí sản phẩm', 'Phí vận chuyển', 'Tổng tiền', 'Thanh toán', 'Thời gian giao', 'Chi tiết đơn hàng']
        for pos in range(len(list_label_text)):
            Label(self.scroll_frame, text=list_label_text[pos], bg='brown', fg='white', font=('Times New Roman', 20)).grid(column=pos, row=0)  

        i = 1
        list_info_label=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for a in self.parent.parent.cursor.execute(f"EXEC USP_XEMDANHSACHDONHANG @trangthai = 3"):
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
           
        list_label_text = ['Mã đơn hàng', 'Tên khách hàng', 'Tên tài xế', 'Tên đối tác', 'Địa chỉ chi nhánh', 'Thời gian lập', 'Địa chỉ giao hàng',
                            'Trạng thái', 'Phí sản phẩm', 'Phí vận chuyển', 'Tổng tiền', 'Thanh toán', 'Thời gian giao', 'Chi tiết đơn hàng']
        for pos in range(len(list_label_text)):
            Label(self.scroll_frame, text=list_label_text[pos], bg='brown', fg='white', font=('Times New Roman', 20)).grid(column=pos, row=0)  

        i = 1
        list_info_label=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for a in self.parent.parent.cursor.execute(f"EXEC USP_XEMDANHSACHDONHANG @trangthai = 2"):
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
        if self.button_return != None and self.button_cart != None:
            if self.button_cart.winfo_exists():
                self.button_cart.destroy()

            if self.button_return.winfo_exists():
                self.button_return.destroy()

        if self.button_danggiao != None and self.button_dagiao != None and self.button_cho != None and self.button_dahuy != None:
            if self.button_danggiao.winfo_exists():
                self.button_danggiao.destroy()

            if self.button_dagiao.winfo_exists():
                self.button_dagiao.destroy()

            if self.button_dahuy.winfo_exists():
                self.button_dahuy.destroy()

            if self.button_cho.winfo_exists():
                self.button_cho.destroy()
        self.frame_info.grid(row=3)
        self.button_logout.grid(row=4)
        
        return super().frame_clear()

    def frame_clear1(self):
        return super().frame_clear()