from info_ui import *

class NV_Info_UI(Info_UI):
    def __init__(self, parent):
        super().__init__(parent)

        self.label_text.configure(text='Nhân viên')
        self.button_info1.configure(text='THÔNG TIN', command=self.thongtin)
        self.button_info2.configure(text='DANH SÁCH HỢP ĐỒNG', command=self.danhsachhopdong)
        self.button_info3.configure(text='DUYỆT HỢP ĐỒNG', command=self.duyethopdong)

        self.button_info3 = Button(self.frame, text='GIA HẠN HỢP ĐỒNG', fg="white", bg="green", width= 30, command=self.giahanhopdong)
        self.button_info3.grid(column = 3, row = 1, padx = 10, pady = 20)

        self.label_text.grid(columnspan=4)
        self.frame_info.grid(columnspan=4)

    def thongtin(self):
        self.frame_clear()
        for a in self.parent.parent.cursor.execute("exec usp_XemThongTin"):
            label_info = Label(self.frame_info, text='Mã nhân viên: ' + a[0], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=0, padx=10, pady=10)
            if a[1] == None:
                a[1] = 'Null'
            label_info = Label(self.frame_info, text='Tên nhân viên: ' + a[1], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=1, padx=10, pady=10)
            label_info = Label(self.frame_info, text='Loại nhân viên: ' + a[2], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=2, padx=10, pady=10)
        pass

    def danhsachhopdong(self):
        self.frame_clear()
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
        list_label_text = ['Mã hợp đồng', 'Thời gian lập', 'Thời gian hết hạn', 'Mã thuế', 'Người đại diện', 'Số chi nhánh', 'Phần trăm hoa hồng']
        for pos in range(len(list_label_text)):
            Label(self.scroll_frame, text=list_label_text[pos], bg='brown', fg='white', font=('Times New Roman', 20)).grid(column=pos, row=0)  

        i = 1
        list_info_label=[0, 5, 6, 7, 8, 9, 10]
        for a in self.parent.parent.cursor.execute(f"EXEC usp_XemHopDongDaLap"):
            print(a)
            col = 0
            for pos in range(len(list_info_label)): 
                if list_info_label[pos] == 10:
                    a[list_info_label[pos]] = str(a[list_info_label[pos]]) + '%'
                label = Label(self.scroll_frame, text=a[list_info_label[pos]], bg='#ff7f50', font=('Times New Roman', 20))
                label.grid(column=pos, row=i)
                col = pos + 1
            i += 1

        self.scrollbar_horizontal.pack(side='bottom', fill='x')
        self.scrollbar_vertical.pack(side='right', fill='y')
        self.canvas_frame.pack(side="left", fill="both", expand=True)

    def duyethopdong(self):
        self.frame_clear()
        #label_text
        label_MAHD = Label(self.frame_info, text='Mã hợp đồng:', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=0, padx=10, pady=10)
        label_MADT = Label(self.frame_info, text='Mã đối tác:', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=1, padx=10, pady=10)
        label_TGBT = Label(self.frame_info, text='Thời gian bắt đầu:', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=2, padx=10, pady=10)
        label_TGKT = Label(self.frame_info, text='Thời gian kết thúc:', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=3, padx=10, pady=10)
        label_NGDD = Label(self.frame_info, text='Người đại diện:', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=4, padx=10, pady=10)
        label_SoCH = Label(self.frame_info, text='Số cửa hàng:', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=5, padx=10, pady=10)
        label_PHI = Label(self.frame_info, text='Phí:', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=6, padx=10, pady=10)

        #ENTRY
        self.entry_MAHD = Entry(self.frame_info, bg='white', fg='black').grid(column=1, row=0, padx=10, pady=10)
        self.entry_MADT = Entry(self.frame_info, bg='white', fg='black').grid(column=1, row=1, padx=10, pady=10)
        self.entry_TGBT = Entry(self.frame_info, bg='white', fg='black').grid(column=1, row=2, padx=10, pady=10)
        self.entry_TGKT = Entry(self.frame_info, bg='white', fg='black').grid(column=1, row=3, padx=10, pady=10)
        self.entry_NGDD = Entry(self.frame_info, bg='white', fg='black').grid(column=1, row=4, padx=10, pady=10)
        self.entry_SoCH = Entry(self.frame_info, bg='white', fg='black').grid(column=1, row=5, padx=10, pady=10)
        self.entry_PHI = Entry(self.frame_info, bg='white', fg='black').grid(column=1, row=6, padx=10, pady=10)

        #button
        button_duyet = Button(self.frame_info, text="Duyệt", fg="white", bg="green", width= 30, command=self.takeinfo).grid(column = 0, row = 7, padx = 10, pady = 10, columnspan=2)
        pass

    def takeinfo(self):
        mahd = self.entry_MAHD.get()
        madt = self.entry_MADT.get()
        tgbt = self.entry_TGBT.get()
        tgkt = self.entry_TGKT.get()
        ngdd = self.entry_NGDD.get()
        soch = self.entry_SoCH.get()
        phi = self.entry_PHI.get()

        for a in self.parent.parent.cursor.execute("CHUC NANG"):
            pass
        pass

    def giahanhopdong(self):
        self.frame_clear()
        #label_text
        label_MAHD = Label(self.frame_info, text='Mã hợp đồng:', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=0, padx=10, pady=10)
        label_MADT = Label(self.frame_info, text='Mã đối tác:', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=1, padx=10, pady=10)
        label_TGBT = Label(self.frame_info, text='Thời gian bắt đầu:', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=2, padx=10, pady=10)
        label_TGKT = Label(self.frame_info, text='Thời gian kết thúc:', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=3, padx=10, pady=10)
        label_NGDD = Label(self.frame_info, text='Người đại diện:', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=4, padx=10, pady=10)
        label_SoCH = Label(self.frame_info, text='Số cửa hàng:', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=5, padx=10, pady=10)
        label_PHI = Label(self.frame_info, text='Phí:', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=6, padx=10, pady=10)

        #ENTRY
        self.entry_MAHD = Entry(self.frame_info, bg='white', fg='black').grid(column=1, row=0, padx=10, pady=10)
        self.entry_MADT = Entry(self.frame_info, bg='white', fg='black').grid(column=1, row=1, padx=10, pady=10)
        self.entry_TGBT = Entry(self.frame_info, bg='white', fg='black').grid(column=1, row=2, padx=10, pady=10)
        self.entry_TGKT = Entry(self.frame_info, bg='white', fg='black').grid(column=1, row=3, padx=10, pady=10)
        self.entry_NGDD = Entry(self.frame_info, bg='white', fg='black').grid(column=1, row=4, padx=10, pady=10)
        self.entry_SoCH = Entry(self.frame_info, bg='white', fg='black').grid(column=1, row=5, padx=10, pady=10)
        self.entry_PHI = Entry(self.frame_info, bg='white', fg='black').grid(column=1, row=6, padx=10, pady=10)

        #button
        button_duyet = Button(self.frame_info, text="Gia hạn", fg="white", bg="green", width= 30, command=self.takeinfo).grid(column = 0, row = 7, padx = 10, pady = 10, columnspan=2)
        pass


    
    def frame_clear1(self):
        return super().frame_clear()
