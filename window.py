import tkinter as tk
from tkinter import ttk

def new_window():
    extra=tk.Toplevel()
    print('salut')
    
window=tk.Tk()


button=ttk.Button(master=window,text="hello",command=new_window)
button.pack()




window.mainloop()

