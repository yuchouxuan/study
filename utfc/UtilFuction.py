import numpy as np

from itertools import permutations
from math import radians, cos, sin, asin, sqrt
from utfc.ArrayFunc import *
import gmpy2


def m_bin(n, clong):  # 转定长二进制
    ret = ''
    b0 = (n >= 0)  # 非负数标志
    if not b0:    n = -n - 1
    ret = str(bin(n))[2:]
    if len(ret) < clong: ret = '0' * (clong - len(ret)) + ret
    if not b0:
        rx = ret
        ret = ""
        for i in rx:
            if i == '0': ret += '1'
            if i == '1': ret += '0'
    return ret


class MathCump:
    @staticmethod
    def Geodistance(lng1, lat1, lng2, lat2, R=6371.393):  # 地球平均半径，6371km
        lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)])  # 经纬度转换成弧度
        dlon = lng2 - lng1
        dlat = lat2 - lat1
        return 2 * asin(sqrt(sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2)) * R

    @staticmethod
    def AllRange(listx=[]):  # 全排列
        ret = []
        for x in list(permutations(listx)):
            ret.append(list(x))
        return ret

    @staticmethod
    def prime(inc=2):  # 比较小的求因式分解
        num = int(inc)
        ret = []
        if (num < 2): return ret;
        n = num
        ty = 2
        while (num > 2):
            while (ty <= n):
                while (num % ty == 0):
                    num = num // ty
                    ret.append(int(ty))
                ty = gmpy2.next_prime(ty)
        return ret

    @staticmethod
    def MitrxRe(array=[]):  # 矩阵求逆
        if len(array) == 0: return []
        a = np.linalg.inv(np.array(List2Array(array))).tolist()
        if isinstance(array[0], list):
            return a
        else:
            return Array2List(a)


# 进制转换（60以内）
def baseCov(num, b=16) -> str:
    return ((num == 0) and "0") or \
           (baseCov(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz" +
            'abcdefghijklmnopqrstuvwxyz'.upper()[num % b])


# 在球面上找三点定位法
def Geod_FindPos(pos=[], dis=[], rd=4):
    def Sum_dDis(lo, la, pos=[], dis=[]):  # 求 (lo,la)到 pos各点距离与指定距离的绝对值差
        ret = 0;
        for i in range(len(pos)):
            dbx = abs(MathCump.Geodistance(pos[i][0], pos[i][1], lo, la) - dis[i])
            ret += dbx
        return ret

    def FindMin(pos=[0, 0, 1e7], posl=[], disl=[], r=[]):  # 遍历穷举
        ret = pos.copy()
        o = pos[0] - r[0]
        while o <= pos[0] + r[0]:
            a = pos[1] - r[1]
            while a <= pos[1] + r[1]:
                sumd = Sum_dDis(o, a, posl, disl)
                if (sumd < ret[2]):
                    ret = [o, a, sumd]
                    print(ret)
                a += r[2]
            o += r[2]
        return ret

    pp = [0, 0, 1e7]
    r = [180, 90, 10]
    for i in range(rd):
        pp = FindMin(pp, pos, dis, r)
        r = [r[0] / 10, r[1] / 10, r[2] / 10]

    print('- ' * 20)
    print("(%f,%f):%f" % (pp[0], pp[1], pp[2]))
    print('- ' * 20)


class frange:
    l=0
    r=0
    step=1
    def __init__(self,l=None,r=None,s=None):
        if l==None :l=0
        if s==None :s =1
        if r==None:
            r=l
            l=0
        if (r>l and s<0) or (r <l and s >0) or (s==0):
            self.r=self.l=r
            self.step=1
        else:
            self.r=r
            self.l=l
            self.step=s

    def __iter__(self):
        n=self.l
        while  (self.step>0 and n < self.r) or (self.step < 0 and n > self.r ) :
            yield n
            n += self.step
        return

class Area(object):
    convGT=True # 如 ascii(mid(flag,1,1)) > ?
    Ldata=[]
    bl=0
    br=0
    Test=None
    ans=None
    def __init__(self,l=[],dirGT=True,reSort=False):
        self.convGT=dirGT
        self.Ldata=l.copy()
        if(reSort):
            self.Ldata.sort()
        self.br=len(self.Ldata)-1
    @staticmethod
    def fromNum(l=1,r=1):
        return Area([i for i in range(l,r+1)])
    def __iter__(self):

        while self.br != self.bl :
            if self.convGT:  # 大于号模式
                mid = self.bl + (self.br - self.bl) // 2
            else:
                mid = self.br - (self.br - self.bl) // 2
            self.ans= self.Ldata[mid]
            yield  self.ans
            if self.br-self.bl==1:
                if self.convGT:  # 区间只有两个元素时 接受测试的必为左侧元素 实际>测试
                    if self.Test:
                        self.bl = self.br  # 实际值大于左侧值，则向右收缩，返回右侧值
                    else:
                        self.br = self.bl  # 实际值小于等于左侧值，向左收缩，返回左侧值
                else:  # 区间只有两个元素时 接受测试的必为右侧元素 实际<测试
                    if self.Test:
                        self.br = self.bl  # 实际值小于小右侧值，则向左收缩，返回左侧值
                    else:
                        self.bl = self.br  # 实际值大于等于右侧值（大于是不可能的），向右收缩，返回右侧值
                self.ans = self.Ldata[self.bl]
                return self.ans


            if self.Test:  # 测试通过
                if self.convGT:   # ascii(mid(flag,1,1)) > ? == true  实际值大于测试值
                    self.bl=mid   #  l->mid 向右收缩
                else:             # ascii(mid(flag,1,1)) < ? == true  实际值小于测试值
                    self.br=mid   #  r->mid 向左收缩
            else : #测试不通过
                if self.convGT:   # ascii(mid(flag,1,1)) > ? == false  实际值小于等于测试值
                    self.br=mid   # r->mid 向左收缩
                else:             # ascii(mid(flag,1,1)) < ? == false  实际值大于等于测试值
                    self.bl=mid   # l->mid 向右收缩




if __name__ == '__main__':
    print(MathCump.Geodistance(0, 0, -1, -1))
    pass
