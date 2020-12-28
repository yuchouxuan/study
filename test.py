import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import tqdm
import numpy as np

import math
import seaborn as sns
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from sklearn.metrics import accuracy_score
import random
import numpy as np
def func_en(arr=[]):
    x= (6*arr[0]+7*arr[1]+3*arr[2]+7*arr[3]+3*arr[4])*(math.sin(math.pi*arr[5]/24))
    return 1 if x>=0 else 0

# 训练集, 因为这个题可以实时看到结果，反正我们只需要拿到flag，又不准备训练个多好的网络，所以完全不需要测试集
trainFile=open("c:\\ctf\\t.txt",'r').readlines()
t_x = []
t_y = []
for i in trainFile:
        s=i.strip().split('\t')
        t_y.append(int(s[0]))
        t_x.append(eval(s[1]))
#flag文件读取
q_x=[]
FlagFile=open("c:/ctf/flag.txt",'r').readlines()
for i in FlagFile: q_x.append(eval(i))


import cv2
img=cv2.imread("c:\\ctf\\flag.png",1)
iq_y=img.flatten()[1::3]//200
q_x=[]


import tqdm as  tq
print('生成测试数据：')
for i in tq.tqdm(iq_y):
    t = [random.randint(-64, 64) for i in range(6)]
    while func_en(t) != i:
        t= [random.randint(-64,64) for i in range(6)]
    q_x.append(t)




in_V = 6 #输入张量的维度
#定义一个 三层全连接网络
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # 输入层
        self.lin = nn.Linear(in_V, in_V * 64)
        # 全连接层
        self.h0 = nn.Linear(in_V * 64, in_V * 64)
        self.h1 = nn.Linear(in_V * 64, in_V * 64)
        self.h2 = nn.Linear(in_V * 64, 2)
        self.drop = nn.Dropout(p=0.3) #防止过拟合的drop函数，其实这个题厚道的送分狸给的训练集很友好，没有也行，而且吧drop设的小点（比如0.1）出结果更快些,
                                      #但是，玩这东西，避免过拟合应该是类似于强迫症的存在，所以，我还是决定用0.5的默认值了 哈哈
    def forward(self, x):
        x = self.drop(F.sigmoid(self.lin(x)))#激活函数试了一下 sigmoid是效果最好的
        x = self.drop(F.sigmoid(self.h0(x)))
        x = self.drop(F.sigmoid(self.h1(x)))
        return F.sigmoid(self.h2(x))

print('训练测试网络：')
#你需要一块能做CUDA加速的显卡
device =torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#把训练集、测试集、问题集转成张量
t_x = torch.tensor(np.array(t_x), dtype=torch.float).to(device)
t_y= torch.tensor(np.array(t_y), dtype=torch.long).to(device)
q_x = torch.tensor(np.array(q_x), dtype=torch.float).to(device)

net = Net().to(device)  # 实例化神经网络
optimizer = optim.Adam(net.parameters(), lr=0.001)  # 据说adam算法比较时髦，且好用 其实SGD啥的都行 可以挨个试试
criterion = nn.CrossEntropyLoss()# 交叉熵损失函数
plt.figure(figsize=(20, 2))
for epoch in tqdm.trange(3000): #训练三千轮，其实如果到了1000轮的时候还啥都不是，那就重新 开始吧，估计是初始梯度随机到一个尴尬的地方去了
    optimizer.zero_grad()  #梯度清零
    y_pred = net(t_x)  #正向
    loss = criterion(y_pred, t_y) #损失计算
    loss.backward()#反馈
    optimizer.step()#优化
    if epoch % 2==0:#动态显示，如果训练了1000轮还不知所云就重启吧，这玩意很玄学 可以调大一些 但是我喜欢看着flag慢慢浮现的样纸，你咬我啊
        y_pred = net(q_x)
        y_pred = np.array(torch.argmax(y_pred.cpu(), dim=1))
        img=y_pred.reshape(79,991)#图像长宽，分解因数可得到
        plt.cla()
        plt.imshow(img)
        plt.pause(0.0001)
plt.show()








































































