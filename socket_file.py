#-*-coding:utf-8 -*-
from socket import *
import threading
from time import  ctime
import os
import sys

class Server_file(object):                                              #the file's transport of Server
    """docstring for Server_file"""
    def __init__(self,HOST,PORT,socket_num):
        super(Server_file, self).__init__()

        self.BASE_DIR=os.path.dirname(os.path.abspath(__file__))
        self.path=None
        self.HOST=HOST                                          #Server's address of IP
        self.PORT=PORT                                                  #Server's port
        self.BUFSIZ=1024
        self.ADDR = (self.HOST,self.PORT)
        self.socket_num=socket_num
        self.socks=[]
        self.t = threading.Thread(target=self.upload_file_process)

    def connect_init(self):
        self.tcpCliSock = socket()                  #build the new socket object
        self.tcpCliSock.bind(self.ADDR)                                 #bind the IP
        self.tcpCliSock.listen(self.socket_num)
        print('Server started！\n')                                    
    def connect_client(self):
        print('Server waiting......')                                          #The connection is blocked by self.tcpCliSock.accept()
        self.conn,self.addr=self.tcpCliSock.accept()
        print("{0},{1} are connected！".format(self.addr[0],self.addr[1]))
    def upload_file_header(self):                                       #Collaborate with the client to create a file directory(/data/)
        try:
            self.tcpCliSock = socket()                  #build the new socket object
            self.tcpCliSock.bind(self.ADDR)                                 #bind the IP
            self.tcpCliSock.listen(self.socket_num)
            self.t.start()
            while True:
                self.conn,self.addr=self.tcpCliSock.accept()
                print("{0},{1} are connected！".format(self.addr[0],self.addr[1]))
                self.conn.setblocking(0)
                self.socks.append(self.conn)
                print(self.socks)
        except Exception as e:
            pass
    def upload_file_process(self):
        while True:
            try:
                data = self.socks[1].recv(self.BUFSIZ)
            except Exception as e:
                continue
            s=self.socks[0]
            s.send(b'%s' %(data))

class Client_file(object):                                                    #the file's transport of Client
    """docstring for client_file"""
    def __init__(self,HOST,PORT):
        super(Client_file, self).__init__()

        self.BASE_DIR=os.path.dirname(os.path.abspath(__file__))
        self.path=None

        self.file_size=0
        self.HOST=HOST                                                #Server's address of IP
        self.PORT=PORT                                                        #Server's port
        self.BUFSIZ=1024
        self.ADDR = (self.HOST,self.PORT)

        self.tcpCliSock=None



    def input_commend(self):
        inp = input('>').strip()
        cmd,content = inp.split('|')
        return cmd,content


    def connect_server(self):
        self.tcpCliSock = socket(AF_INET,SOCK_STREAM)                         #create the new Client's socket object
        self.tcpCliSock.connect(self.ADDR)                                    #connect the IP address

    def upload_file_header_send(self):
        self.tcpCliSock = socket(AF_INET,SOCK_STREAM)                         #create the new Client's socket object
        self.tcpCliSock.connect(self.ADDR)                                    #connect the IP address
        while True:
            cmd,content=self.input_commend()
            self.path = os.path.join(self.BASE_DIR,content)
            self.file_name=os.path.basename(self.path)
            self.file_size=os.stat(self.path).st_size
            file_info = '%s|%s|%s' %(cmd,self.file_name,self.file_size)
            self.tcpCliSock.sendall(bytes(file_info,'utf-8'))
            self.has_sent=0
            with open(self.path,'rb') as fp:
                # self.tcpCliSock.recv(self.BUFSIZ)
                while self.has_sent != self.file_size:
                    data = fp.read(self.BUFSIZ)
                    self.tcpCliSock.sendall(data)
                    self.has_sent+=len(data)
                    print('\r'+'[Upload progress]：%s%.02f%%' %('>'*int((self.has_sent/self.file_size)*50),float(self.has_sent/self.file_size)*100),end='')
                print()
                print('%s Upload success！'%(self.file_name))
    def upload_file_header_rev(self):                                         #rev faction
        self.tcpCliSock = socket(AF_INET,SOCK_STREAM)                         #create the new Client's socket object
        self.tcpCliSock.connect(self.ADDR)                                    #connect the IP address
        while True:
            data = self.tcpCliSock.recv(self.BUFSIZ)
            cmd,self.file_name,file_size = str(data,'utf-8').split('|')
            self.path=os.path.join(self.BASE_DIR,'rev')
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            self.path=os.path.join(self.path,self.file_name)
            self.file_size=int(file_size)
            self.has_sent=0
            with open(self.path,'wb') as fp:
                # self.tcpCliSock.recv(self.BUFSIZ)
                while self.has_sent != self.file_size:
                    rec_data=self.tcpCliSock.recv(self.BUFSIZ)
                    # rec_data = rec_data.decode('utf-8')
                    fp.write(rec_data)
                    self.has_sent+=len(rec_data)
                    print('\r'+'[Download progress]：%s%.02f%%' %('>'*int((self.has_sent/self.file_size)*50),float(self.has_sent/self.file_size)*100),end='')
                print()
                print('%s download success！'%(self.file_name))

