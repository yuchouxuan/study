import numpy
from scipy import signal
import libnum
import matplotlib.pyplot as plt

f = FileF.f2s(down + 'fsknoise_1.txt').split()
numx = [float(i) for i in f]
# 滤波器
b, a = signal.butter(4, 0.2, 'lowpass')  # 'lowpass','bandpass' 'highpass'
f = signal.filtfilt(b, a, numx)
w = 80  # 窗口宽度

s = ''
for i in range(0, len(f), w):
    a = numpy.abs(numpy.fft.fft(f[i:i + w]))
    if a[1] > a[4]:
        s += '0'
    else:
        s += '1'
i = int(s, 2)
print(s)
print(libnum.n2s(i))
