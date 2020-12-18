from utfc.StrFunc import *
import base91
import base64
import base58
import math

'''---------------------------------------------
    Base全家桶--残次品，跑不通
---------------------------------------------'''


class BaseQ:
    defTable = {
        '16': b'0123456789ABCDEF',
        '32': b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
        '36': b'0123456789abcdefghijklmnopqrstuvwxyz',
        '58': b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',
        '58b': b'rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz',
        '62': b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
        '62b': b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        '64': b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/',
        '85': b'!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstu',
        '85b': b'!#$%&()*+-./0123456789:<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^abcdefghijklmnopqrstuvwxyz{}',
        '85c': b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~',
        '91': b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~"',
        '92': b"!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}",
        '128': b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\xb5\xb6\xb7\xbc\xbd\xbe\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff',
        'r16': b'FEDCBA9876543210',
        'r32': b'765432ZYXWVUTSRQPONMLKJIHGFEDCBA',
        'r36': b'zyxwvutsrqponmlkjihgfedcba9876543210',
        'r58': b'zyxwvutsrqponmkjihgfedcbaZYXWVUTSRQPNMLKJHGFEDCBA987654321',
        'r62': b'zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA9876543210',
        'r62b': b'9876543210ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba',
        'r64': b'/+9876543210zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA',
        'r85': b'utsrqponmlkjihgfedcba`_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)(\'&%$#"!',
        'r85b': b'}{zyxwvutsrqponmlkjihgfedcba^][ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<:9876543210/.-+*)(&%$#!',
        'r85c': b'~}|{`_^@?>=<;-+*)(&%$#!zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA9876543210',
        'r91': b'"~}|{`_^][@?>=<;:/.,+*)(&%$#!9876543210zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA',
        'r92': b"}|{zyxwvutsrqponmlkjihgfedcba_^]\\[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)('&%$#!",
        'r128': b'\xff\xfe\xfd\xfc\xfb\xfa\xf9\xf8\xf7\xf6\xf5\xf4\xf3\xf2\xf1\xef\xee\xed\xec\xeb\xea\xe9\xe8\xe7\xe6\xe5\xe4\xe3\xe2\xe1\xdf\xde\xdd\xdc\xdb\xda\xd9\xd8\xd7\xd6\xd5\xd4\xd3\xd2\xd1\xcf\xce\xcd\xcc\xcb\xca\xc9\xc8\xc7\xc6\xc5\xc4\xc3\xc2\xc1\xbe\xbd\xbc\xb7\xb6\xb5zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA9876543210',

    }

    @staticmethod
    def Dc(txt=''):

        reta = []
        retb = []
        for i in BaseQ.defTable:
            c = BaseQ.decode(txt, i)
            reta.append(bytes(c[0][0], 'utf-8'))
            retb.append(c[1][0])
        return [reta, retb]

    @staticmethod
    def decode(txt='', tab='', base=None):
        if isinstance(tab, bytes):
            tab = tab.encode()
        if base != None and len(tab) < base:
            tab += '=' * (base - len(tab))
        elif base != None and len(tab) > base:
            tab = tab[:base]
        ret = []
        alpha = tab
        if tab not in BaseQ.defTable: tab = 'UserDef'
        if (alpha.lower() in BaseQ.defTable): alpha = str(BaseQ.defTable[alpha.lower()])
        # 码长
        clong = len(alpha)
        pr = 1
        bigint = 0
        rev = txt[::-1]
        for i in rev:
            iv = alpha.find(i)
            if iv < 0: iv = 0
            bigint = bigint + iv * pr
            pr *= clong
        st = str(bin(bigint))[2:]
        st = '0' * (8 - len(st) % 8) + st
        ret = CharF.num2str(st, bs=2, spl=8)
        return [[ret], ['Base:' + tab]]

    @staticmethod
    def DcTW(fn):
        base = [base64.b16decode, base64.b32decode, base58.b58decode, base64.b64decode, base64.b85decode, base91.decode]
        c = ''
        with open(fn, 'r') as f:
            c = f.read()
        BaseQ.DcStrQJT(c)

    @staticmethod
    def DcStrQJT(c=''):
        base = [base64.b16decode, base64.b32decode, base58.b58decode, base64.b64decode, base64.b85decode, base91.decode]
        if 'flag' in c: return
        for i in base:
            try:
                c = i(c).decode()
                print(i.__name__,c)
                continue
            except:
                pass


if __name__ == "__main__":
    print(BaseQ.Dc(''))

    pass
