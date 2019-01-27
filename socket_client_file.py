#-*-coding:utf-8 -*-
from socket import *
from threading import Thread
from time import  ctime
import os
import sys
class Client_file(object):                                                    #the file's transport of Client
    """docstring for client_file"""
    def __init__(self):
        super(Client_file, self).__init__()

        self.BASE_DIR=os.path.dirname(os.path.abspath(__file__))
        self.path=None

        self.has_sent=0
        self.file_size=0
        self.HOST='127.0.0.1'                                                 #Server's address of IP
        self.PORT=2159                                                        #Server's port
        self.BUFSIZ=1024
        self.ADDR = (self.HOST,self.PORT)

        self.tcpCliSock=None



    def connect_server(self):
        self.tcpCliSock = socket(AF_INET,SOCK_STREAM)                         #create the new Client's socket object
        self.tcpCliSock.connect(self.ADDR)                                    #connect the IP address

    def upload_file_header(self,cmd,content):                                 #
        self.path = os.path.join(self.BASE_DIR,content)
        self.file_name=os.path.basename(self.path)
        self.file_size=os.stat(self.path).st_size
        file_info = '%s|%s|%s' %(cmd,self.file_name,self.file_size)
        self.tcpCliSock.sendall(bytes(file_info,'utf-8'))
    def upload_file_process(self):
        if self.path != None:
            with open(self.path,'rb') as fp:
                self.tcpCliSock.recv(self.BUFSIZ)
                while self.has_sent != self.file_size:
                    data = fp.read(self.BUFSIZ)
                    self.tcpCliSock.send(data)
                    self.has_sent+=len(data)
                    print('\r'+'[保存进度]：%s%.02f%%' %('>'*int((self.has_sent/self.file_size)*50),float(self.has_sent/self.file_size)*100),end='')
                print('%s 保存成功！'%(self.file_name))

        else:
            print('please use load_file_header to load file path')
            pass

