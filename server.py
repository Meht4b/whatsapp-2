import socket
import threading
import mysql.connector
import mysql.connector.cursor

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',8080))
server.listen()



def handle_client(conn:socket.socket,addr):
    while True:
        try:

            login_register = conn.recv(50).decode('utf-8')
            if login_register == 'l':


        except:
            conn.close()
            break

while True:
    conn,addr = server.accept()
    thread = threading.Thread(target=handle_client,args=(conn,addr))
    thread.start()