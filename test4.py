from tkinter import *

def EntryBox(root_frame, w, h):
    boxframe = Frame(root_frame, width = w+2, height= h+2, highlightbackground="black",
                     highlightcolor="black", highlightthickness=1, bd=0)
    l = Entry(boxframe, borderwidth=0, relief="flat", highlightcolor="white")
    l.place(width=w, height=h)
    l.pack()
    boxframe.pack()
    return boxframe

root = Tk()
frame = Frame(root, width = 1000, height = 500, bd=2)
subframe = Frame(frame, width = 500, height=400, bd=3)
frame.pack()
subframe.pack()

labels = []

for i in range(5):
    for j in range(5):
        box = EntryBox(frame, 40, 30)
        box.place(x = 50 + i*100, y = 30 + j*30 , width = 100, height = 30)
        labels.append(box)

root.mainloop()