import socket
import threading
import mysql.connector
import mysql.connector.cursor
from database import db 
import pickle

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',8080))
server.listen()

client_last_read = {}
client_channels = {}
database = db('localhost','root','password','test1')

def client_login(conn:socket.socket,addr):
    print(addr,'connected')
    while True:
        try:

            login_register = conn.recv(50).decode('utf-8')
            if login_register == 'l':
                username,password = pickle.loads(conn.recv(500))
                print(username,password)
                ret = database.password_check(username,password)
                if ret[0]:
                    user_id = ret[1]
                    conn.send(pickle.dumps(True))
                    
                    #update later (store on user side)                 
                    client_last_read[user_id] = 0
                    client_channels[user_id] = database.get_channels(user_id)[1]


                    threading.Thread(target=handle_client,args=(conn,user_id)).start()

                    break
                else:
                    conn.send(pickle.dumps(False))    
                    continue

            
            elif login_register =='r':
                username,password,nickname = pickle.loads(conn.recv(500))
                print(username,password,nickname)
                ret = database.register(username,password,nickname)
                if ret[0]:
                    conn.send(pickle.dumps(True))
                    user_id = ret[1]
                    continue
                else:
                    conn.send(pickle.dumps(False))
                    continue


        except:
            conn.close()
            break


def handle_client(conn:socket.socket,user_id):
    while True:
        try:
            curr_channel = pickle.load(conn.recv(300))
            
            for i in texts:
                database.create_text()

        except:
            pass


while True:
    conn,addr = server.accept()
    thread = threading.Thread(target=client_login,args=(conn,addr))
    thread.start()
