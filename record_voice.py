
# -*- coding: utf-8 -*-
 
'''
author:Decadence
email:leizhang9527@163.com
'''
 
import wave
import time
from datetime import datetime
from pyaudio import PyAudio, paInt16
 
chunk = 1024
framerate=8000   #采样率
NUM_SAMPLES=2000 #采样点
channels=1  #一个声道
sampwidth=2 #两个字节十六位
TIME=2      #条件变量，可以设置定义录音的时间
filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+".wav"
 
def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')  #二进制写入模式
    wf.setnchannels(channels)  
    wf.setsampwidth(sampwidth)  #两个字节16位
    wf.setframerate(framerate)  #帧速率
    wf.writeframes(b"".join(data))  #把数据加进去，就会存到硬盘上去wf.writeframes(b"".join(data)) 
    wf.close()
 
    
def my_record():
    pa = PyAudio()
    stream = pa.open(format = paInt16,channels = 1,
                     rate = framerate,input = True,
                     frames_per_buffer = NUM_SAMPLES)
    my_buf = []
    count = 0
    time.sleep(5)
    print('开始录音')
 
    while count < TIME*50:
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count += 1
        # print('...')
    save_wave_file(filename, my_buf)
    stream.close()
 
def read_file():
    wf = wave.open(filename, 'rb')
    p = PyAudio()
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),rate = wf.getframerate(),output = True,)
    print('开始放音')
    while True:
        data = wf.readframes(chunk)
        if data == b'': break
        stream.write(data)
        # print('...')
    wf.close()
    stream.close()
    p.terminate()
 
def main():
    my_record()
    print('录音完毕')
    read_file()
    print('放音完毕')
 
if __name__ == "__main__":
    main()
