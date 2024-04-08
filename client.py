import tkinter as tk
import ttkbootstrap as ttk
import socket

class user:
    def __init__(self,host,port):
        self.window = ttk.Window(themename='journal')
        self.window.geometry('400x200')
        self.window.title('Whatsapp 2 ')
        self.login_GUI()
        self.window.mainloop()

    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def login_server(self,username,password):
        self.login_GUI(retry=True)

    def login_GUI(self,retry=False,newUser=False):

        self.clear()

        login_frame = ttk.Frame(self.window)

        if newUser:
            ttk.Label(login_frame,text='succesfuly registered',font='Calibri 12',foreground='green').pack(pady=3)
        

        sign = ttk.Label(login_frame,text='login',font='Calibri 24 bold')
        sign.pack(pady=10)

        username_frame = ttk.Frame(login_frame)
        username_prompt = ttk.Label(username_frame,text='username:',font='Calibri 14')
        username_entry = ttk.Entry(username_frame)

        username_entry.grid(column=1,row=0)
        username_prompt.grid(column=0,row=0)
        username_frame.pack()

        password_frame = ttk.Frame(login_frame)
        password_prompt = ttk.Label(password_frame,text='password:',font='Calibri 14')
        password_entry = ttk.Entry(password_frame)

        password_entry.grid(column=1,row=0)
        password_prompt.grid(column=0,row=0)
        password_frame.pack()

        login_register_frame = ttk.Frame(login_frame)
        login_button = ttk.Button(login_register_frame,text='login',command=lambda:self.login_server(username_entry.get(),password_entry.get()))
        register_button = ttk.Button(login_register_frame,text='register',command=self.register_GUI)
        login_button.pack(side='left',padx=10)
        register_button.pack(side='left')
        login_register_frame.pack(pady=10)

        if retry==True:
            ttk.Label(login_frame,text='wrong username/password',foreground='red').pack()

        login_frame.pack()

    def register_server(self,username,nickname,password):
        
        self.login_GUI(newUser=True)

    def register_GUI(self):
        self.clear()
        
        self.register_frame = ttk.Frame(self.window)

        sign = ttk.Label(self.register_frame,text='Register',font='Calibri 24 bold')
        sign.pack()

        username_frame = ttk.Frame(self.register_frame)
        username_prompt = ttk.Label(username_frame,text='username:',font='Calibri 14')
        username_entry = ttk.Entry(username_frame)

        username_entry.grid(column=1,row=0)
        username_prompt.grid(column=0,row=0)
        username_frame.pack()

        password_frame = ttk.Frame(self.register_frame)
        password_prompt = ttk.Label(password_frame,text='password:',font='Calibri 14')
        password_entry = ttk.Entry(password_frame)

        password_entry.grid(column=1,row=0)
        password_prompt.grid(column=0,row=0)
        password_frame.pack()

        nickname_frame = ttk.Frame(self.register_frame)
        nickname_prompt = ttk.Label(nickname_frame,text='nickname:',font='Calibri 14')
        nickname_entry = ttk.Entry(nickname_frame)

        nickname_entry.grid(column=1,row=0)
        nickname_prompt.grid(column=0,row=0)
        nickname_frame.pack()

        register_button = ttk.Button(self.register_frame,text='register',command=lambda:self.register_server(username_entry.get(),password_entry.get(),nickname_entry.get()))
        register_button.pack()

        self.register_frame.pack()


a =user('localhost',8080)