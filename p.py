import pyaudio

player=pyaudio.PyAudio()
chunk_size = 1024  # 512
audio_format = pyaudio.paInt16
channels = 1
rate = 20000

playing_stream = player.open(format=audio_format, channels=channels, rate=rate, output=True,
                                    frames_per_buffer=chunk_size)
record_stream = player.open(format=audio_format, channels=channels, rate=rate, input=True,
                                    frames_per_buffer=chunk_size)
recd=b''
for i in range(1000):
    recd+=record_stream.read(1024)
playing_stream.write(recd) 
'''
data=b''
with open('1.mp3','rb') as f:
    for i in f.readlines():
        playing_stream.write(i)
        '''