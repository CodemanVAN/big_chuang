
# -*- coding: utf-8 -*-
# create time    : 2020-12-30 15:37
# author  : CY
# file    : voice_server.py
# modify time:
import socket
import threading
import wave
import time
from datetime import datetime
from pyaudio import PyAudio, paInt16
 
chunk = 1024
framerate=8000   #采样率
NUM_SAMPLES=1024 #采样点
channels=1  #一个声道
sampwidth=2 #两个字节十六位

 
def save_wave_file(filename, data):
    filename = filename+' '+datetime.now().strftime("%Y-%m-%d-%H-%M")+".wav"
    wf = wave.open(filename, 'wb')  #二进制写入模式
    wf.setnchannels(channels)  
    wf.setsampwidth(sampwidth)  #两个字节16位
    wf.setframerate(framerate)  #帧速率
    wf.writeframes(b"".join(data))  #把数据加进去，就会存到硬盘上去wf.writeframes(b"".join(data)) 
    wf.close()

class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.record_data={}
        while True:
            try:
                self.port = 9808
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((self.ip, self.port))
                break
            except:
                print("Couldn't bind to that port")
 
        self.connections = []
        
        self.accept_connections()
 
    def accept_connections(self):
        self.s.listen(100)
 
        print('Running on IP: ' + self.ip)
        print('Running on port: ' + str(self.port))
 
        while True:
            c, addr = self.s.accept()
 
            self.connections.append(c)
            self.record_data[addr[0]]=[]
            threading.Thread(target=self.handle_client, args=(c, addr,)).start()
            threading.Thread(target=self.clear_dead_connection, args=()).start()
    def clear_dead_connection(self):
        while 1:
            tp=self.connections
            self.connections=[]
            exist_ip=[]
            for i in tp:
                if not i._closed:
                    self.connections.append(i)
                    exist_ip.append(i.getsockname()[0])
            for i in list(self.record_data.keys()):
                if i not in exist_ip:
                    save_wave_file(i,self.record_data[i])
                    del self.record_data[i]
    def broadcast(self, sock, data):

        for client in self.connections:
            if client != self.s and client != sock and not client._closed:
                try:
                    client.send(data)
                except:
                    pass
 
    def handle_client(self, c, addr):
        while 1:
            try:        
                data = c.recv(1024)
                if addr[0] in self.record_data:
                    self.record_data[addr[0]].append(data)
                #for i in self.record_data.keys():
                #save_wave_file(addr[0],data)
                self.broadcast(c, data)
            except socket.error:
                c.close()
                break
 
 
server = Server()