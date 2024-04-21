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
                        CREATE TABLE IF NOT EXISTS channel_details(channel_id int auto_increment primary key,channel_name varchar(40),member1 int,member2 int,member3 int,member4 int,member5 int
                        )
                        """)
            
            self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS messages(msg_id int auto_increment primary key,channel_id int,from_id int,sent_date datetime default(getdate
                                ),message varchar(500)
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
    
    def acc_id(self,username):
        try:
            self.cursor.execute(f'select user_id from user_details where username="{username}"')
            return (True,self.cursor.fetchall()[0][0])
        except Exception as e:
            return (False,e)
        
    def get_username(self,acc_id):
        try:
            self.cursor.execute(f'select username from user_details where user_id={acc_id}')
            return (True,self.cursor.fetchall()[0][0])
        except Exception as e:
            return (False,e)
        
    def create_channel(self,channel_name,member1=None,member2=None,member3=None,member4=None,member5=None):
        try:
            self.cursor.execute(f'insert into channel_details(member1,member2,member3,member4,member5) values ("{channel_name}",{member1},{member2},{member3},{member4},{member5})')
            self.conn.commit()
            return (True,self.cursor.lastrowid)
        except:
            self.conn.rollback()
            return (False,Exception)
        
    def create_text(self,channel_id,user_id,msg):
        try:
            self.cursor.execute(f'insert into messages(channel_id,from_id,message) values({channel_id},{user_id},"{msg}")')
            self.conn.commit()
            return (True,)
        except:
            self.conn.rollback()
            return (False,Exception)

    def retrive_text(self,channel_id,last_read):
        try:
            self.cursor.execute(f'select channel_id,from_id,sent_date,message from messages where channel_id in {channel_id} and msg_id > {last_read}')
            return (True,self.cursor.fetchall())
        except Exception as e:
            return (False,e)
    
    def get_channels(self,user_id):
        try:
            self.cursor.execute(f'select channel_id from channel_details where {user_id} in (member1,member2,member3,member4,member5)')
            ret = self.cursor.fetchall()
            retPretty = []
            for i in ret:
                retPretty.append(i[0])
            retPretty = tuple(retPretty)
            return (True,retPretty)
        except Exception as e:
            return (False,e)

