# -*- coding=utf8 -*-
import wave
import pylab as pl
import numpy as np
import os

# 打开WAV文档
wavdir = "C:\\Users\\vili\\Downloads\\animals"
flist =os.listdir(wavdir)
f = wave.open(os.path.join(wavdir,flist[0]), "rb")

# 读取格式信息
# (nchannels, sampwidth, framerate, nframes, comptype, compname)
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]

# 读取波形数据
str_data = f.readframes(nframes)
f.close()

#将波形数据转换为数组
wave_data = np.fromstring(str_data, dtype=np.short)
wave_data.shape = -1, 2
wave_data = wave_data.T
time = np.arange(0, nframes) * (1.0 / framerate)


N=44100
start=0 #开始采样位置
df = framerate/(N-1) # 分辨率
freq = [df*n for n in range(0,N)] #N个元素
wave_data2=wave_data[0][start:start+N]
c=numpy.fft.fft(wave_data2)*2/N
#常规显示采样频率一半的频谱
d=int(len(c)/2)
#仅显示频率在4000以下的频谱
while freq[d]>4000:
    d-=10
    pl.plot(freq[:d-1],abs(c[:d-1]),'r')
    pl.show()
