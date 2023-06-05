from tkinter import *

list_label_text = ['Mã đơn hàng', 'Tên khách hàng', 'Tên tài xế', 'Địa chỉ chi nhánh', 'Tên đối tác', 'Ngày lập', 'Địa chỉ giao hàng',
                            'Trạng thái', 'Phí sản phẩm', 'Phí vận chuyển', 'Tổng tiền', 'Thanh toán', 'Thời gian giao', 'Chi tiết đơn hàng']

scroll_frame = Tk()

for pos in range(len(list_label_text)):
            Label(scroll_frame, text=list_label_text[pos], bg='brown', fg='white', font=('Times New Roman', 20)).grid(column=pos, row=0) 

scroll_frame.mainloop()