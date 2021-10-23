# -*- coding: utf-8 -*-
# create time    : 2021-01-06 15:52
# author  : CY
# file    : voice_client.py
# modify time:
import socket
import threading
import pyaudio
from PyQt5 import QtWidgets


class Client:
    def __init__(self, ip='192.168.192.68', port=9808):
        self.state = "未连接到服务器"
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while 1:
            try:
                self.target_ip = ip
                self.target_port = port
                self.s.connect((self.target_ip, self.target_port))
                break
            except:
                self.state = "连接到服务器失败"
        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 8000
        NUM_SAMPLES = 2000  # 采样点
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)
        self.state = "成功连接服务器"
        # start threads
        self.receive_thread = threading.Thread(
            target=self.receive_server_data).start()
        self.send_thread = threading.Thread(
            target=self.send_data_to_server).start()

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass

    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass

    def destroy(self):
        self.receive_thread.stop()
        self.send_thread.stop()
        del self


def connect_to_server():
    client = Client()
    return client
