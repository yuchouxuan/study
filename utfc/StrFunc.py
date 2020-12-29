from utfc.ArrayFunc import *
from urllib.parse import urlparse, urlunsplit, urlsplit
from urllib import parse
import itertools

WdF = [  # 字频率矩阵
    0.0651738, 0.0124248, 0.0217339, 0.0349835, 0.1041442, 0.0197881,
    0.0158610, 0.0492888, 0.0558094, 0.0009033, 0.0050529, 0.0331490,
    0.0202124, 0.0564513, 0.0596302, 0.0137645, 0.0008606, 0.0497563,
    0.0515760, 0.0729357, 0.0225134, 0.0082903, 0.0171272, 0.0013692,
    0.0145984, 0.0007836]


class CharF:
    @staticmethod
    def str2Dir(cph='', spl1='\n', sp2=':'):
        return {i[:i.find(sp2)].strip():i[i.find(sp2) + 1:].strip()  for i in cph.split(spl1)}
    @staticmethod
    def mapa2b(a="", b=""):
        lenmin = min(len(a), len(b))
        mapret = {i: "" for i in a}
        for i in range(lenmin):
            if not b[i] in mapret[a[i]]:
                mapret[a[i]] += b[i]
        icc = 0
        for i in sorted(mapret):
            if icc % 10 == 0 and icc > 0:
                print()
            icc += 1
            print(i, end='=>')
            for k in mapret[i]:
                cont = 0
                for j in mapret.values():
                    if k in j: cont += 1
                if cont > 1:
                    printc(k, cmd_color.red, '')
                else:
                    print(k, end='')
            print('\t', end='')
        print()
        return mapret

    @staticmethod
    def Chr_permutations(txt='', num=1):  # 排列
        ret = []
        for i in itertools.permutations(txt, num):
            ret.append(i)
        return ret

    @staticmethod
    def Chr_combinations(txt='', num=1):
        ret = []
        for i in itertools.combinations(txt, num):  # 组合
            ret.append(i)
        return ret

    @staticmethod
    def Chr_combinations_with_replacement(txt='', num=1):
        ret = []
        for i in itertools.combinations_with_replacement(txt, num):
            ret.append(i)
        return ret

    @staticmethod
    def Chr_product(txt='', txt2=None, num=1):  # 笛卡尔积
        ret = []
        if txt2 == None: txt2 = txt
        for i in itertools.product(txt, txt2, repeat=num):
            ret.append(i)
        return ret

    @staticmethod
    def chra2z(st='a', end='z') -> list:
        if isinstance(st, str): st = ord(st)
        if isinstance(end, str): end = ord(end)
        return [chr(i) for i in range(st, end + 1)]

    @staticmethod
    def haveAll(a, b):
        for i in b:
            if not i in a: return False
        return True

    @staticmethod
    def int2binstr(inp, bs=2, lenb=0):
        if isinstance(inp, str):
            inp = int(inp, bs)
        b = bin(inp)[2:]
        if lenb != 0:
            b = '0' * (lenb - (len(b) % lenb)) + b
        return CharF.num2str(b, spl=8, bs=2)


    @staticmethod
    def getSame(inc='', b1=True, b2=True, b3=True):
        hs = 'suctf.c' + inc
        def getUrl(url):
            url = url
            host = parse.urlparse(url).hostname
            if host == hs:
                return b1
            parts = list(urlsplit(url))
            host = parts[1]
            if host == hs:
                return b2
            newhost = []
            for h in host.split('.'):
                newhost.append(h.encode('idna').decode())
                parts[1] = '.'.join(newhost)
                finalUrl = urlunsplit(parts).split(' ')[0]
                host = parse.urlparse(finalUrl).hostname
            if host == hs:
                return b3
            else:
                return False
        ret = []
        for x in range(65536):
            uni = chr(x)
            url = "http://suctf.c{}".format(uni)
            try:
                if getUrl(url):
                    print('\t\\u' + str(hex(x))[2:] + ":" + uni)
                    ret.append(uni)
            except:
                pass
        print('-' * 25)
        return ret

    F = WdF
    Fd = {chr(ord('a') + i): WdF[i] for i in range(len(WdF))}

    s = ""
    dic = {}

    def __init__(self, sx=""):
        self.s = sx
        self.dic = {sx[i]: i for i in range(len(sx))}

    def __getitem__(self, find):
        try:
            return int(self.dic[find])
        except:
            return -1

    @staticmethod
    def compStr(t1='', t2=''):
        shot = min(len(t1), len(t2))
        print('a:', t1[:shot])
        print('b:', t2[:shot])
        res = [[], [], []]
        for i in range(shot):
            a = t1[i]
            b = t2[i]
            if isinstance(a, str): a = ord(a)
            if isinstance(b, str): b = ord(b)
            res[0].append(a - b)
            res[1].append(a + b)
            res[2].append(a ^ b)
        print('a-b:', res[0])
        print('a+b:', res[1])
        print('a^b:', res[2])
        print('- ' * 30)
        return res

    @staticmethod
    def hex2str(txt='', bs=16) -> str:
        t = txt.replace(' ', '').replace('0x', '')
        return CharF.num2str(t, spl=2, bas=bs)

    @staticmethod
    def str2hex(txt='') -> str:
        ret = ''
        for i in txt:
            ret += hex(ord(i))[2:]
        return ret

    @staticmethod
    def Chkstr(s1='', s2=''):
        ml = min(len(s1), len(s2))

        def output(n='', ev='ord(s1[i]) - ord(s2[i])', s1=s1, s2=s2, x=ml):
            print('%15s:' % n, end=' ')
            for i in range(x):
                w = 0xFF & (eval(ev))
                if w < 32:
                    wc = ' '
                else:
                    wc = chr(w)
                print('[%d]%s' % (w, wc), end='\t')
            print()

        print('- ' * 30)
        print('String Check:')
        output('s1-s2')
        output('s1+s2', 'ord(s1[i]) + ord(s2[i])')
        output('s1^s2', 'ord(s1[i]) ^ ord(s2[i])')

        output('s1-rev(s2)', s2=s2[::-1])
        output('s1+rev(s2)', 'ord(s1[i]) + ord(s2[i])', s2=s2[::-1])
        output('s1^rev(s2)', 'ord(s1[i]) ^ ord(s2[i])', s2=s2[::-1])
        print('- ' * 30)

    @staticmethod
    def ReplaceChar(txt="", s="", t="", DorpUndef=False):
        ret = ""
        f = CharF(s)
        for i in txt:
            cn = f[i]
            if 0 <= cn < len(t):
                ret += t[cn]
            elif not DorpUndef:
                ret += i
        return ret;


    @staticmethod
    def CreateReorderdString(tt=""):  # 全排列字符串
        if len(tt) <= 1: return [tt]
        ret = []
        for i in range(len(tt)):
            ts = tt[:i] + tt[i + 1:]
            child = CharF.CreateReorderdString(ts)
            for cstr in child:
                ret.append(tt[i] + cstr)
        return ret


    @staticmethod
    def SplitByLen(t="", l=8, instr=" "):
        if l < 1: return t
        ret = ""
        for i in range(len(t)):
            ret += t[i]
            if i % (l) == l - 1: ret += instr
        while ret.startswith(instr):
            ret = ret[len(instr):]
            while ret.endswith(instr):
                ret = ret[:-len(instr)]
        return ret

    @staticmethod
    def str2num(txt="0", split=' ', bs=16, spl=0):
        txt = txt.lower()
        if spl == 0:
            numl = txt.split(split)
        else:
            numl = CharF.SplitByLen(txt, spl, ' ').split(' ')
        retl = []
        for i in numl:
            try:
                retl.append(int(i, bs))
            except:
                pass
        return retl

    @staticmethod
    def num2str(txt='0', split=' ', bs=16, spl=0, bas=16):
        bas = bs
        nl = CharF.str2num(txt, split, bas, spl)
        ret = ""
        for i in nl: ret += chr(i)
        return ret
    @staticmethod
    def strInf(txt=''):
        d = {}
        for i in txt:
            if i in d:
                d[i] += 1
            else:
                d[i] = 1
        print('Len : ', len(txt))
        print('Chr : ', len(d))
        print('ChrF: ', list(OrderByValue.d2str(d)))
        print('ChrO: ', (sorted(d.keys())))
        return OrderByValue.d2l(d)

    @staticmethod
    def ReplaceAll(s='', l1=[], l2=[]):
        i = min(len(l1), len(l2))
        for j in range(i):
            s = s.replace(l1[j], l2[j])
        return s

    @staticmethod
    def a2s(ina=[], bs=None):
        s = ''
        if len(ina) == 0: return ''
        for i in ina:
            if isinstance(i, str):
                if bs == None:
                    s += i
                else:
                    s += (chr(int(i, bs)))
            elif isinstance(i, int):
                s += chr(i)
            elif isinstance(i, bytes):
                s += str(i, 'utf-8')
            elif isinstance(i, list):
                s += CharF.a2s(i)
        return s

    @staticmethod
    def mask(str='', strh='', strn='', strl=-1, start=0):
        try:
            if len(strn) == 0:
                if strl < 0:
                    return str[str.index(strh, start) + len(strh):]
                else:
                    return str[str.index(strh, start) + len(strh):str.index(strh, start) + len(strh) + strl]
            else:
                str = CharF.mask(str, strh, strl=-1, start=start)
                return str[:str.index(strn)]
        except:
            return str


