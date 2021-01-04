import wave
import numpy as np

def openwave(fn=''):
    with wave.open(fn, 'rb') as f:
        params = f.getparams()
        print('params:', params)
        nchannels, sampwidth, framerate, nframes = params[:4]
        strData = f.readframes(nframes)  # 读取音频，字符串格式
        return np.frombuffer(strData, dtype=np.int16).tolist()  # 将字符串转化为int
data=openwave('example.wav')[::-1]
LS=''
for i in data:
    if i&1==1 : LS+='1'
    else:LS+='0'

b=[]
for i in range(0,len(LS),8):
    lsb=int(LS[i:i+8],2)
    print(chr(lsb),end='')
    b.append(lsb)
open('a.png','wb').write(bytes(b[::-1]))