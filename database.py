import mysql.connector

class db:

    def __init__(self,host,user,password,database_name):
        try:
            self.conn = mysql.connector.connect(host=host,user=user,password=password)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            self.conn.database = database_name
            self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS user_details(user_id int auto_increment primary key,username varchar(30) unique,password varchar(30),nickname varchar(25)
                        )
                        """)
            self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS channel_details(channel_id int auto_increment primary key,member1 int,member2 int,member3 int,member4 int,member5 int
                        )
                        """)
            
            self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS messages(msg_id int auto_increment primary key,channel_id int,from_id int,sent_date date,message varchar(500)
                        )
                        """)

        except Exception as e:
            print(e)

    def password_check(self,username,password):
        try:
            self.cursor.execute("SELECT password,user_id FROM user_details WHERE username = %s",(username,))
            a = self.cursor.fetchall()
            if a[0][0] == password:
                return (True,a[0][1])
            else:
                return (False,'incorrect password')
        except Exception as e:
            return (False,e)
        
    def register(self,username,password,nicknamae):
        try:
            self.cursor.execute('insert into user_details(username,password,nickname) values (%s,%s,%s)',(username,password,nicknamae))
            user_id=  self.cursor.lastrowid
            self.conn.commit()
            return (True,user_id)
        except Exception as e:
            self.conn.rollback()
            return (False,e)
    
    