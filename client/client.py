import tkinter as tk
import ttkbootstrap as ttk
#from tkinter import ttk
import socket
import pickle
import threading




class user:
    def __init__(self,host,port):
        self.window = ttk.Window(themename='journal')
        self.window.geometry('400x200')
        self.window.title('Whatsapp 2 ')

        self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.conn.connect((host,port))
        self.send_queue = []
        self.texts = []

        #fix later
        self.current_channel = None

        self.login_GUI()
        self.window.mainloop()

    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    #checks password and username 
    def login_server(self,username,password):
        
        self.conn.send('l'.encode('utf-8'))
        self.conn.send(pickle.dumps((username,password)))
        response = pickle.loads(self.conn.recv(50))
        if response == True:
            self.client_loop_GUI()
            threading.Thread(target=self.input_feed).start()
            threading.Thread(target=self.output_feed).start()

        else:
            self.login_GUI(retry=True)

    #GUI for login
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

    #registers new user
    def register_server(self,username,nickname,password):
        
        print(username,password,nickname)
        self.conn.send('r'.encode('utf-8'))
        self.conn.send(pickle.dumps((username,password,nickname)))
        flag = pickle.loads(self.conn.recv(500))

        if flag:
            self.login_GUI(newUser=True)

    #GUI for new user
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
        username_frame.pack(pady=4)

        password_frame = ttk.Frame(self.register_frame)
        password_prompt = ttk.Label(password_frame,text='password:',font='Calibri 14')
        password_entry = ttk.Entry(password_frame)

        password_entry.grid(column=1,row=0)
        password_prompt.grid(column=0,row=0)
        password_frame.pack(pady=4)

        nickname_frame = ttk.Frame(self.register_frame)
        nickname_prompt = ttk.Label(nickname_frame,text='nickname:',font='Calibri 14')
        nickname_entry = ttk.Entry(nickname_frame)

        nickname_entry.grid(column=1,row=0)
        nickname_prompt.grid(column=0,row=0)
        nickname_frame.pack(pady=4)

        register_button = ttk.Button(self.register_frame,text='register',command=lambda:self.register_server(username_entry.get(),password_entry.get(),nickname_entry.get()))
        register_button.pack()

        self.register_frame.pack()

    #creates new channel with user and other contact
    def add_contact_server(self,username):
        self.conn.send(pickle.dumps(1,username))

    #to add new contact
    def add_contact_GUI(self,retry=False):
        pass

    #returns all the channels the user is in as list(server)
    def get_channels(self): 
        pass

    #scrollable widget with buttons which requests server chat history
    def channels_GUI(self):
        pass

    def client_loop_GUI(self):
        self.clear()
        self.chat_entry = ttk.Entry(self.window)
        but = ttk.Button(self.window,text='h',command=self.output_feed)
        self.chat_entry.pack()
        but.pack()

    def output_feed(self):
        self.send_queue.append(self.chat_entry.get())
        self.send_queue.clear()

    def data_loop(self):
        self.conn.send(pickle.dumps(self.current_channel))

        self.conn.send(pickle.dumps(self.send_queue))
        self.send_queue = []
  
        if self.current_channel != None:
            self.texts.extend(0,pickle.loads(self.conn.recv(500)))

a =user('localhost',8080)
