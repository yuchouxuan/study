import seaborn as sns
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from sklearn.metrics import accuracy_score
import tqdm
import numpy as np
from sklearn.metrics import classification_report
# 训练集
trainFile=open("c:\\ctf\\t.txt",'r').readlines()
tx=[]
ty=[]
for i in trainFile:
    try:
        s=i.strip().split('\t')
        ty.append(int(s[0]))
        tx.append(eval(s[1]))
    except:
        print("err:",i)

#训练集 和测试集分赃，反正给的多，直接五千测试 ok
t_x = tx[:-5000]
t_y = ty[:-5000]
t_y = np.array(t_y)
# 测试集
p_x = tx[-5000:]
p_y = ty[-5000:]
p_y = np.array(p_y)
q_x=[]
#flag文件读取
FlagFile=open("c:/ctf/flag.txt",'r').readlines()
for i in FlagFile:
    try:
        q_x.append(eval(i))
    except:
        print("err:",i)

in_V = 6

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
        # 输出层
        self.lout = nn.Softmax(dim=1)
        self.drop = nn.Dropout(p=0.5) #防止过拟合的drop函数，其实这个题厚道的送分狸给的训练集很友好，没有也行，而且吧drop设的小点（比如0.1）出结果更快些,
                                      #但是，玩这东西，避免过拟合应该是类似于强迫症的存在，所以，我还是决定用0.5的默认值了 哈哈

    def forward(self, x):
        x = F.sigmoid(self.lin(x)) #激活函数试了一下 sigmoid是效果最好的
        x = self.drop(x)
        x = F.sigmoid(self.h0(x))
        x = self.drop(x)
        x = F.sigmoid(self.h1(x))
        x = self.drop(x)
        x = F.sigmoid(self.h2(x))
        return x  #r如果用nn.NLLLoss之类的代价函数 需要softMax下，交叉熵可以不要下面的
        x = self.drop(x)
        return self.lout(x)
net = Net()  # 实例化神经网络

#把训练集、测试集、问题集转成张量
t_x = torch.tensor(np.array(t_x[::-1]), dtype=torch.float)
t_y= torch.tensor(np.array(t_y[::-1]), dtype=torch.long)
q_x = torch.tensor(np.array(q_x), dtype=torch.float)
p_x = torch.tensor(np.array(p_x), dtype=torch.float)
p_y= torch.tensor(np.array(p_y), dtype=torch.long)

#你需要一块能做CUDA加速的显卡
device =torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

optimizer = optim.Adam(net.parameters(), lr=0.001)  # 据说adam算法比较时髦，且好用 其实SGD啥的都行 可以挨个试试
criterion = nn.CrossEntropyLoss()# 交叉熵损失函数

error=[]
zql=[]
net.to(device)
plt.figure(figsize=(10, 2))
for epoch in tqdm.trange(3000): #训练三千轮，其实如果到了1000轮的时候还啥都不是，那就重新 开始吧，估计是初始梯度随机到一个尴尬的地方去了
    optimizer.zero_grad()  #梯度清零
    y_pred = net(t_x.to(device))  #正向
    loss = criterion(y_pred, t_y.to(device)) #损失计算
    loss.backward()#反馈
    optimizer.step()#优化
    if epoch % 2==0:#动态显示，如果训练了1000轮还不知所云就重启吧，这玩意很玄学 可以调大一些 但是我喜欢看着flag慢慢浮现的样纸，你咬我啊
        error.append(loss.item())
        y_pred = net(p_x.to(device))
        y_pred = torch.argmax(y_pred, dim=1)
        zql.append(float(accuracy_score(p_y, y_pred.cpu())))
        y_pred = net(q_x.to(device))
        y_pred = np.array(torch.argmax(y_pred.cpu(), dim=1))
        img=y_pred.reshape(79,991)#图像长宽，分解因数可得到
        plt.cla()
        plt.imshow(img)
        plt.pause(0.0001)

plt.show()
y_pred = net(p_x.to(device))
y_pred = torch.argmax(y_pred, dim=1)
print(classification_report(p_y, y_pred.cpu()))
torch.cuda.empty_cache()
sns.lineplot(data=error,color='red',label='loss')
sns.lineplot(data=zql,color='green',label='acc')
plt.show()
