import tkinter as tk
import ttkbootstrap as ttk
#from tkinter import ttk
import socket
import pickle
import threading
import time




class user:
    def __init__(self,host,port):
        self.window = ttk.Window(themename='journal')
        self.window.geometry('400x200')
        self.window.title('Whatsapp 2 ')

        self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.conn.connect((host,port))
        self.send_queue = []
        self.new_channels_queue = []
        self.texts = []
        self.channels = []
        self.members = {}

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
        response = pickle.loads(self.conn.recv(500))
        if response[0] == True:
            self.client_loop_GUI()
            self.network_thread = threading.Thread(target=self.data_loop)
            self.network_thread.start()

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
        self.new_channels_queue.append(username)
        self.client_loop_GUI()

    #to add new contact
    def add_contact_GUI(self,retry=False):
        self.clear()
        username_entry = ttk.Entry(self.window)
        username_entry.insert(0,'enter username')
        username_entry.pack()

        ttk.Button(self.window,text='add contact',command=lambda:self.add_contact_server(username_entry.get())).pack()
        

    def update_current_channel(self,e):
        self.current_channel = int(self.channels_dropdown.get().split()[0])
        self.current_channel_name.config(text=self.channels_dropdown.get().split()[1])

    def update_sendqueue(self):
        self.send_queue.append((self.message_text.get(),self.current_channel))
        self.message_text.delete(0,ttk.END)


    def client_loop_GUI(self):

        self.clear()

        self.window.geometry('690x430')

        self.channels_dropdown = ttk.Combobox(self.window,values=self.channels)
        self.channels_dropdown.bind('<<ComboboxSelected>>',self.update_current_channel)
        self.channels_dropdown.grid(row=0,column=0)
        self.channels_dropdown.config(state="readonly",)

        ttk.Button(self.window,text='add contact',command=self.add_contact_GUI).grid(column=0,row=2,sticky='sew')

        self.text_area = ttk.ScrolledText(self.window)
        self.text_area.grid(column=1,row=1,columnspan=3,sticky='ew') 

        self.message_text = ttk.Entry(self.window)
        self.message_text.grid(column=1,row=2,sticky='we',columnspan=2)

        ttk.Button(self.window,text='send',command=self.server_send).grid(column=3,row=2,sticky='we')


        self.current_channel_name = ttk.Label(self.window)
        self.current_channel_name.grid(row=0,column=1)

        

        top_right_frame = ttk.Frame(self.window)
        top_right_frame.grid(column=2,row=0,sticky='e',columnspan=2)


        add_member  = ttk.Button(top_right_frame,text='add member to channel')
        add_member.pack(side='left',padx=4)
        change_name  = ttk.Button(top_right_frame,text='change channel name')
        change_name.pack(side='left')

        self.window.protocol('WM_DELETE_WINDOW',self.stop)


    def stop(self):
        self.conn.close()
        self.window.destroy()

    def server_send(self):
        
        self.conn.send(pickle.dumps((self.message_text.get(),self.current_channel)))
        self.message_text.delete(0,ttk.END)
        

    def server_recv(self):
        data = self.conn.recv()


a =user('localhost',8080)
