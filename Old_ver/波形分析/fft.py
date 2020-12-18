f = FileF.f2s(down + 'ASKnoise.txt').split()
num = [float(i) for i in f]
import numpy
import matplotlib.pyplot as plt

b = numpy.abs(numpy.fft.fft(num))
# 求变换后的幅值谱：np.abs(F);
# 求变换后的相位谱：np.angle(F)。

half_x = [i for i in range(len(num) // 2)]  # 取一半区间

a = numpy.abs(numpy.fft.fft(num[0:100]) / 100)
c = numpy.abs(numpy.fft.fft(num[100:200]) / 100)
d = numpy.abs(numpy.fft.fft(num[200:300]) / 100)
e = numpy.abs(numpy.fft.fft(num[300:400]) / 100)

x = [i for i in range(50)]

plt.subplot(331)
plt.plot(x, a[:len(a) // 2], color='black')
plt.ylim(0, 1)
plt.title('0-100')

plt.subplot(332)
plt.plot(x, c[:len(c) // 2], color='black')
plt.ylim(0, 1)
plt.title('100-200')

plt.subplot(333)
plt.plot(x, d[:len(d) // 2], color='black')
plt.ylim(0, 1)
plt.title('200-300')

plt.subplot(334)
plt.plot(x, e[:len(e) // 2], color='black')
plt.ylim(0, 1)
plt.title('300-400')

plt.show()