# 控制台颜色
'''
前景色	背景色	颜色
30	    40	    黑色
31	    41	    红色
32	    42	    绿色
33	    43	    黃色
34	    44	    蓝色
35	    45	    紫红色
36	    46	    青蓝色
37	    47	    白色

显示方式	意义
0	终端默认设置
1	高亮显示
4	使用下划线
5	闪烁
7	反白显示
8	不可见

输出特效格式控制：  
\033[0m  关闭所有属性    
\033[1m   设置高亮度    
\03[4m   下划线    
\033[5m   闪烁    
\033[7m   反显    
\033[8m   消隐    
\033[30m   --   \033[37m   设置前景色    
\033[40m   --   \033[47m   设置背景色  

光标位置等的格式控制：  
\033[nA  光标上移n行    
\03[nB   光标下移n行    
\033[nC   光标右移n行    
\033[nD   光标左移n行    
\033[y;xH设置光标位置    
\033[2J   清屏    
\033[K   清除从光标到行尾的内容    
\033[s   保存光标位置    
\033[u   恢复光标位置    
\033[?25l   隐藏光标    
\33[?25h   显示光标
'''


class cmd_color:
    none = "\033[0m"
    black = "\033[0;30m"
    dark_gray = "\033[1;30m"
    blue = "\033[0;34m"
    light_blue = "\033[1;34m"
    green = "\033[0;32m"
    light_green = "\033[1;32m"
    cyan = "\033[0;36m"
    light_cyan = "\033[1;36m"
    red = "\033[0;31m"
    light_red = "\033[1;31m"
    purple = "\033[0;35m"
    light_purple = "\033[1;35m"
    brown = "\033[0;33m"
    yellow = "\033[1;33m"
    light_gray = "\033[0;37m"
    white = "\033[1;37m"


