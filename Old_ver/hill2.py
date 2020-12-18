#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


# 加密：c=K*m
def hill_encode(K, m):
    rank = K.shape[0]  # Key矩阵的秩，要求满秩
    m = list(map(lambda c: ord(c) - ord('a'), m))
    padding = (rank - len(m) % rank) % rank
    m.extend([0] * padding)  # 用a填充
    m = np.mat(m)
    m = m.reshape(rank, m.size // rank)  # 重排列
    c = (K * m) % 26  # 加密
    c = c.reshape(1, c.size)  # 重排成1行
    c = c.tolist()[0]
    print(c)
    c = list(map(lambda i: chr(i + ord('a')), c))  # 数字转字符
    return ''.join(c)


# In[3]:


# 模反函数，求满足ab=1 mod m的b
def modinv(a, m):
    # 辗转相除法
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


# In[57]:


# 解密：m=K1*c
def hill_decode(K, c):
    det = np.linalg.det(K)  # K的行列式，要求与26互质
    # print('K.I=',K.I)
    Kw = np.round(K.I * det).astype(np.int) % 26  # K的伴随矩阵，K*K_1=1，Kw=K_1*det(K)
    # print('K*K.I=',K*K.I)
    # print('Kw=',Kw)
    K1 = (Kw * modinv(int(det), 26)) % 26  # 解密矩阵，这个是关键：
    # print('K1',K1)
    rank = K1.shape[0]
    c = list(map(lambda c: ord(c) - ord('a'), c))
    c = np.mat(c)
    c = c.reshape(rank, c.size // rank)  # 重排列
    m = (K1 * c).astype(np.int32) % 26  # 解密
    m = m.reshape(1, m.size)
    m = m.tolist()[0]
    m = list(map(lambda i: chr(i + ord('a')), m))
    return ''.join(m)


# In[58]:


K = np.mat([[6, 13, 20], [24, 16, 17], [1, 10, 15]]).T
m = 'cat'
c = hill_encode(K, m)
print(c)
m2 = hill_decode(K, c)
print(m2)

# In[59]:


# find a bug ？？？
import numpy as np

K = np.mat([[6, 13, 20], [24, 16, 17], [1, 10, 15]]).T
det = np.linalg.det(K)  # K的行列式，要求与26互质
print('K.I=', K.I)
Kw = (K.I * det)  # .astype(np.int)#%26#K的伴随矩阵，K*K_1=1，Kw=K_1/det(K)
print('K*K.I=', (K * K.I).astype(np.int))
print('Kw=', Kw)
Kw2 = Kw.astype(np.int)
print('Kw2=', Kw2)
