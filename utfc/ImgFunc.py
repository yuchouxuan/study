import cv2 as cv
import numpy as np
import struct
import binascii
from PIL import Image, ImageDraw, ImageFont
import pyzbar.pyzbar as pyzbar
import imageio
import matplotlib.pyplot as plt
import tqdm

'''opencv 其他常用函数
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
画圆:
cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
        img：要画的圆所在的矩形或图像
        center：圆心坐标，如 (100, 100)
        radius：半径，如 10
        color：圆边框颜色，如 (0, 0, 255) 红色，BGR
        thickness：正值表示圆边框宽度. 负值表示画一个填充圆形
        lineType：圆边框线型，可为 0，4，8
        shift：圆心坐标和半径的小数点位数
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
画线
:cv2.line(img, pt1, pt2, color[, thickness[, lineType[, shift]]])
        img：要画的圆所在的矩形或图像
        pt1：直线起点
        pt2：直线终点
        color：线条颜色，如 (0, 0, 255) 红色，BGR
        thickness：线条宽度
        lineType：
        - 8 (or omitted) ： 8-connected line
        - 4：4-connected line
        - CV_AA - antialiased line
        shift：坐标点小数点位数
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
画方块
cv2.rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]]) 
        mg：要画的圆所在的矩形或图像
        pt1：矩形左上角的点
        pt2：矩形右下角的点
        color：线条颜色，如 (0, 0, 255) 红色，BGR
        thickness：线条宽度
        lineType：
        8 (or omitted) ： 8-connected line
        4：4-connected line
        CV_AA - antialiased line
        shift：坐标点小数点位数
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
画椭圆  
cv2.ellipse(img, center, axes, rotateAngle, startAngle, endAngle, color[, thickness[, lineType[, shift]]]) 
        img：要画的圆所在的矩形或图像
        center：椭圆的中心点
        axes：椭圆的长半轴和短半轴的大小
        rotateAngle：椭圆的旋转角度
        startAngle：椭圆弧的起始角度
        endAngle：椭圆弧的终止角度
        color：线条颜色，如 (0, 0, 255) 红色，BGR
        thickness：线条宽度
        lineType：
        8 (or omitted) ： 8-connected line
        4：4-connected line
        CV_AA - antialiased line
        shift：坐标点小数点位数
'''


