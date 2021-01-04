import wave
import cv2 as cv
import numpy as np
from PIL import Image, ImageFont
from PIL import ImageDraw
#学python语法时练手写的一个用于操作图像的类，代码效率很低，但实在懒得重写了
class imgBase:
    img = None
    height = 0
    weight = 0
    def __init__(self, w=100,h=100):
        self.weight = w
        self.height = h
        self.img = np.zeros((h, w, 3), np.uint8)
        self.img.fill(255)
    def show(self, wname='image'):
        cv.imshow(wname, self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    def setxy(self, x=0, y=0, col=[0, 0, 0]):
        height = self.img.shape[0]
        weight = self.img.shape[1]
        if x < 0: x = -x
        if y < 0: y = -y
        self.img[y % height, x % weight] = col
    def save(this, fn=''):
        if fn == '': fn = this.fn
        cv.imwrite(fn, this.img)
import matplotlib.pyplot as plt

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