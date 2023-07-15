from tkinter import *

print(2 ** 5) 
def get_text():
    s = text.get(1.0, END)
    print(s, end="")
 
root = Tk()
 
text = Text(width=25, height=5)
text.pack()
 
frame = Frame()
frame.pack()
Button(frame, text="Вставить",
       command=get_text).pack(side=LEFT)
 
label = Label()
label.pack()
 
root.mainloop()
 
