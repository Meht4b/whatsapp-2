import tkinter as tk
import ttkbootstrap as ttk


class user:
    def __init__(self):
        self.window = ttk.Window()
        self.login_GUI()
        self.window.mainloop()

    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def login_

    def login_GUI(self):

        self.clear()

        self.login_frame = ttk.Frame(self.window)

        sign = ttk.Label(self.login_frame,text='login',font='Calibri 24 bold')
        sign.pack()

        username_frame = ttk.Frame(self.login_frame)
        username_prompt = ttk.Label(username_frame,text='username:',font='Calibri 14')
        username_entry = ttk.Entry(username_frame)

        username_entry.grid(column=1,row=0)
        username_prompt.grid(column=0,row=0)
        username_frame.pack()

        password_frame = ttk.Frame(self.login_frame)
        password_prompt = ttk.Label(password_frame,text='password:',font='Calibri 14')
        password_entry = ttk.Entry(password_frame)

        password_entry.grid(column=1,row=0)
        password_prompt.grid(column=0,row=0)
        password_frame.pack()

        login_confirm = ttk.Button(self.login_frame,text='login',command=self.login_check)
        login_confirm.pack()



        self.login_frame.pack()

        
a =userGui()