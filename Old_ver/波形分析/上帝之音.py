import wave
import numpy

## 第一：音频->0101010101
wav = wave.open('/users/s.h/Downloads/' + 'godwave.wav', 'rb')
params = wav.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
## 读取音频
## 音频关键参数 音轨、载波、频率、数据点
strData = wav.readframes(nframes)
## 数据字符串
waveData = numpy.fromstring(strData, dtype=numpy.int16)
## 转数值型
waveData = abs(waveData * 1.0 / (max(abs(waveData))))  # 对负半周进行翻转
# 下面对波形数据进行二值化处理，也就是大于阈值的 定义为1，小于阈值的定义为0
# 为了减少毛刺采用平均值算法 平滑曲线
bits = ""  # 存放二值化数据的字符串
gate = 0.2  # 阈值
for i in range(0, len(waveData), 5):  # 临近四个点取平均值
    avg = numpy.average(waveData[i:i + 4])
    if avg > gate:
        bits += '1'
    else:
        bits += '0'
# 因为不知道最小脉宽，所以要分析一下脉宽情况
w = {}
counter = 0
last = '0'
for i in bits:
    if i == last:
        counter += 1
    else:
        w[counter] = ''
        counter = 0
print(w.keys())
# dict_keys([0, 25, 13, 26, 12])  可见最小脉宽为12-13 宽脉冲为 25-26
# 接下来就把连续12个0 或者1 替换成 x,y 剩下的 0，1 不成气候扔掉即可
bits = bits.replace('0' * 12, 'x').replace('1' * 12, 'y').replace('0', '').replace('1', '')
# 曼彻斯特解码
decode = ''
for i in range(0, len(bits), 2):
    if 'xy' == bits[i:i + 2]:
        decode += '0'
    else:
        decode += '1'

res = hex(int(decode, 2))[2:-1]
print(res)
