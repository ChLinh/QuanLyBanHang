label_info = Label(self.frame_info, text='Tên cửa hàng', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=0, padx=10, pady=10)
        label_info = Label(self.frame_info, text='Địa chỉ cửa hàng', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=1, row=0, padx=10, pady=10)
        label_info = Label(self.frame_info, text='Thời gian mở cửa', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=2, row=0, padx=10, pady=10)
        label_info = Label(self.frame_info, text='Thời gian đóng cửa', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=3, row=0, padx=10, pady=10)
        label_info = Label(self.frame_info, text='Tình trạng', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=4, row=0, padx=10, pady=10)
        label_info = Label(self.frame_info, text='Chọn', font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=5, row=0, padx=10, pady=10)
            
        i = 1
        for a in self.parent.parent.cursor.execute("exec USP_XEMDANHSACHCUAHANG"):
            label_info = Label(self.frame_info, text=a[2], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=0, row=i, padx=10, pady=10)
            label_info = Label(self.frame_info, text=a[1], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=1, row=i, padx=10, pady=10)
            label_info = Label(self.frame_info, text=a[3], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=2, row=i, padx=10, pady=10)
            label_info = Label(self.frame_info, text=a[4], font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=3, row=i, padx=10, pady=10)
            #1 (Mở cửa), 0 (Tạm nghỉ), -1 (Đóng cửa)
            if a[5] == 1:
                stri = 'Mở cửa'
            elif a[5] == 0:
                stri = 'Tạm nghỉ'
            if a[5] == -1:
                stri = 'Đóng cửa'
            label_info = Label(self.frame_info, text=stri, font=('Arial', 20), bg='#ff7f50', fg='white', anchor='w').grid(column=4, row=i, padx=10, pady=10)
            button_chose = Button(self.frame_info, text="Chọn", bg='green', fg="white", width=20, command=lambda madt=a[0], diachi=a[1]:self.thucdon(madt, diachi)).grid(column=5, row=i)
            i += 1