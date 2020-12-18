# -*- coding: utf-8 -*- 
'''
代码中各个函数的说明如下
calc_cofactor(mat) #计算矩阵mat的伴随矩阵
calc_inverse(n) #计算 n在Z_26下的逆元
crack() #计算密钥的主体函数
'''

import numpy as np
import numpy.linalg as lg


def calc_cofactor(mat):
    ans = np.zeros([len(mat), len(mat)])
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            ans[i, j] = (-1) ** (i + j) * lg.det(np.delete(np.delete(mat, j, axis=1), i, axis=0))
    return (np.around(ans).astype(int) % 26).T


def calc_inverse(n):
    for i in range(1, 26):
        if i * n % 26 == 1:
            return i


def crack():
    y = "dsrmsioplxljbzullm"
    x = "adisplayedequation"
    y = [ord(i) - ord('a') for i in y]
    x = [ord(i) - ord('a') for i in x]
    x1 = np.array(x[0:9]).reshape(3, 3)
    x2 = np.array(x[9:]).reshape(3, 3)
    y1 = np.array(y[0:9]).reshape(3, 3)
    y2 = np.array(y[9:]).reshape(3, 3)
    Y = (y2 - y1) % 26
    X = (x2 - x1) % 26
    X_inverse = (calc_inverse(int(lg.det(X) % 26)) * calc_cofactor(X)) % 26
    key = np.dot(X_inverse, Y) % 26
    b = ((y1 - np.dot(x1, key)) % 26)[0, :]
    return key, b


key, b = crack()
print('key is \n', key)
print('b is ', b)

import numpy as fw


def Euclid(a, b=26):
    x1 = 1
    x2 = 0
    x3 = a
    y1 = 0
    y2 = 1
    y3 = b

    while y3 != 0:
        q = int(x3 / y3)
        t1 = x1 - q * y1
        t2 = x2 - q * y2
        t3 = x3 - q * y3

        x1 = y1
        x2 = y2
        x3 = y3

        y1 = t1
        y2 = t2
        y3 = t3

        if x1 < 0:
            x1 = x1 + b
    return x1


# 求模m的逆矩阵
def want1(x):
    a = x[0, 0]
    b = x[0, 1]
    c = x[1, 0]
    d = x[1, 1]
    k = a * d - b * c
    k = Euclid(k)
    x1 = [[(k * d) % 26, (-k * b) % 26], [(-k * c) % 26, (k * a) % 26]]
    return x1


# 加密
def hill2encrypt(c1, A):
    c11 = [0, 0]
    c1111 = []
    for i in range(len(c1)):
        if c1[i] == 'z':
            c1[i] = '`'
    for i in range(len(c1)):
        if i % 2 == 0:
            c11[0] = ord(c1[i]) - 96
        else:
            c11[1] = ord(c1[i]) - 96
            strc11 = str(c11[0]) + ';' + str(c11[1])
            c111 = fw.mat(strc11)
            c111 = A * c111
            x = chr((int(c111[0][0])) % 26 + 96)
            y = chr((int(c111[1][0])) % 26 + 96)
            if x == '`':
                x = 'z'
            if y == '`':
                y = 'z'
            c112 = x + y
            c1111.append(c112)
    c1111 = ''.join(c1111)
    print('加密后为', c1111)


# 解密
# def hill2decrypt(d1):
def hill2decrypt(d1, A1):
    d11 = [0, 0]
    d1111 = []
    for i in range(len(d1)):
        if d1[i] == 'z':
            d1[i] = '`'
    for i in range(len(d1)):
        if i % 2 == 0:
            d11[0] = ord(d1[i]) - 96
        else:
            d11[1] = ord(d1[i]) - 96
            strd11 = str(d11[0]) + ';' + str(d11[1])
            d111 = fw.mat(strd11)
            d111 = A1 * d111
            x = chr((int(d111[0][0])) % 26 + 96)
            y = chr((int(d111[1][0])) % 26 + 96)
            if x == '`':
                x = 'z'
            if y == '`':
                y = 'z'
            d112 = x + y
            d1111.append(d112)
    d1111 = ''.join(d1111)
    print('解密后为', d1111)


'''
print("请输入一段4字母的用hill2加密的明文和其密文（线性无关）")
a = input('明文为：')
b = input('密文为：')
c = input('想要加密的明文为：')
d = input('想要解密的密文为：')'''

a = 'taco'
b = 'ucrs'
c = 'clintonisgoingtovisitacountryinmiddleeastt'
d = 'ojwpiswazuxauuiseabaucrsiplbhaammlpjjotenh'

# 输入已知的明文和密文
a = list(a)
for i in range(4):
    if a[i] == 'z':
        a[i] == '`'
a[0] = str(ord(a[0]) - 96) + ' '
a[1] = str(ord(a[1]) - 96) + ' '
a[2] = str(ord(a[2]) - 96) + ';'  # abcdefghijklmnopqrstuvwxyz
a[3] = str(ord(a[3]) - 96)  # cfglkroxsdwjapevibmhqnutyz
a[1], a[2] = a[2], a[1]
a = ''.join(a)

b = list(b)
for i in range(4):
    if b[i] == 'z':
        b[i] == '`'
b[0] = str(ord(b[0]) - 96) + ' '
b[1] = str(ord(b[1]) - 96) + ' '
b[2] = str(ord(b[2]) - 96) + ';'
b[3] = str(ord(b[3]) - 96)
b[1], b[2] = b[2], b[1]
b = ''.join(b)

# a,b变为矩阵
a1 = fw.mat(a)
b1 = fw.mat(b)
'''print('a1:\n',a1)
print('b1\n',b1)
'''
A = b1 * want1(a1)
A1 = want1(A)
'''print(A1)'''

# 对要明文和密文操作
c1 = list(c)
d1 = list(d)
print('A:\n', A)
print('A1:\n', A1)
hill2encrypt(c1, A)
hill2decrypt(d1, A1)
