from math import *
import matplotlib.pyplot as plt
import random

window = 31 * 20
dx = 2 * pi / 31


def cNumbers(x):
    start = 0;
    ret = []
    x = int(x)
    for i in range(window):
        ret.append(sin(start + dx * i + x * pi))
    return ret


nol = []
for i in arr:
    wav = random.randint(-100, 100) / 20 * noiz
    nol.append(i + wav)
plt.plot(nol);
plt.show()

for i in range(12):
    a = numpy.abs(numpy.fft.fft(nol[i * window:i * window + window]) / 100)
    b = numpy.angle(numpy.fft.fft(nol[i * window:i * window + window]) / 100)
    print(b[20], end=' ')
'''
    plt.subplot(331+i)
    plt.plot(a[:window//2], color='black')

    plt.title('0-100')
'''

plt.show()

'''
from math import *
window=31*20
dx= 2*pi/31
#生成载波----------------------------------------------------
def cNumbers(x ):
    start = 0;
    ret=[]
    x = int(x)
    for i in range(window):
            ret.append(sin(start+dx*i + x*pi))
    return ret

#生成原始波形----------------------------------------------------
flago='flag{4fee119fbdf9ae1ae470e4f638507cb1}'
flag= bin(libnum.s2n(flago))[2:]
flag = ('0')*(8-len(flag)%8)+flag
arr=[]
for i in flag:
    arr.extend(cNumbers(i))
#加干扰----------------------------------------------------
import random
nol = []
noiz=max(arr)
for i in arr:
    wav = random.randint(-100,100)/20*noiz
    nol.append(i+wav)
#存文件----------------------------------------------------
with open(down+'FSK.txt','w') as f:
    for i in nol :
        f.write('%f '%i)'''
'''
#解密
window=31*20
nol = open('PSK.txt','r').read().split()
nol =[float(i) for i in nol]
bincode=''
for i in range(len(nol)//window):
    b= numpy.angle(numpy.fft.fft(nol[i * window:i * window + window]) / 100)
    if(b[20] >0) :bincode+='1'
    else: bincode+='0'
dfla=libnum.n2s(int(bincode,2))
CharF.compStr(flago,dfla)
'''
