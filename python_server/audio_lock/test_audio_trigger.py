'''
Repeatedly run a command if the system records a sound loud enough.
Requires PyAudio and Numpy.

Windows users:
win32 Python 2.7: http://www.python.org/ftp/python/2.7.3/python-2.7.3.msi
Numpy: http://sourceforge.net/projects/numpy/files/NumPy/1.7.1/numpy-1.7.1-win32-superpack-python2.7.exe/download
PyAudio: http://people.csail.mit.edu/hubert/pyaudio/packages/pyaudio-0.2.7.py27.exe
'''
import os
import time

import pyaudio
import numpy

import matplotlib.pyplot as plt
from scipy.fft import fft


system_command = 'ls' # passed to os.system() on audio trigger
threshold = 0.05 # volume threshold to trigger at, 0 is nothing 1 is max volume
min_delay = 1 # min seconds between attempts
last_run = 0 # helper for min_delay behavior

audio_sample_rate = 48e3
audio_frame_samples = 1024*7

audio_sample_rate = 48e3/4
audio_frame_samples = 1024*7


left_channel = 0
right_channel = 1

def audio_data():
  try:
    _ = audio_data.stream
  except AttributeError:
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=2,
                     rate=int(audio_sample_rate),
                     input=True,
                     frames_per_buffer=audio_frame_samples)
    audio_data.stream = stream

  # When reading from our 16-bit stereo stream, we receive 4 characters (0-255) per
  # sample. To get them in a more convenient form, numpy provides
  # fromstring() which will for each 16 bits convert it into a nicer form and
  # turn the string into an array.
  raw_data = audio_data.stream.read(audio_frame_samples) # always read a whole buffer.
  samples  = numpy.fromstring(raw_data, dtype=numpy.int16)
  # Normalize by int16 max (32767) for convenience, also converts everything to floats
  normed_samples = samples / float(numpy.iinfo(numpy.int16).max)
  # split out the left and right channels to return separately.
  # audio data is stored [left-val1, right-val1, left-val2, right-val2, ...]
  # so just need to partition it out.
  left_samples = normed_samples[left_channel::2]
  right_samples = normed_samples[right_channel::2]
  return left_samples, right_samples

audio_data() # toss out first read
while True:
  left, right = audio_data()

  if max(right) > threshold and time.time() - last_run > min_delay:
    os.system(system_command)
    print('Detected sound')
    last_run = time.time()

    f = abs(fft(left))
    
    plt.subplot(2,1,1)
    plt.plot(left)
    plt.subplot(2,1,2)
    plt.plot(f)
    plt.show()


