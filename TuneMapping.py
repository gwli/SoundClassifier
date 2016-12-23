import wave
import numpy as np
import pylab as pl
import sys
import os
import math
import logging
import time

logging.basicConfig(level=logging.INFO)
  
def moments(x):
    mean = x.mean()
    std = x.var()**0.5
    skewness = ((x - mean)**3).mean() / std**3
    kurtosis = ((x - mean)**4).mean() / std**4
    return [mean, std, skewness, kurtosis]
  
def fftfeatures(wavdata):
    f = np.fft.fft(wavdata)
    f = f[2:(f.size / 2 + 1)]
    f = abs(f)
    total_power = f.sum()
    f = np.array_split(f, 10)
    return [e.sum() / total_power for e in f]
  
def features(x):
    f = []
    length = int (math.log(x.size,2))
    reduce_x = x[0:2**length]
    xs = x
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))
     
    xs = reduce_x.reshape(-1, 64).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))
     
    xs = reduce_x.reshape(-1, 512).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))
     
    xs = reduce_x.reshape(-1, 1024).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))
     
    f.extend(fftfeatures(x))
    return f
  
   # f will be a list of 42 floating point features with the following
   # names:
     
   # amp1mean
   # amp1std
   # amp1skew
   # amp1kurt
   # amp1dmean
   # amp1dstd
   # amp1dskew
   # amp1dkurt
   # amp10mean
   # amp10std
   # amp10skew
   # amp10kurt
   # amp10dmean
   # amp10dstd
   # amp10dskew
   # amp10dkurt
   # amp100mean
   # amp100std
   # amp100skew
   # amp100kurt
   # amp100dmean
   # amp100dstd
   # amp100dskew
   # amp100dkurt
   # amp1000mean
   # amp1000std
   # amp1000skew
   # amp1000kurt
   # amp1000dmean
   # amp1000dstd
   # amp1000dskew
   # amp1000dkurt
   # power1
   # power2
   # power3
   # power4
   # power5
   # power6
   # power7
   # power8
   # power9
   # power10
   
def read_wav(wav_file):
    """Returns two chunks of sound data from wave file."""
    w = wave.open(wav_file)
    n = w.getnframes()
    frames = w.readframes(n)
    wave_data = np.fromstring(frames, dtype=np.short)
    wave_data.shape = -1, 2   
    wave_data = wave_data[:,1] 
    return wave_data

def compute_chunk_features(mp3_file):
    wav_data = read_wav(mp3_file)
    # We'll cover how the features are computed in the next section!
    return features(wav_data)
  
# Main script starts here
# =======================

def test1():
    for path, dirs, files in os.walk('C:/Users/vili/Downloads/animals'):
        for f in files:
            if not f.endswith('.wav'):
               # Skip any non-MP3 files
               continue
            mp3_file = os.path.join(path, f)
            # Extract the track name (i.e. the file name) plus the names
            # of the two preceding directories. This will be useful
            # later for plotting.
            tail, track = os.path.split(mp3_file)
            tail, dir1 = os.path.split(tail)
            tail, dir2 = os.path.split(tail)
            # Compute features. feature_vec1 and feature_vec2 are lists of floating
            # point numbers representing the statistical features we have extracted
            # from the raw sound data
            feature_vec1, feature_vec2 = compute_chunk_features(mp3_file)
            try:
             feature_vec1, feature_vec2 = compute_chunk_features(mp3_file)
            except:
             continue
def test2():
    wavdir = "C:\\Users\\vili\\Downloads\\animals"
    flist =os.listdir(wavdir)
    map(lambda x:plot_power(os.path.join(wavdir,x)),flist)


def plot_power(mp3_file):
    file_name,ext = os.path.splitext(os.path.basename(mp3_file))
    feature_vec = compute_chunk_features(mp3_file)
    pl.clf()
    pl.plot(range(10),feature_vec[-10:],'r')
    pl.xlabel("power distrubute of {}".format(file_name))
    #pl.show()
    pl.savefig(file_name)
    pl.close()


    logging.info( "{} {} finish".format(time.asctime(time.localtime(time.time())),mp3_file))

def main():
    test2()

if __name__ == "__main__":
    main()
