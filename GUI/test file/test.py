import tkinter as tk

def delFrame():
    main_frame.destroy()

win = tk.Tk()
main_frame = tk.Frame(win)
canvas_frame = tk.Canvas(main_frame, width=600)
v = tk.Scrollbar(main_frame, orient='vertical', command=canvas_frame.yview)
scroll_frame = tk.Frame(canvas_frame)
list = ['KH001', 'KH002', 'KH003', 'KH000', 'KH0006', 'KH0007', 'KH0008', 'KH0009', 'KH0010', 'KH001', 'KH002', 'KH003', 'KH005', 'KH0022', 'KH0027', 'KH008', 'KH0039', 'KH0100']

scroll_frame.bind(
    "<Configure>",
    lambda e: canvas_frame.configure(
        scrollregion=canvas_frame.bbox("all")
    )
)
canvas_frame.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas_frame.configure(yscrollcommand=v.set)


for i in range(len(list)):
    button_1 = tk.Button(master=scroll_frame, bg='green', fg='white', text=list[i], width=20, command=delFrame).grid(column=0, row=i)


main_frame.pack()
canvas_frame.pack(side="left", fill="both", expand=True)
v.pack(side='right', fill='y')

win.mainloop()