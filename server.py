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

            login_register = conn.recv(500).decode('utf-8')
            if login_register == 'l':
                username,password = pickle.loads(conn.recv(5000))
                
                ret = database.password_check(username,password)
                if ret[0]:
                    user_id = ret[1]
                    
                    conn.send(pickle.dumps((True,database.get_channels(user_id))))
                    
                    #update later (store on user side)                 
                    client_last_read[user_id] = 0
                    client_channels[user_id] = database.get_channels(user_id)[1]


                    threading.Thread(target=handle_client,args=(conn,user_id)).start()

                    break
                else:
                    conn.send(pickle.dumps((False,)))    
                    continue

            
            elif login_register =='r':
                username,nickname,password = pickle.loads(conn.recv(500))
                
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
    print(user_id,'logged in')
    curr_channel = None
    while True:
        try:
            time.sleep(0.5)
            data = pickle.loads(conn.recv(5000))


            if data[1]:
                for i in data[1]:
                    database.create_text(i[1],user_id,i[0])
            
            if data[2]:
                for i in data[2]:
                    ret = database.get_uid(i)
                    username = database.get_username(user_id)[1]
                    if ret[0]:
                        contact_id = ret[1]
                        print(database.create_channel(i+','+username,member1=user_id,member2=contact_id))

            retData = [[],[],{}]

            if data[0] != None:
                if data[0]!=curr_channel:
                    curr_channel = data[0]
                    client_last_read[user_id]=0
                texts_send = database.get_text(data[0],client_last_read[user_id])
                retData[0] = texts_send
                if texts_send[0] and texts_send[1]:
                    
                    client_last_read[user_id] = texts_send[1][-1][0]
                
                channel_info = database.get_channel_info(data[0])
                if channel_info[0]:
                    for i in channel_info[1]:
                        if i:
                            print(database.get_nickname(i)[1],i)
                            retData[2][i] = database.get_nickname(i)[1]
            
            retData[1] = database.get_channels(user_id)

            conn.send(pickle.dumps(retData))    
                
        except Exception as e:
            print(addr,user_id,e)
            conn.close()
            break

            

while True:
    
    conn,addr = server.accept()
    thread = threading.Thread(target=client_login,args=(conn,addr))
    thread.start()
