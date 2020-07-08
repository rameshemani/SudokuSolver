from tkinter import *
parent = Tk()
for x_inx in range(9):
    for y_inx in range(9):
        e1 = Entry(parent).grid(row = x_inx, column = y_inx)
        e1.(highlightwidth=10)

submit = Button(parent, text = "Submit").grid(row = 10, column = 0)
parent.mainloop()