class imgBase:
    img = None
    fn = ''
    height = 0
    weight = 0
    channels = 0

    def __init__(self, fn=None, w=100, h=100):
        if fn == None:
            self.fn = 'Temp'
            self.createImage(w, h)
            return
        try:
            self.img = cv.imread(fn)
            self.fn = fn
            self.height = self.img.shape[0]
            self.weight = self.img.shape[1]
            self.channels = self.img.shape[2]
            print(fn, self.weight, self.height, self.channels)
        except:
            pass

    def zbar(self):
        code = ''
        try:
            code = pyzbar.decode(self.img)
            code = code[0][0]
        except:
            pass
        return code

    def show(self, wname='image'):
        cv.imshow(wname, self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def getxy(self, x=0, y=0):
        height = self.img.shape[0]
        weight = self.img.shape[1]
        channels = self.img.shape[2]
        if x < 0: x = -x
        if y < 0: y = -y
        ret = []
        for c in range(channels):
            ret.append(self.img[y % height, x % weight, c])
        return ret

    def setxy(self, x=0, y=0, col=[0, 0, 0]):
        height = self.img.shape[0]
        weight = self.img.shape[1]
        if x < 0: x = -x
        if y < 0: y = -y
        self.img[y % height, x % weight] = col


    def drawtext(self, text='', x=0, y=0, size=18, col=(0, 0, 0)):
        img = Image.fromarray(cv.cvtColor(self.img, cv.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        fontStyle = ImageFont.truetype("font/simsun.ttc", size, encoding="utf-8")
        draw.text((x, y), text, col, font=fontStyle)
        self.img = cv.cvtColor(np.asarray(img), cv.COLOR_RGB2BGR)


    def createImage(self, w=100, h=100):
        self.weight = w
        self.height = h
        self.img = np.zeros((h, w, 3), np.uint8)
        self.img.fill(255)


    def rev(self):  # 负片
        for x in tqdm.trange(self.weight):
            for y in range(self.height):
                c = self.getxy(x, y)
                self.setxy(x, y, [~c[0], ~c[1], ~c[2]])


    def drawHist(self, line=''):  # 直方图
        b, g, r = cv.split(self.img)
        hists, bins = np.histogram(b.flatten(), 256, [0, 256])
        plt.plot(hists, line + 'b')
        hists, bins = np.histogram(g.flatten(), 256, [0, 256])
        plt.plot(hists, line + 'g')
        hists, bins = np.histogram(r.flatten(), 256, [0, 256])
        plt.plot(hists, line + 'r')




def save(this, fn=''):
    if fn == '': fn = this.fn
    cv.imwrite(fn, this.img)


class PicQP(imgBase):  # 棋盘绘图，二维码用
    w = 600
    dw = 60

    def __init__(self, w=600, dw=30):
        self.w = w
        self.dw = dw
        self.img = np.zeros((w + 1, w + 1, 3), np.uint8)
        self.img.fill(255)

    def show(self):
        cv.imshow('image', self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def drawBox(self, pos=(0, 0), col=(128, 128, 128)):
        x0 = int(self.dw * pos[0])
        y0 = int(self.dw * pos[1])
        cv.rectangle(self.img, (x0, y0), (x0 + self.dw, y0 + self.dw), col, -1, 0)

    @staticmethod
    def fromStr(w, h, imgb="0000000", dw=1):
        qp = PicQP(max(w, h) * dw, dw)
        cont = 0
        for i in imgb:
            if (cont >= w * h): break
            if i == '0':
                qp.drawBox((cont // w, cont % w), [0, 0, 0])
            cont += 1
        return qp


class ImgBits(imgBase):  # 像素操作

    def b2l(self):
        if self.fn == '': return []
        height = self.img.shape[0]
        weight = self.img.shape[1]
        channels = self.img.shape[2]
        retx = []
        for row in range(height):
            for col in range(weight):
                ch = []
                for c in range(channels):
                    ch.append(self.img[row, col, c])
                retx.append(ch)
        return retx

    def b2ml(self):
        if self.fn == '': return []
        height = self.img.shape[0]
        weight = self.img.shape[1]
        channels = self.img.shape[2]
        retx = []
        for row in range(height):
            coll = []
            for col in range(weight):
                ch = []
                for c in range(channels):
                    ch.append(self.img[row, col, c])
                coll.append(ch)
            retx.append(coll)
        return retx

    @staticmethod
    def gif2bl(fn=''):
        rtl = []
        im = Image.open(fn)
        print("FrameCont:", im.n_frames)
        for i in range(im.n_frames):
            im.seek(i)
            CF = Image.new("RGBA", im.size)
            CF.paste(im)
            img = cv.cvtColor(np.asarray(CF), cv.COLOR_RGB2BGR)
            nb = ImgBits()
            nb.img = img
            nb.height = im.height
            nb.weight = im.width

            nb.fn = 'Tmp'
            rtl.append(nb)
        return rtl

@staticmethod
def imgl2gif(image_list, gif_name, duration=0.35):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return


class PicF:  #
    @staticmethod
    def PNG_wh_crc(fn='', cx=0):  # PNG求宽高

        m = open(fn, "rb").read()
        k = 0
        if cx == 0:
            cx = m[0x1d] << 24 | m[0x1e] << 16 | m[0x1f] << 8 | m[0x20]
        print(fn)
        print('- ' * 15)
        print('CRC: x%X' % cx)

        for i in range(5000):
            for j in range(5000):
                c = m[12:16] + struct.pack('>i', i) + struct.pack('>i', j) + m[24:29]
                crc = binascii.crc32(c) & 0xffffffff
                if crc == cx:
                    print("\r\nW:%08X\r\nH:%08X" % (i, j));
        print('- ' * 15)

    @staticmethod
    def CompImgFileALL(fn1='', fn2=''):
        for i in range(8):
            for j in range(3):
                PicF.CompImgFile('c:\\ctf\\1.png', 'c:\\ctf\\2.png', (j, i),SIG=True)
        cv.waitKey()
        cv.destroyAllWindows()


    @staticmethod
    def CompImgFile(fn1='', fn2='', bits=(0, 0),SIG=False):
        img1 = imgBase(fn1)
        img2 = imgBase(fn2)
        PicF.CompImg(img1, img2,bits=bits)

    @staticmethod
    def CompImg(img1, img2, bits=(0, 0),SIG=False):
        w = min(img1.weight, img2.weight)
        h = min(img1.height, img2.height)
        c = min(img1.channels, img2.channels)
        img = np.zeros((h + 1, w + 1, c), np.uint8)
        img.fill(0)
        for i in range(w):
            for j in range(h):
                b1 = img1.getxy(i, j)
                b2 = img2.getxy(i, j)
                if bits == (0, 0):
                    for x in range(c):
                        xr = 0
                        if b1[x] ^ b2[x] == 0: xr = 255
                        img[j,i] = img[j,i] | xr
                elif not ((b1[bits[0]]) & (1 << bits[1]) & 0xff)  < ((b2[bits[0]])== (1 << bits[1]) & 0xff):
                    img[j, i] = 255
        cv.imshow('image%d,%d'%bits, img)
        if SIG:
            cv.waitKey(0)
            cv.destroyAllWindows()




if __name__ == '__main__':
    pass
