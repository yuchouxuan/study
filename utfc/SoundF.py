import wave
import matplotlib.pyplot as plt
import numpy as np
import struct


class WavF:
    strData = ''
    params = ''
    nchannels = 0
    sampwidth = 0
    framerate = 0
    nframes = 0
    strData = ''
    waveData = []

    def __init__(self, fn=''):
        self.open(fn)

    def open(self, fn=''):
        with wave.open(fn, 'rb') as f:
            self.params = f.getparams()
            print('params:', self.params)
            self.nchannels, self.sampwidth, self.framerate, self.nframes = self.params[:4]
            self.strData = f.readframes(self.nframes)  # 读取音频，字符串格式
            self.waveData = np.frombuffer(self.strData, dtype=np.int16).tolist()  # 将字符串转化为int

    def showit(self):
        time = np.arange(0, self.nframes) * (1.0 / self.framerate)
        plt.plot(time, self.waveData)
        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude")
        plt.title("Single channel wavedata")
        plt.grid('on')  # 标尺，on：有，off:无。
        plt.show()


def CreateWav(fn='', datas=[0], framerate=8000, channel=2, sampwidth=2):
    with wave.open(fn, 'w') as f:
        f.setnchannels(channel)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        if isinstance(datas[0], list):
            for i in range(len(datas[0])):
                for j in range(channel):
                    try:
                        f.writeframesraw(struct.pack('h', int(round(datas[j][i]))))
                    except:
                        f.writeframesraw(struct.pack('h', 0))
        else:
            for i in datas:
                f.writeframesraw(struct.pack('h', int(round(i))))


if __name__ == '__main__':
    s = WavF()
    dec0 = ''
    for i in range(s.nframes):
        if s.waveData[i] < 0: s.waveData[i] = -s.waveData[i]
        if s.waveData[i] < 10000:
            s.waveData[i] = 0
            dec0 += '|'
        else:
            s.waveData[i] = 1
            dec0 += '-'

    print(dec0)

    pass
