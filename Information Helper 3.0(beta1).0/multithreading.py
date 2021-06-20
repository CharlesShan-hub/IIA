#from playsound import playsound

#playsound('六万.mp3')

#https://my.oschina.net/u/4017343/blog/4853842
#############################################
# for mac 需要: 
#pip3 install PyObjC --user
#pip install audioplayer
#############################################
from audioplayer import AudioPlayer

listm = ["六万.mp3","小肥川.mp3"]

import pyaudio
import wave
import sys

chunk = 1024
wf = wave.open("六万.mp3", 'rb')
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(chunk)

while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()

'''
import wx 
sound = wx.Sound("六万.mp3")
sound.Play(wx.SOUND_SYNC)
'''
