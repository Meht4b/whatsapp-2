import socket
import threading
import mysql.connector
import mysql.connector.cursor
from database import db 
import pickle
import time

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


        except Exception as e:
            print(e)
            conn.close()
            return None


def handle_client(conn:socket.socket,user_id):
    while True:
        try:
            time.sleep(1/2)
            data = pickle.loads(conn.recv(5000))
            print(data)

            if data[1]:
                for i in data[1]:
                    print(i)
                    database.create_text(i[0],user_id,i[1])
                
            if data[0] != None:
                texts_send = database.get_text(data[0],client_last_read[user_id])
                print(texts_send)
                conn.send(pickle.dumps(texts_send))
                
                
        except Exception as e:
            print(addr,user_id,e)
            conn.close()
            return None

while True:
    conn,addr = server.accept()
    thread = threading.Thread(target=client_login,args=(conn,addr))
    thread.start()
