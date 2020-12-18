from utfc.ImgFunc import *
from utfc.SoundF import CreateWav

pic = imgBase(down + '1.png')
h = pic.height
w = pic.weight // 25
dy = 60000 / h
dx = 60000 / w
print(h, w)
imgb = []
for i in range(26):
    ch = []
    for y in range(h):
        for x in range(w):
            if pic.getxy(i * w + x + 4, y)[0] < 128:
                ch.append((x, y))
    imgb.append(ch)
x = []
y = []
for i in range(26):
    x.extend([0 for x in range(1000)])
    y.extend([0 for x in range(1000)])
    for j in range(20):
        for k in imgb[i]:
            for w in range(30):
                x.append(k[0] * dx - 30000)
                y.append(30000 - k[1] * dy)

CreateWav(down + 'c.wav', [x, y], 32000)
