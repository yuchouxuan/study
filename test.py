from gmpy2 import  *
import gmpy2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import *

wavelen=4111
BinF=512
ByteinFrame=BinF//8
dx=const_pi()/wavelen
def makeWave(x=1):
    d=dx*8*x
    alpha=0
    arr=[]
    for i in range(wavelen):
        arr.append(float(sin(alpha)))
        alpha+=d
    return np.array(arr)

flagb= open('c:/ctf/flag.png','rb').read()
bm=0x80
tbar = tqdm(total=64)
wavedat=np.array([])
for Frame in trange(0,len(flagb),ByteinFrame):
    ax = np.array([0. for i in range(wavelen)])
    for bcont in range(ByteinFrame):
        try:
            x= flagb[Frame+bcont]
        except:
            x=0x0
        for i in range(8):
                if(x&(bm>>i))!=0:
                    ax = ax + makeWave(bcont*8+i)
        tbar.update(1)
    wavedat = np.append(wavedat,ax)
    tbar.update(-64)
    break

len(wavedat),max(wavedat),min(wavedat)
WD=wavedat*200
len(WD),max(WD),min(WD)
import utfc.SoundF
WD=wavedat*200
len(WD),max(WD),min(WD)

import utfc.SoundF
WD = wavedat*2
np.min(WD)
wave_data= np.array(WD,np.int16)
wave_data.tolist()

a=wave_data[:wavelen]
fft_data=np.abs(np.fft.fft(a))[:wavelen//2]
for i in range(0,len(fft_data),4):
    if fft_data[i]>1000 :print(1,end='')
    else: print(0,end='')
print()

print(fft_data.tolist())

plt.plot(fft_data)
plt.show()