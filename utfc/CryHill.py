# 导入numpy模块
import numpy as np
import string
from sympy import Matrix

alphabet = string.ascii_uppercase  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 0-25对应A-Z


def convert2matrix(s, dimension):  # s:字符串，dimension维度
    for index, i in enumerate(s):  # 产生 index ,i = 0, A、1,B、2，C这样的序列对
        values = []
        if index % dimension == 0:
            for j in range(0, dimension):
                values.append([alphabet.index(s[index + j])])  # alphabet.index('A')获取对应序列
            if index == 0:
                m_mat = np.matrix(values)
            else:
                m_mat = np.hstack((m_mat, values))  # 使用np.hstack,使得构造的矩阵，字符串读取应是按列读取
    return m_mat


def Bang_k(cipher, plain, dimension):
    '''参数 ：部分密文和明文、维度'''
    cipher_m = convert2matrix(cipher, dimension)  # 密文矩阵
    plain_m = convert2matrix(plain, dimension)  # 明文矩阵
    # 将cipher_m和plain_m Matrix化
    cipher_m_M = Matrix(cipher_m)
    plain_m_M = Matrix(plain_m)
    # 求cipher_m_M模26的逆元
    try:
        cipher_m_M_inv = cipher_m_M.inv_mod(26)
        # 根据 K= X-1 Y 求密钥K
        Key = plain_m_M * cipher_m_M_inv % 26
        return Key
    except ValueError:
        return Matrix([0])


def Matrix2Strings(matr, demension):
    matr_list = matr.tolist()
    plaintxt = ''
    for i in range(len(matr_list[0])):
        for row in matr_list:
            plaintxt += alphabet[row[i]]

    return plaintxt


def main():
    dic_keys = []
    unknown_c = 'AUJPSOADUIWAAMYOKQNTRLKY'
    m = 'BABYHILLS'
    for i in range(len(unknown_c) - 9 + 1):
        dic_keys.append(Bang_k(unknown_c[i:i + 9], m, 3).tolist())
    print("K的逆：", dic_keys)
    cipher_all_M = convert2matrix(unknown_c, 3)
    plain_all_M = Matrix(dic_keys[0]) * Matrix(cipher_all_M) % 26
