import socket
import threading
import mysql.connector
import mysql.connector.cursor
from database import db 
import pickle

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',8080))
server.listen()

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
                    break
                else:
                    conn.send(pickle.dumps(False))    
                    continue

            
            elif login_register =='r':
                username,password,nickname = pickle.loads(conn.recv(500))
                print(username,password,nickname)
                ret = database.register(username,password,nickname)
                if ret[0]:
                    user_id = ret[1]
                    break
                else:
                    conn.send(pickle.dumps(False))
                    continue


        except:
            conn.close()
            break

def client_loop(conn,user_id):
    pass

while True:
    conn,addr = server.accept()
    thread = threading.Thread(target=client_login,args=(conn,addr))
    thread.start()