def printc(s, color=cmd_color.none, end='\n'):
    print(strcolor(s, color), end=end)


def strcolor(s, color=cmd_color.none):
    return color + s + cmd_color.none


def printhex(i, c=cmd_color.none):
    hexs = ''
    if isinstance(i, int):
        hexs = hex(i)[2:]
    elif isinstance(i, str):
        for x in i:
            hexs += hex(ord(x))[2:]
    elif isinstance(i, bytes):
        for x in i:
            hexs += hex(x)[2:]
    print(c + hexs + cmd_color.none)
    return hexs, int(hexs, 16)


def printbin(i, c=cmd_color.none):
    hexs = ''
    if isinstance(i, int):
        hexs = bin(i)[2:]
    elif isinstance(i, str):
        for x in i:
            hexs += bin(ord(x))[2:]
    elif isinstance(i, bytes):
        for x in i:
            hexs += bin(x)[2:]


def printl(s, w=30, c=cmd_color.none):
    print()
    print('- ' * w + c)
    if isinstance(s, list) or isinstance(s, tuple):
        for i in s:
            print(i)
    elif isinstance(s, dict):
        for i in s:
            print(i, '=>', s[i])
    else:
        print(s)
    print(cmd_color.none + '- ' * w)


def printbi(i=1, s='', w=20):
    print()
    f = '%-{0}s|%02d| '.format(w)
    print(f % (s, i), end='')


def print3c(txt='', r=CharF.chra2z('a', 'z'), g=CharF.chra2z('A', 'Z'), lower=True):
    for i in txt:
        if i in r:
            i = strcolor(i, cmd_color.red)
        elif i in g:
            i = strcolor(i, cmd_color.green)
        else:
            i = strcolor(i, cmd_color.none)
        print(i.lower(), end='')
