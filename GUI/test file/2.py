# Import the required library
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Create an instance of tkinter frame
win=Tk()
main_frame = Frame(win)
main_frame.pack(fill=BOTH, expand=True)

frame_canvas = Canvas(main_frame)


h=Scrollbar(main_frame, orient=HORIZONTAL, command=frame_canvas.xview)
h.pack(side=BOTTOM, fill=X)
frame_canvas.pack(fill=BOTH, side=LEFT, expand=True)

frame_canvas.configure(xscrollcommand=h.set)
frame_canvas.bind(
    '<Configure>',
    lambda e:frame_canvas.configure(
        scrollregion=frame_canvas.bbox('all')
    )
)

frame_work = Frame(frame_canvas)
frame_canvas.create_window((0, 0), window=frame_work, anchor='nw')

l = ['KH001', 'KH002', 'KH003', 'KH000', 'KH0006', 'KH0007', 'KH0008', 'KH0009', 'KH0010', 'KH001', 'KH002', 'KH003', 'KH005', 'KH0022', 'KH0027', 'KH008', 'KH0039', 'KH0100']

for i in range(len(l)):
    button = Button(frame_work, text=l[i], width=30, bg='green')
    button.grid(column=i, row=0)

win.mainloop()