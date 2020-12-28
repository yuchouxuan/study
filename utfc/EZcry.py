import base64
import binascii as bis
import hashlib
import html
import math
import quopri
import re
import struct
from itertools import permutations
from zlib import crc32
from itertools import cycle
import base91
import base92
import gmpy2
from Crypto.Cipher import PKCS1_OAEP as PKCS1_OAEP
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from bubblepy import BubbleBabble
import pycipher
import base58
import base128
import utfc.UtilFuction as uf
from utfc.ngram_score import ngram_score
from utfc.StrFunc import *

''' 
    - - - - - - - - - - - - - - - - - - - - - -
    W.X.H  2020.01.03
    - - - - - - - - - - - - - - - - - - - - - -

    编码类:     Dc->2Dret
    - - - - - - - - - - - - - - - - - - - - - -
    Html实体    HtmlC
    泡泡码      Bubble
    Unicode     Unic                     Dc/Ec
    Quoted      Quoted                   Dc/Ec
    XXCode      XXCode       ???+        Dc/Ec
    UUCode      UUCode                   Dc/Ec
    URL编码     URLC                     Dc/Ec
    Base码      BaseX                    Dc/Ec
    曼彻斯特    MCST
    - - - - - - - - - - - - - - - - - - - - - -

    密码类：  Dc->2Dret
    - - - - - - - - - - - - - - - - - - - - - -
    幂数      Power
    维吉尼亚  Virginia     
    培根:     Bacon
    曲路:     Curve                    四种方向
    逆序：    Atbash
    凯撒：    Caesar                   128/26
    列位移    CMove        1Dret       Need Key
    摩斯码    MorseOrBin               莫斯+二进制
    栅栏码    Fence
    计算      Maths
    B64隐写   B64H
    替换代码  Excange
    棋盘喵喵  QPM 
    仿射密码  Affine
    
    - - - - - - - - - - - - - - - - - - - - - - 

    需要key的密码 Dc->2Dret
    - - - - - - - - - - - - - - - - - - - - - -
    移位密码        PMove          
    托马斯转轮      TJ_ROOL
    RSA            rsaT
    - - - - - - - - - - - - - - - - - - - - - - 

    辅助类：
    - - - - - - - - - - - - - - - - - - - - - -
    MYB      是时候莽一波了
    过滤器    Filler                   print filler
    字频矩阵  F
    - - - - - - - - - - - - - - - - - - - - - -
'''


def f_JoinAnsList(l1=[], l2=[]):
    ret1 = []
    ret2 = []
    if len(l1) == 0: return l2
    if len(l2) == 0: return l1

    ret1 = l1[0]
    ret2 = l1[1]
    ret1.extend(l2[0])
    ret2.extend(l2[1])
    dl = len(ret1) - len(ret2)
    if dl > 0:
        for i in range(dl):
            ret2.append('')
    elif dl < 0:
        for i in range(-dl):
            ret1.append('')
    return [ret1, ret2]


class MYB:  # 莽一波
    def __init__(self, c='', *args, **kwargs):
        if isinstance(c, list):
            if isinstance(c[0], str):
                c = "".join(c)
            if isinstance(c[0], int):
                c = ''.join([chr(i) for i in c])

        def func_findflag(txt=''):
            return ("flag" in txt.lower()) \
                   or ('ZmxhZ' in txt.lower()) \
                   or ('666c61677b' in txt.replace(' ', '').lower()) \
                   or (
                           '0011011000110110001000000011011001100011001000000011011000110001001000000011011000110111' in txt.replace(
                       ' ', ''))

        p(MYB.go(c), func_findflag)

    @staticmethod
    def go(txt):  # 莽一波
        try:
            m = Bubble.Dc(txt)
        except:
            pass
        try:
            m = f_JoinAnsList(m, Unic.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, Quoted.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, XXCode.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, UUCode.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, URLC.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, BaseX.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, Caesar.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, Curve.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, Fence.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, MorseOrBin.Dc(txt))
        except:
            pass
        # m = f_JoinAnsList(m,PMove.Dc(txt))
        try:
            m = f_JoinAnsList(m, Atbash.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, Bacon.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, Maths.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, B64H.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, HtmlC.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, Power.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, Excange.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, Affine.Dc(txt))
        except:
            pass
        try:
            m = f_JoinAnsList(m, MCST.Dc(txt))
        except:
            pass
        return m


class MCST:
    @staticmethod
    def Dc(txt=''):
        def long_to_bytes(n):
            s = b''
            pack = struct.pack
            while n > 0:
                s = pack('>I', n & 0xffffffff) + s
                n = n >> 32
            for i in range(len(s)):
                if s[i] != b'\000'[0]:
                    break
            else:
                s = b'\000'
                i = 0
            s = s[i:]
            return s

        # 字节逆序
        def byteinvert(str_bin):
            ret = ''
            for i in range(len(str_bin) // 8):
                ret += str_bin[i * 8:i * 8 + 8][::-1]
            return ret

        # 标准曼彻斯特
        def MCST_stand(str_bin):
            ret = ''
            for i in range(len(str_bin) // 2):
                x = str_bin[i * 2:i * 2 + 2]
                if x == '01':
                    ret += '0'
                elif x == '10':
                    ret += '1'

            return ret

        # IEEE规范的曼彻斯特
        def MCST_IEEE(str_bin):
            ret = ''
            for i in range(math.ceil(len(str_bin) / 8)):
                x = str_bin[i * 2:i * 2 + 2]
                if x == '01':
                    ret += '1'
                elif x == '10':
                    ret += '0'
            return ret

        # 差分曼彻斯特
        def MCST_diff(str_bin):
            ret = ''
            for i in range(len(str_bin) // 2 - 1):
                x1 = str_bin[i * 2:i * 2 + 2]
                x2 = str_bin[i * 2 + 2:i * 2 + 4]
                if x1 == x2:
                    ret += '0'
                else:
                    ret += '1'
            return ret

        txt = txt.replace('0x', '')

        try:
            x = int(txt, 16)
        except:
            return []
        str_bin = str(bin(int(txt, 16)))[2:]
        str_bin = '0' * (8 - (len(str_bin) % 8)) + str_bin

        m1 = MCST_IEEE(str_bin)
        m2 = MCST_stand(str_bin)
        m3 = MCST_diff(str_bin)
        ret2 = []
        ret1 = []
        try:
            ret2.append('IEEE曼彻斯特:' + hex(int(m1, 2)))
            ret1.append(CharF.int2str(m1))
        except:
            pass
        try:
            ret2.append('标准曼彻斯特:' + hex(int(m2, 2)))
            ret1.append(CharF.int2str(m2))
        except:
            pass
        try:
            ret2.append('差分曼彻斯特:' + hex(int(m3, 2)))
            ret1.append(CharF.int2str(m3))
        except:
            pass

        try:
            m1 = byteinvert(m1)
            ret2.append('[rev]IEEE曼彻斯特:' + hex(int(m1, 2)))
            ret1.append(CharF.int2str(m1))
        except:
            pass
        try:
            m2 = byteinvert(m2)
            ret2.append('[rev]标准曼彻斯特:' + hex(int(m2, 2)))
            ret1.append(CharF.int2str(m2))
        except:
            pass
        try:
            m3 = byteinvert(m3)
            ret2.append('[rev]差分曼彻斯特:' + hex(int(m3, 2)))
            ret1.append(CharF.int2str(m3))
        except:
            pass

        return [ret1, ret2]


class Affine:
    # 加密
    @staticmethod
    def Dckk(enc='', k1=0, k2=0) -> str:
        ret = [[], []]
        for m in range(1, 26):
            try:
                flag = ''
                for i in enc:
                    if i.isalpha():
                        if i.islower():
                            x = 97
                        if i.isupper():
                            x = ord('A')
                        a = ord(i) - x
                        inv = gmpy2.invert(k1, m)
                        flag += chr(((a - k2) * inv) % m + x)
                    else:
                        flag += i;
                ret[0].append(flag)
                ret[1].append("Affin:%d,%d,%d" % (m, k1, k2))
            except:
                pass
        return ret

    @staticmethod
    def Ec(m, c, a, b):
        for i in range(len(m)):
            # 加密成相应的大写字母
            c.append(chr(((ord(m[i]) - 97) * a + b) % 26 + 65))
        d = ''.join(c)
        print(d)

    # 解密
    @staticmethod
    def Ecs(c, k, b):
        mw = []
        for i in range(len(c)):
            if (c[i].isalpha()):
                tem = ord(c[i]) - 65 - b
                if tem < 0:
                    tem += 26
                mw.append(chr((k * tem) % 26 + 97))
            else:
                mw.append(c[i])
        return [[''.join(mw)], ["Affine:" + str(k) + ',' + str(b)]]

    @staticmethod
    def format(m="", c=""):
        cout = ""
        ip = 0
        for i in m:
            if not i.isalpha():
                cout += i
            elif i.isupper():
                cout += c[ip].upper()
                ip += 1
            else:
                cout += c[ip]
                ip += 1
        return cout

    @staticmethod
    def Dc(cin='', onlychar=True):
        c = ""
        if onlychar:
            for i in cin.lower():
                if i.isalpha():
                    c += i
        else:
            c = cin
        m = [[], []]
        la = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        lb = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
              14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
        for i in range(0, 12):
            for j in range(0, 26):
                c1 = Affine.Dckk(c, la[i], lb[j])
                if onlychar:
                    for x in range(len(c1[0])):
                        c1[0][x] = Affine.format(cin, c1[0][x])
                m = f_JoinAnsList(m, c1)
                c2 = Affine.Ecs(c, la[i], lb[j])
                if onlychar:
                    for x in range(len(c2[0])):
                        c2[0][x] = Affine.format(cin, c2[0][x])
                m = f_JoinAnsList(m, c2)
        return m


class QPM:
    list1 = [
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i/j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
         'x', 'y', 'z'],
        ['a', 'b', 'c/k', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
         'x', 'y', 'z'],
        'abcdefghijklmnopqrstuvwxyz',
        'btalpdhozkqfvsngjcuxmrewy',
        'cohmtrginuabjpvyekqwdflsx']
    adf = 'adfgvx'

    @staticmethod
    def Dc(txt='', addqp='', r='12345'):
        l = QPM.list1
        txt = CharF.ReplaceChar(txt, r, '01234')
        if len(addqp) >= 25: l.append(addqp)
        r1 = []
        r2 = []
        for i in l:
            if len(txt) % 2 == 1: txt += '0'
            r = ''
            for p in range(0, len(txt), 2):
                x = int(txt[p])
                y = int(txt[p + 1])
                r += i[x * 5 + y]

            r2.append('QPM:' + str(i)[0:13] + '.....')
            r1.append(r)
        for i in l:
            if len(txt) % 2 == 1: txt += '0'
            r = ''
            for p in range(0, len(txt), 2):
                y = int(txt[p])
                x = int(txt[p + 1])
                r += i[x * 5 + y]
            r2.append('QPM_R:' + str(i)[0:13] + '.....')
            r1.append(r)
        return [r1, r2]


class PlayfairError(Exception):
    def __init__(self, message):
        print
        message


class Playfair:
    @staticmethod
    def Ec(txt='', key=''):
        px = Playfair()
        px.setPassword(key)
        return px.encrypt(txt)

    @staticmethod
    def Dc(txt='', key=''):
        px = Playfair()
        px.setPassword(key)
        return [[px.decrypt(txt)], ['PlayFair']]

    def __init__(self, omissionRule=0, doublePadding='X', endPadding='X'):
        omissionRules = [
            'Merge J into I',
            'Omit Q',
            'Merge I into J',
        ]
        if omissionRule >= 0 and omissionRule < len(omissionRules):
            self.omissionRule = omissionRule
        else:
            raise PlayfairError('Possible omission rule values are between 0 and ' + (len(omissionRules) - 1) + '.')

        # start with a blank password
        self.grid = self.generateGrid('')

        # make sure the input for the double padding character is valid
        if len(doublePadding) != 1:
            raise PlayfairError('The double padding must be a single character.')
        elif not self.isAlphabet(doublePadding):
            raise PlayfairError('The double padding must be a letter of the alphabet.')
        elif doublePadding not in self.grid:
            raise PlayfairError('The double padding character must not be omitted by the omission rule.')
        else:
            self.doublePadding = doublePadding.upper()

        # make sure the input for the end padding character is valid
        if len(endPadding) != 1:
            raise PlayfairError('The end padding must be a single character.')
        elif not self.isAlphabet(endPadding):
            raise PlayfairError('The end padding must be a letter of the alphabet.')
        elif endPadding not in self.grid:
            raise PlayfairError('The end padding character must not be omitted by the omission rule.')
        else:
            self.endPadding = endPadding.upper()

    # returns None if the letter should be discarded, else returns the converted letter
    def convertLetter(self, letter):
        if self.omissionRule == 0:
            if letter == 'J':
                letter = 'I'
            return letter
        elif self.omissionRule == 1:
            if letter == 'Q':
                letter = None
            return letter
        elif self.omissionRule == 2:
            if letter == 'I':
                letter = 'J'
            return letter
        else:
            raise PlayfairError('The omission rule provided has not been configured properly.')

    # returns the alphabet used by the cipher (takes into account the omission rule)
    def getAlphabet(self):
        fullAlphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        alphabet = ''

        for letter in fullAlphabet:
            letter = self.convertLetter(letter)
            if letter is not None and letter not in alphabet:
                alphabet += letter

        return alphabet

    # generates the 25 character grid based on the omission rule and the given password
    def generateGrid(self, password):
        grid = ''
        alphabet = self.getAlphabet()

        for letter in password:
            if letter not in grid and letter in alphabet:
                grid += letter

        for letter in alphabet:
            if letter not in grid:
                grid += letter

        return grid

    # splits the text input into digraphs
    def generateDigraphs(self, input):
        input = self.toAlphabet(input).upper()
        inputFixed = ''

        for i in range(len(input)):
            letter = self.convertLetter(input[i])
            if letter is not None:
                inputFixed += letter

        digraphs = []

        counter = 0
        while counter < len(inputFixed):
            digraph = ''
            if counter + 1 == len(inputFixed):  # we have reached the end of the inputFixed
                digraph = inputFixed[counter] + self.endPadding
                digraphs.append(digraph)
                break
            elif inputFixed[counter] != inputFixed[counter + 1]:  # we just need to create a normal digraph
                digraph = inputFixed[counter] + inputFixed[counter + 1]
                digraphs.append(digraph)
                counter += 2
            else:  # we have a double letter digraph, so we add the double padding
                digraph = inputFixed[counter] + self.doublePadding
                digraphs.append(digraph)
                counter += 1

        return digraphs

    # encrypts a digraph using the defined grid
    def encryptDigraph(self, input):
        if len(input) != 2:
            raise PlayfairError('The digraph that is going to be encrypted must be exactly 2 characters long.')
        elif not self.isUpper(input):
            raise PlayfairError(
                'The digraph that is going to be encrypted must contain only uppercase letters of the alphabet.')

        firstLetter = input[0]
        secondLetter = input[1]

        firstLetterPosition = self.grid.find(firstLetter)
        secondLetterPosition = self.grid.find(secondLetter)

        firstLetterCoordinates = (firstLetterPosition % 5, firstLetterPosition / 5)
        secondLetterCoordinates = (secondLetterPosition % 5, secondLetterPosition / 5)

        if firstLetterCoordinates[0] == secondLetterCoordinates[0]:  # letters are in the same column
            firstEncrypted = self.grid[(((firstLetterCoordinates[1] + 1) % 5) * 5) + firstLetterCoordinates[0]]
            secondEncrypted = self.grid[(((secondLetterCoordinates[1] + 1) % 5) * 5) + secondLetterCoordinates[0]]
        elif firstLetterCoordinates[1] == secondLetterCoordinates[1]:  # letters are in the same row
            firstEncrypted = self.grid[(firstLetterCoordinates[1] * 5) + ((firstLetterCoordinates[0] + 1) % 5)]
            secondEncrypted = self.grid[(secondLetterCoordinates[1] * 5) + ((secondLetterCoordinates[0] + 1) % 5)]
        else:  # letters are not in the same row or column, i.e. they form a rectangle
            firstEncrypted = self.grid[(firstLetterCoordinates[1] * 5) + secondLetterCoordinates[0]]
            secondEncrypted = self.grid[(secondLetterCoordinates[1] * 5) + firstLetterCoordinates[0]]

        return firstEncrypted + secondEncrypted

    # decrypts a digraph using the defined grid
    def decryptDigraph(self, input):
        if len(input) != 2:
            raise PlayfairError('The digraph that is going to be encrypted must be exactly 2 characters long.')
        elif not self.isUpper(input):
            raise PlayfairError(
                'The digraph that is going to be encrypted must contain only uppercase letters of the alphabet.')

        firstEncrypted = input[0]
        secondEncrypted = input[1]

        firstEncryptedPosition = self.grid.find(firstEncrypted)
        secondEncryptedPosition = self.grid.find(secondEncrypted)

        firstEncryptedCoordinates = (firstEncryptedPosition % 5, firstEncryptedPosition / 5)
        secondEncryptedCoordinates = (secondEncryptedPosition % 5, secondEncryptedPosition / 5)

        if firstEncryptedCoordinates[0] == secondEncryptedCoordinates[0]:  # letters are in the same column
            firstLetter = self.grid[(((firstEncryptedCoordinates[1] - 1) % 5) * 5) + firstEncryptedCoordinates[0]]
            secondLetter = self.grid[(((secondEncryptedCoordinates[1] - 1) % 5) * 5) + secondEncryptedCoordinates[0]]
        elif firstEncryptedCoordinates[1] == secondEncryptedCoordinates[1]:  # letters are in the same row
            firstLetter = self.grid[(firstEncryptedCoordinates[1] * 5) + ((firstEncryptedCoordinates[0] - 1) % 5)]
            secondLetter = self.grid[(secondEncryptedCoordinates[1] * 5) + ((secondEncryptedCoordinates[0] - 1) % 5)]
        else:  # letters are not in the same row or column, i.e. they form a rectangle
            firstLetter = self.grid[(firstEncryptedCoordinates[1] * 5) + secondEncryptedCoordinates[0]]
            secondLetter = self.grid[(secondEncryptedCoordinates[1] * 5) + firstEncryptedCoordinates[0]]

        return firstLetter + secondLetter

    # encrypts text input
    def encrypt(self, input):
        digraphs = self.generateDigraphs(input)
        encryptedDigraphs = []

        for digraph in digraphs:
            encryptedDigraphs.append(self.encryptDigraph(digraph))

        return ''.join(encryptedDigraphs)

    # decrypts text input
    def decrypt(self, input):
        digraphs = self.generateDigraphs(input)

        decryptedDigraphs = []

        for digraph in digraphs:
            decryptedDigraphs.append(self.decryptDigraph(digraph))

        return ''.join(decryptedDigraphs)

    # sets the password for upcoming encryptions and decryptions
    def setPassword(self, password):
        password = self.toAlphabet(password).upper()

        self.grid = self.generateGrid(password)

    # strips out all non-alphabetical characters from the input
    def toAlphabet(self, input):
        return re.sub('[^A-Za-z]', '', input)

    # tests whether the string only contains alphabetical characters
    def isAlphabet(self, input):
        if re.search('[^A-Za-z]', input):
            return False
        return True

    # tests whether the string only contains uppercase alphabetical characters
    def isUpper(self, input):
        if re.search('[^A-Z]', input):
            return False
        return True


class HtmlC:
    @staticmethod
    def Ec(txt=''):
        return html.escape(txt)

    @staticmethod
    def Dc(txt=''):
        return [[(html.unescape(txt))], ['HTML']]


class Maths:  # 各种乱七八糟的计算 异或啥的

    @staticmethod
    def Dc(txt, ds='utf-8'):

        str = ""
        ret = [[], []]
        for c in range(256):
            # 异或（0-255）
            str = ""
            for i in txt:
                str += chr(ord(i) ^ c)
            ret[0].append(str)
            ret[1].append('Xor:%d' % c)

            # +x（0-255）
            str = ""
            for i in txt:
                str += chr(ord(i) + c)
            ret[0].append(str)
            ret[1].append('+%d' % c)

            # -x
            str = ""
            for i in txt:
                ch = ord(i) - c
                if ch < 0: ch += 255
                str += chr(ch)

            ret[0].append(str)
            ret[1].append('-%d' % c)

            # x-
            str = ""
            for i in txt:
                ch = c - ord(i)
                if ch < 0: ch += 255
                str += chr(ch)
            ret[0].append(str)
            ret[1].append('%d-' % c)
        return ret


class Bubble:
    @staticmethod
    def Dc(txt, ds='utf-8'):
        Str = BubbleBabble()
        try:
            return [[str(Str.decode(txt), ds)], ['Bubble']]
        except:
            return []

    @staticmethod
    def Ec(txt, ds='utf-8'):
        Str = BubbleBabble()
        return str(Str.encode(txt), ds)


class Unic:
    @staticmethod
    def Ec(txt="tst", ds='utf-8'):
        f = txt.encode(ds)
        ret = ""
        for i in f:
            ret += "\\u%04x" % i
        return ret

    @staticmethod
    def Dc(txt, ds='utf-8'):
        txt = txt.replace('%u', '\\u')
        try:
            rets = [txt.encode('utf-8').decode(ds)]
            retc = [ds]
            rets.append(txt.encode('utf-8').decode('unicode_escape'))
            retc.append('unicode_escape')
        except:
            pass
        return [rets, retc]


class XXCode:  # code可定制，
    @staticmethod
    def Ec(txt="tst", code='+-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', ds='utf-8'):
        stx = UUCode.Ec(txt, ds)
        stret = "";
        for i in range(len(stx)):
            stret += code[ord(stx[i]) - 32]
        return stret[:-1]

    @staticmethod
    def Dc(txt, code='+-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', ds='utf-8'):
        cf = CharF(code)
        ut = ""
        for i in range(len(txt)):
            chP = cf[txt[i]]
            if chP >= 0: ut += chr(chP + 32)
        if len(ut) != len(txt): return []
        try:
            return [str(bis.a2b_uu(ut), ds), 'XXCode']
        except:
            return []


class UUCode:
    @staticmethod
    def Ec(txt="tst", ds='utf-8'):
        try:
            return str(bis.b2a_uu(txt.encode(ds)), ds)
        except:
            return ""

    @staticmethod
    def Dc(txt, ds='utf-8'):
        try:
            return [str(bis.a2b_uu(txt), ds), 'UUCode']
        except:
            return []


class URLC:
    @staticmethod
    def Ec(txt):
        rtx = ''
        for i in txt:
            if ord(i) < 128:
                rtx += '%%%X' % ord(i)
            else:
                rtx += parse.quote(i)
        return rtx

    @staticmethod
    def Dc(txt):
        return [parse.unquote(txt), 'URLCode']


class Quoted:
    @staticmethod
    def Dc(txt, ds='utf-8'):
        return [quopri.decodestring(txt).decode(ds), ' Quoted']

    @staticmethod
    def Ec(txt, ds='utf-8'):
        return str(quopri.encodestring(txt.encode(ds)), ds)


class BaseX:
    @staticmethod
    def DC_r(sti='', r=0, sts='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'):
        l = ""
        for i in sti:
            l += sts[(sts.index(i) - r) % len(sts)]
        if len(l) % 8 != 0:
            l = l + "=" * (4 - (len(l) % 4))
        return BaseX.Dc(l)

    @staticmethod
    def Ec(strin, b=64, ds='utf-8'):  # 16/32/64/85； 86=A85
        txt = strin.encode(ds)
        t = ''
        if (b == 16):
            t = base64.b16encode(txt)
        elif (b == 32):
            t = base64.b32encode(txt)
        elif (b == 58):
            t = base58.b58encode(txt)
        elif (b == 64):
            t = base64.b64encode(txt)
        elif (b == 85):
            t = base64.b85encode(txt)
        elif (b == 86):
            t = base64.a85encode(txt)
        elif (b == 91):
            t = base91.encode(txt)
        elif (b == 92):
            t = base92.b92encode(txt)
        elif (b == 128):
            b128 = base128.base128(chars=base128.base128.defaultchars, chunksize=7)
            t = b128.encode(txt)
        return str(t, ds)

    @staticmethod
    def Dc(txt, ds='utf-8'):
        ret = [[], []]
        try:
            t = str(base64.b16decode(txt))
            try:
                t += '\n' + str(base64.b16decode(txt), ds)
            except:
                pass
            ret[0].append(t)
            ret[1].append('Base16')
        except:
            pass

        try:
            t = str(base64.b32decode(txt))
            try:
                t += '\n' + str(base64.b32decode(txt), ds)
            except:
                pass
            ret[0].append(t)
            ret[1].append('Base32')
        except:
            pass

        try:
            t = str(base58.b58decode(txt))
            try:
                t += '\n' + str(base58.b58decode(txt), ds)
            except:
                pass
            ret[0].append(t)
            ret[1].append('Base58')
        except:
            pass

        try:
            t = str(base64.b64decode(txt))
            try:
                t += '\n' + str(base64.b64decode(txt), ds)
            except:
                pass
            ret[0].append(t)
            ret[1].append('Base64')
        except:
            pass

        try:
            t = str(base64.a85decode(txt))
            try:
                t += '\n' + str(base64.a85decode(txt), ds)
            except:
                pass
            ret[0].append(t)
            ret[1].append('Base85A')
        except:
            pass

        try:
            t = str(base64.b85decode(txt))
            try:
                t += '\n' + str(base64.b85decode(txt), ds)
            except:
                pass
            ret[0].append(t)
            ret[1].append('Base85')
        except:
            pass

        try:
            t = str(base91.decode(txt))
            try:
                t += '\n' + str(base91.decode(txt), ds)
            except:
                pass
            ret[0].append(t)
            ret[1].append('Base91')
        except:
            pass

        try:
            t = str(base92.b92decode(txt))
            try:
                t += '\n' + str(base92.b92decode(txt), ds)
            except:
                pass
            ret[0].append(t)
            ret[1].append('Base92')
        except:
            pass

        try:
            b128 = base128.base128(chars=base128.base128.defaultchars, chunksize=7)
            t = b128.decode(txt)
            t = str(b128.decode(txt))
            try:
                t += '\n' + str(base128.base128.decode(txt), ds)
            except:
                pass
            ret[0].append(t)
            ret[1].append('Base128')
        except:
            pass

        return ret


class Virginia:  # 维吉尼亚
    cipher_alpha = ""
    keyset = []
    keygus = []
    maxguess = 3

    def c_alpha(self, cipher):  # 去掉非字母后的密文
        cipher_alpha = ''
        for i in range(len(cipher)):
            if (cipher[i].isalpha()):
                cipher_alpha += cipher[i]
        return cipher_alpha

    # 字母频率矩阵
    F = [
        0.0651738, 0.0124248, 0.0217339, 0.0349835, 0.1041442, 0.0197881,
        0.0158610, 0.0492888, 0.0558094, 0.0009033, 0.0050529, 0.0331490,
        0.0202124, 0.0564513, 0.0596302, 0.0137645, 0.0008606, 0.0497563,
        0.0515760, 0.0729357, 0.0225134, 0.0082903, 0.0171272, 0.0013692,
        0.0145984, 0.0007836]

    # 计算cipher的重合指数
    def count_CI(self, cipher):
        N = [0.0 for i in range(26)]
        cipher = self.c_alpha(cipher)
        L = len(cipher)
        if cipher == '':
            return 0
        else:
            for i in range(L):  # 计算所有字母的频数，存在数组N当中
                test = ord(cipher[i])
                if (test >= ord('a') and test <= ord('z')):
                    N[test - ord('a')] += 1
                elif (test >= ord('A') and test <= ord('Z')):
                    N[test - ord('A')] += 1
        CI_1 = 0
        for i in range(26):
            CI_1 += ((N[i] / L) * ((N[i] - 1) / (L)))
        return CI_1

    # 计算秘钥长度为 key_len 的重合指数
    def count_key_len_CI(self, cipher, key_len):
        un_cip = ['' for i in range(key_len)]  # un_cip 是分组
        aver_CI = 0.0
        count = 0
        for i in range(len(self.cipher_alpha)):
            z = i % key_len
            un_cip[z] += self.cipher_alpha[i]
        for i in range(key_len):
            un_cip[i] = self.count_CI(un_cip[i])
            aver_CI += un_cip[i]
        aver_CI = aver_CI / len(un_cip)
        return aver_CI

    ## 找出最可能的前十个秘钥长度
    def pre_10(self, cipher):
        M = [(1, self.count_CI(cipher))] + [(0, 0.0) for i in range(49)]
        for i in range(2, 50):
            M[i] = (i, abs(0.065 - self.count_key_len_CI(cipher, i)))
        M = sorted(M, key=lambda x: x[1])  # 按照数组第二个元素排序
        for i in range(1, 10):
            print(M[i])

    # 猜测单个秘钥得到的重合指数
    def count_CI2(self, cipher, n):  # n 代表我们猜测的秘钥，也即偏移量
        N = [0.0 for i in range(26)]
        cipher = self.c_alpha(cipher)
        L = len(cipher)
        for i in range(L):  # 计算所有字母的频数，存在数组N当中
            if (cipher[i].islower()):
                N[(ord(cipher[i]) - ord('a') - n) % 26] += 1
            else:
                N[(ord(cipher[i]) - ord('A') - n) % 26] += 1
        CI_2 = 0
        for i in range(26):
            CI_2 += ((N[i] / L) * self.F[i])
        return CI_2

    def one_key(self, cipher, key_len):
        ret = []
        un_cip = ['' for i in range(key_len)]
        self.cipher_alpha = self.c_alpha(cipher)
        for i in range(len(self.cipher_alpha)):  # 完成分组工作
            z = i % key_len
            un_cip[z] += self.cipher_alpha[i]
        for i in range(key_len):
            ret.append(self.pre_5_key(un_cip[i]))  ####这里应该将5个分组的秘钥猜测全部打印出来
        return ret;

    ## 找出前5个最可能的单个秘钥
    def pre_5_key(self, cipher):
        M = [(0, 0.0) for i in range(26)]
        for i in range(26):
            M[i] = (chr(ord('a') + i), abs(0.065 - self.count_CI2(cipher, i)))
        M = sorted(M, key=lambda x: x[1])  # 按照数组第二个元素排序
        return M;

    @staticmethod
    def Decrypto(txt: 'str', key: 'str'):
        a = Virginia()
        return a.decrypto(txt, key)

    def decrypto(self, miwen, key):
        mingwen = [0] * (len(miwen))
        count = 0
        for i in range(len(miwen)):
            if (miwen[i].isalpha()):
                if (miwen[i].isupper()):
                    offset1 = ord(key[(i - count) % len(key)]) - ord('a')
                    mingwen[i] = chr(((ord(miwen[i]) + ord('A')) - offset1) % 26 + ord('A'))
                else:
                    offset2 = ord(key[(i - count) % len(key)]) - ord('a')
                    mingwen[i] = chr(((ord(miwen[i]) - ord('a')) - offset2) % 26 + ord('a'))
            else:
                mingwen[i] = miwen[i]
                count = count + 1
        return mingwen

    def createKeySet(self, hafk=""):
        pos = len(hafk)
        ret = []
        if (pos >= len(self.keyset)): return [hafk]
        for i in range(self.maxguess):
            newhk = hafk + self.keyset[pos][i][0]
            ret.extend(self.createKeySet(newhk))
        return ret

    @staticmethod
    def Dc(txt, ks=3):
        vg = Virginia()
        vg.maxguess = ks
        vg.cipher_alpha = vg.c_alpha(txt)

        vg.pre_10(txt)
        key_len = int(input("秘钥可能的位数："))
        vg.keyset = vg.one_key(txt, key_len)
        cnt = 1
        for i in vg.keyset:
            print("\nPos%2d: " % cnt, end="")
            cnt += 1
            for x in i:
                print("%s, " % x[0], end="")
        vg.keyset = vg.createKeySet()
        ret = []
        for key in vg.keyset:
            t = "".join(vg.decrypto(txt, key))
            ret.append(t)
        return [ret, vg.keyset]

    @staticmethod
    def Dckeyf(fn='', key='Vigenere', NoChar=True):
        txt = open(fn, 'r').read()
        Virginia.Dckey(txt, key, NoChar)

    @staticmethod
    def Dckey(txt='', key='Vigenere', NoChar=True):  # 最后一位表示非字符元素是否占用key序列
        ret = ''
        index = 0
        key = key.upper()
        kl = cycle([ord(keychar) - ord('A') for keychar in key])
        for i in txt:
            if i.isalpha():

                if i.isupper():
                    x = (ord(i) - ord("A") - next(kl)) % 26
                    ret += chr(x + ord("A"))
                if i.islower():
                    x = (ord(i) - ord("a") - next(kl)) % 26
                    ret += chr(x + ord("a"))
            else:
                if not NoChar: next(kl)
                ret += i
        print(ret)
        return ret


class Caesar:  # 凯撒密码
    @staticmethod
    # 128 包含非字母 ，返回双列表, ret0为字符串列表，re1位asc值列表
    def Dc128(txt, AllOut=False):
        ret0 = []
        ret1 = []
        for k in range(255):
            s = ""
            m = []
            for i in txt:
                chrx = (ord(i) + k) % 255
                m.append(chrx)
                if i == " ":
                    s += ' '
                elif chrx >= 30 or AllOut == True:
                    s += chr(chrx)
            ret0.append('CK:%3d| ' % k + s)
            ret1.append(m)
        return [ret0, ret1];

    @staticmethod
    def change(c, i):
        num = ord(c)
        if num >= 97 and num <= 122:
            num = 97 + ((num - 97) + i) % 26
        else:
            if num >= 65 and num <= 90:
                num = 65 + ((num - 65) + i) % 26
        return chr(num)

    @staticmethod
    def jm(string, i):
        string_new = ''
        for s in string:
            string_new += Caesar.change(s, i)
        return string_new

    @staticmethod
    def DCAlpha(string):
        ret = []
        ret2 = []
        for i in range(25):
            i += 1
            ret.append(Caesar.jm(string, i))
            ret2.append('Caesar:%d' % i)
        return [ret, ret2]

    @staticmethod
    def Dc(string):
        return f_JoinAnsList(Caesar.DCAlpha(string), Caesar.Dc128(string))


class Atbash:  # 逆序码 a-z =>z-a
    @staticmethod
    def Dc(txt):
        ret = [i for i in txt]
        for i in range(len(ret)):
            num = ord(ret[i])
            if num >= 97 and num <= 122:
                ret[i] = chr(219 - num)
            else:
                if num >= 65 and num < 90: ret[i] = chr(155 - num)
        return [["".join(ret)], ['Atbash']]


class CMove:  # 列位移
    @staticmethod
    def Dc(txti, key):
        txt = str(txti).replace(" ", "")
        l = len(key)
        h = math.ceil(len(txt) / l)
        indx = [a for a in key]
        indx.sort();
        ordx = {key[x]: x for x in range(l)}
        box = [" "] * h * l
        cont = 0
        for tl in indx:
            for th in range(h):
                box[th * l + ordx[tl]] = txt[cont]
                cont += 1
        return ["".join(box)]


class Curve:  # 曲路密码
    @staticmethod
    def _ql(txt, h, l=0):
        t = str(txt).replace(" ", "");
        if h == 0: return;
        if (l == 0): l = int(t.__len__() / h);
        box = [""] * h * l
        desc = True
        cont = 0
        for lx in range(l):
            thl = l - lx - 1
            for hx in range(h):
                thh = hx
                if (desc): thh = h - hx - 1
                if (cont < t.__len__()): box[(thh) * l + thl] = t[cont]
                cont += 1
            desc = not desc
        return box

    @staticmethod
    def _ql2(txt, h, l=0):
        t = str(txt).replace(" ", "");
        if h == 0: return;
        if (l == 0): l = int(t.__len__() / h);
        box = [""] * h * l
        desc = False
        cont = 0
        for lx in range(l):
            thl = l - lx - 1
            for hx in range(h):
                thh = hx
                if (desc): thh = h - hx - 1
                if (cont < t.__len__()): box[(thh) * l + thl] = t[cont]
                cont += 1
            desc = not desc
        return box

    @staticmethod
    def _ql3(txt, h, l=0):
        t = str(txt).replace(" ", "");
        if h == 0: return;
        if (l == 0): l = int(t.__len__() / h);
        box = [""] * h * l
        desc = True
        cont = 0
        for lx in range(l):
            thl = lx
            for hx in range(h):
                thh = hx
                if (desc): thh = h - hx - 1
                if (cont < t.__len__()): box[(thh) * l + thl] = t[cont]
                cont += 1
            desc = not desc
        return box

    @staticmethod
    def _ql4(txt, h, l=0):
        t = str(txt).replace(" ", "");
        if h == 0: return;
        if (l == 0): l = int(t.__len__() / h);
        box = [""] * h * l
        desc = False
        cont = 0
        for lx in range(l):
            thl = lx
            for hx in range(h):
                thh = hx
                if (desc): thh = h - hx - 1
                if (cont < t.__len__()): box[(thh) * l + thl] = t[cont]
                cont += 1
            desc = not desc
        return box

    @staticmethod
    def ysfj(i):
        ret = []
        for ix in range(i - 2):
            if (i % (2 + ix) == 0): ret.append(2 + ix)
        return ret

    @staticmethod
    def Dc(txt):
        ret = []
        ret2 = []
        t = str(txt).replace(" ", "");
        leng = t.__len__();
        for i in Curve.ysfj(leng):
            ret.append("".join(Curve._ql(t, i)))
            ret.append("".join(Curve._ql2(t, i)))
            ret.append("".join(Curve._ql3(t, i)))
            ret.append("".join(Curve._ql4(t, i)))
            ret2 = ['Curve', 'Curve', 'Curve', 'Curve', ]
        return [ret, ret2]


class Bacon:  # 培根码
    @staticmethod
    def Dc(ce=''):
        dc = {}
        for i in ce:
            if i in dc:
                dc[i] = dc[i] + 1
            else:
                dc[i] = 1
        ax = sorted(dc.items(), key=lambda x: -x[1])
        if (len(ax) < 2): return []
        a = ax[0][0]
        b = ax[1][0]
        s = ['', '']

        for x in ce:
            if x == a:
                s[0] += 'a'
                s[1] += 'b'
            if x == b:
                s[0] += 'b'
                s[1] += 'a'
        return f_JoinAnsList(Bacon.Dcx(s[0]), Bacon.Dcx(s[1]))

    @staticmethod
    def Dcx(string=''):

        cipher = {
            'aaaaa': 'a', 'aaaab': 'b', 'aaaba': 'c', 'aaabb': 'd', 'aabaa': 'e',
            'aabab': 'f', 'aabba': 'g', 'aabbb': 'h', 'abaaa': 'i', 'abaab': 'j',
            'ababa': 'k', 'ababb': 'l', 'abbaa': 'm', 'abbab': 'n', 'abbba': 'o',
            'abbbb': 'p', 'baaaa': 'q', 'baaab': 'r', 'baaba': 's', 'baabb': 't',
            'babaa': 'u', 'babab': 'v', 'babba': 'w', 'babbb': 'x', 'bbaaa': 'y',
            'bbaab': 'z'}
        lists = []
        # 分割，五个一组
        s = CharF.SplitByLen(string.lower(), 5)
        lists = s.split(' ')
        strx = ""
        for i in range(0, len(lists)):
            bs = lists[i]
            if bs in cipher: strx += cipher[bs]
        return [[strx], ['Bacon']]


class PMove:  # 移位密码
    def perm(self, l):
        if (len(l) <= 1):
            return [l]
        r = []
        for i in range(len(l)):
            s = l[:i] + l[i + 1:]
            p = self.perm(s)
            for x in p:
                r.append(l[i:i + 1] + x)
        return r

    def yw_t(self, txt, key=""):
        s = ""
        for i in range(0, len(txt), len(key)):
            r = txt[i:i + (len(key))]
            temp = [''] * len(key)
            rgk = len(key)
            if rgk > len(r):
                rgk = len(r)
            for j in range(rgk):
                temp[int(key[j]) - 1] = r[j]
            s += "".join(temp)
        return s

    def yw(self, txt, keyl_in):
        keyset = [];
        keyseed = ""
        for i in range(1, keyl_in + 1):
            keyseed += "%d" % i
        keyset = self.perm(keyseed)
        retL = []
        for keytry in keyset:
            retL.append(self.yw_t(txt, keytry))
        return [retL, keyset];

    @staticmethod
    def Dc(txt, keyl_in=0):
        pm = PMove()
        keyls = []
        if keyl_in != 0:
            keyls.append(keyl_in)
        else:
            keyls.extend(uf.MathCump.prime(len(txt)))
        ret = [[], []]
        for kl in keyls:
            r = pm.yw(txt, kl)
            ret[0].extend(r[0])
            ret[1].extend(r[1])
        return ret


class MorseOrBin:  # 莫尔斯码
    dictMos = {'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
               '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
               '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
               '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
               '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
               '--..': 'Z', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
               '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
               '-----': '0', '..--..': '?', '-..-.': '/', '-.--.-': '()', '-....-': '-',
               '.-.-.-': '.', '--..--': ',', '.--.-.': '@', '---...': ':', '-.-.-.': ':',
               '-...-': '=', '.----.': "'", '-.-.--': '!', '..--.-': '_', '.-..-.': '"',
               '-.--.': '(', '----.--': '{', '-----.-': '}'}

    @staticmethod
    def Dc(txt=""):
        ret = []
        Dcod = {}
        dcs = []
        dcsB = []
        for i in txt:
            if i in Dcod:
                Dcod[i] += 1
            else:
                Dcod[i] = 0
        codsec = sorted(Dcod, key=Dcod.__getitem__)
        if len(codsec) == 0:
            return []
        elif len(codsec) == 1:
            codsec.append(chr(ord(codsec[0]) + 1))
            codsec.append(chr(ord(codsec[0]) + 1))
        elif len(codsec) == 2:
            for i in range(32, 128):
                if i != ord(codsec[0]) and i != ord(codsec[1]):
                    codsec.append(chr(i))
                    break;
        for strx in CharF.CreateReorderdString(codsec[0] + codsec[1] + codsec[2]):
            # ?=>0 , ?=>1,?=> | 
            statStr = CharF.ReplaceChar(txt, strx, '|.-', True)
            tempStr = ""
            tempBin = ""
            for t in statStr.split('|'):
                if t in MorseOrBin.dictMos: tempStr += MorseOrBin.dictMos[t]
                tmpNum = 0;
                for ix in range(len(t)):
                    tmpNum <<= 1
                    if t[ix] == '.':
                        tmpNum += 1
                try:
                    tempBin += chr(tmpNum)
                except:
                    pass
            if len(tempStr) > 0:
                dcs.append(tempStr)
            if len(tempBin) > 0:
                dcsB.append(tempBin)
        # 甩掉有分隔符，直接转二进制
        s = CharF.str2num(CharF.ReplaceChar(txt, codsec[0] + codsec[1], '01', True), spl=8, bs=2)
        dcs.append('BIN1' + ''.join([chr(i) for i in s]))
        s = CharF.str2num(CharF.ReplaceChar(txt, codsec[0] + codsec[1], '10', True), spl=8, bs=2)
        dcsB.append('BIN2' + ''.join([chr(i) for i in s]))

        pass

        return [dcs, dcsB]


class B64H:
    @staticmethod
    def get_base64_diff_value(s1, s2):
        base64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        res = 0
        for i in range(len(s1)):
            if s1[i] != s2[i]:
                return abs(base64chars.index(s1[i]) - base64chars.index(s2[i]))
        return res

    @staticmethod
    def Dc(txt='', ds='utf-8'):
        file_lines = txt.split('\n')
        if len(file_lines) < 2: return []
        b64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

        bin_str = ''
        for line in file_lines:
            try:
                stegb64 = line.replace('\n', '')
                tmpStr = base64.b64encode(base64.b64decode(stegb64))
                rowb64 = str(tmpStr, ds)
                offset = abs(b64chars.index(stegb64.replace('=', '')[-1]) - b64chars.index(rowb64.replace('=', '')[-1]))
                equalnum = stegb64.count('=')  # no equalnum no offset
                if equalnum:
                    bin_str += bin(offset)[2:].zfill(equalnum * 2)
            except:
                pass
        ret = (''.join([chr(int(bin_str[i:i + 8], 2)) for i in range(0, len(bin_str), 8)]))
        return [[ret], ['B64H']]


class Fence:
    @staticmethod
    def WDc(encrypted, num):  # 奇葩的W形栅栏
        matrix = [([0] * len(encrypted)) for i in range(num)]
        cur = 0
        for i in range(num):  # 按行来填
            # 生成每行空格个数的取值序列
            if i == 0:  # 第1行和最后一行，只需要一个取值就好了
                pair = [(num - (i + 1)) * 2 - 1]
            elif i == num - 1:
                pair = [i * 2 - 1]
            else:
                pair = [(num - (i + 1)) * 2 - 1, i * 2 - 1]

            # 按规则填入
            pair_i = 0
            j = i
            while True:
                if cur < len(encrypted):
                    matrix[i][j] = encrypted[cur]
                cur += 1
                j += pair[pair_i % len(pair)] + 1  # 这里要加1，直接加间隔是不够的
                pair_i += 1
                if j >= len(encrypted):
                    break

        # 获取i的取值序列
        i_s = []
        for a in range(num):
            i_s.append(a)
        for a in range(num - 2, 0, -1):
            i_s.append(a)
        i_s_len = len(i_s)
        # 按规则取出
        decrypted = ''
        for j in range(len(encrypted)):
            decrypted += matrix[i_s[j % i_s_len]][j]
        return decrypted

    @staticmethod
    def Dc(txt="", zls=None):
        if len(txt) < 3: return txt
        ret = []
        ret2 = []
        zl = []
        l = len(txt)
        if zls != None and zls < l and zls > 0:
            zl.append(zls)
            if (l % zls) != 0:
                txt += " " * (zls - (l % zls))
        else:
            zl.extend(uf.MathCump.prime(l))
        l = len(txt)
        ret = []
        for i in zl:
            tmpstr = ""
            for j in range(l // i):
                for k in range(i):
                    tmpstr += txt[k * (l // i) + j]
            ret.append(tmpstr)
            ret2.append("Fence:%d" % i)
            ret.append(Fence.WDc(txt, i))
            ret2.append("Fence_W:%d" % i)
        return [ret, ret2]


class Filler:  # 过滤器
    # func为回调函数，bool func(str) 默认为恒真
    @staticmethod
    def Filler_defFunc(instr):
        return True

    def write(inx, fn='', func=None, cs='utf-8'):
        ret = Filler.filler(inx, func)
        if len(ret) == 0: return;
        f = open(fn, 'w', encoding=cs, errors='ignore')
        if isinstance(ret[0], list):
            for i in range(len(ret[0])):
                f.write(ret[0][i] + '\n')
                f.write(str(ret[1][i]) + '\n')
                f.write("-" * 40 + '\n')
        elif isinstance(ret[0], str):
            for i in range(len(ret)):
                f.write(ret[i])
        f.close()

    @staticmethod
    def print(inx, func=None):
        ret = Filler.filler(inx, func)
        if len(ret) == 0: return;
        if isinstance(ret[0], list):
            for i in range(len(ret[0])):
                print(ret[0][i])
                print(ret[1][i])
                print("-" * 40)
        elif isinstance(ret[0], str):
            for i in range(len(ret)):
                print(ret[i])

    @staticmethod
    def filler(inx, func=None):
        if not isinstance(inx, list): return [inx]
        if len(inx) == 0: return []
        if (func == None): func = Filler.Filler_defFunc
        if isinstance(inx[0], list):
            ret = [[], []]
            for i in range(len(inx[0])):
                if func(inx[0][i]):
                    ret[0].append(inx[0][i])
                    ret[1].append(inx[1][i])
            return ret
        elif isinstance(inx[0], str):
            ret = []
            for i in range(len(inx)):
                if func(inx[i]):
                    ret.append(inx[i])
            return ret
        return inx


class Power:
    @staticmethod
    def Dc(txt=''):
        a = txt.split("0")
        flag = ''
        try:
            for i in range(0, len(a)):
                str = a[i]
                list = []
                sum = 0
                for j in str:
                    list.append(j)
                    length = len(list)
                for k in range(0, length):
                    sum += int(list[k])
                flag += chr(sum + 64)
        except:
            pass
        return [[flag], ['Powre']]


class TJ_ROOL:  # 托马斯转轮 key从1开始
    def Dc(r=[''], c='', key=[]):
        ret = []
        if len(key) != 0: return TJ_ROOL.DcK(r, c, key)
        kl = uf.MathCump.AllRange([x + 1 for x in range(len(r))])
        for x in kl:
            ret = f_JoinAnsList(ret, TJ_ROOL.DcK(r, c, x))
        return ret

    @staticmethod
    def DcK(r=[''], c='', key=[]):
        ret1 = []
        ret2 = []
        if len(r) < len(key) or len(c) > len(r): return []
        newl = []
        for i in key:
            newl.append(r[i - 1].lower())
        finl = []
        for i in range(len(c)):
            t = str(newl[i])
            k = c[i].lower()
            x = t.find(k)
            if x >= 0:
                t = t[x:] + t[:x]
            finl.append(t)
        for i in range(len(finl[0])):
            x = ''
            for j in range(len(finl)):
                x += finl[j][i]
            ret1.append(x)
            ret2.append('TJ:' + str(key) + '| %2d' % i)
        return [ret1, ret2]


class rsaT:
    @staticmethod
    def D(p, q, e=65537):
        return int(gmpy2.invert(e, (p - 1) * (q - 1)))

    @staticmethod
    def decode(inx, key):
        ret = []
        rt1 = []
        rt2 = []
        try:
            cp1 = Cipher_pkcs1_v1_5.new(key)
            c = cp1.decrypt(inx, None)
            rt1.append(str(c, 'utf-8'))
            rt2.append('RSA-Cipher_pkcs1_v1_5')
        except:
            pass
        try:
            cp2 = PKCS1_OAEP.new(key)
            c = cp2.decrypt(inx, None)
            rt1.append(str(c, 'utf-8'))
            rt2.append('RSA-PKCS1_OAEP')
        except:
            pass
        return [rt1, rt2]

    @staticmethod
    # 仅支持文件和16进制字符串
    def Dc(st, p, q, file=False, e=65537):

        rb = ''
        d = rsaT.D(p, q, e)
        key = RSA.construct((p * q, e, d))

        if file:
            with open(st, 'rb') as infile2:
                dat = infile2.read()
                return rsaT.decode(dat, key)
        elif isinstance(st, bytes):
            return rsaT.decode(st, key)
        elif isinstance(st, list):
            return rsaT.decode(bytes(st), key)
        elif isinstance(st, str):
            nl = CharF.str2num(st)
            return rsaT.decode(bytes(nl), key)
        return []


F = [  # 字频率矩阵
    0.0651738, 0.0124248, 0.0217339, 0.0349835, 0.1041442, 0.0197881,
    0.0158610, 0.0492888, 0.0558094, 0.0009033, 0.0050529, 0.0331490,
    0.0202124, 0.0564513, 0.0596302, 0.0137645, 0.0008606, 0.0497563,
    0.0515760, 0.0729357, 0.0225134, 0.0082903, 0.0171272, 0.0013692,
    0.0145984, 0.0007836]


class Excange:
    fDic = {'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835,
            'e': 0.1041442, 'f': 0.0197881, 'g': 0.015861, 'h': 0.0492888,
            'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.033149,
            'm': 0.0202124, 'n': 0.0564513, 'o': 0.0596302, 'p': 0.0137645,
            'q': 0.0008606, 'r': 0.0497563, 's': 0.051576, 't': 0.0729357,
            'u': 0.0225134, 'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692,
            'y': 0.0145984, 'z': 0.0007836}

    @staticmethod
    def DC(tt="", decod=[], rTab=["", ""]):

        lDic = {}
        txt = tt
        if len(rTab[0]) == 0:
            txt = tt.lower()
            if len(decod) == 0:
                lDic = Excange.fDic
            else:
                if len(decod) < 26:
                    l = len(decod)
                    for i in range(26 - l + 1): decod.append(0)
                lDic = {chr(ord('a') + i): decod[i] for i in range(26)}
            rTab[1] = uf.OrderByValue.d2str(lDic)
            d = {chr(a): 0 for a in range(ord('a'), ord('z') + 1)}
            for i in txt:
                if i in d: d[i] += 1
            rTab[0] = uf.OrderByValue.d2str(d)
        dl = len(rTab[0]) - len(rTab[1])
        if dl > 0: rTab[1] += "_" * dl
        rt = ''
        for c in txt:
            pos = rTab[0].find(c)
            if pos >= 0:
                rt += rTab[1][pos]
            else:
                rt += c
        return [[rt], ['\nExcange:' + rTab[0] + '->' + rTab[1]]]

    def __init__(self, txt=''):
        self.txt = txt
        self.change = {chr(ord('a') + i): '*' for i in range(26)}

    def soveit(self):
        while 1:

            for i in self.txt:
                if not i.isalpha():
                    printc(i, cmd_color.green, end='')
                else:
                    x = self.change[i.lower()]
                    if '*' in x:
                        printc(i, cmd_color.red, end='')
                    elif i.islower():
                        printc(x, cmd_color.green, end='')
                    else:
                        printc(x.upper(), cmd_color.green, end='')
            print('\n' + '- ' * 80)
            for c in self.change:
                if '*' in self.change[c]:
                    printc(c + '->' + self.change[c], cmd_color.red, end='  ')
                else:
                    if list(self.change.values()).count(self.change[c]) > 1:
                        printc(c + '->' + self.change[c], cmd_color.brown, end='  ')
                    else:
                        printc(c + '->' + self.change[c], cmd_color.green, end='  ')
            print()

            cmdin = input("[CMD]").lower().strip().split()
            print('- ' * 80)

            if len(cmdin) == 1:
                for i in cmdin[0]:
                    try:
                        self.change[i] = '*'
                    except:
                        pass
            elif len(cmdin) == 2:
                for i in range(min(len(cmdin[0]), len(cmdin[1]))):
                    self.change[cmdin[0][i]] = cmdin[1][i]


class WebCode:  # 用于生成 ~%xx%xx之类的反向字符串
    @staticmethod
    def revCode(txt=''):
        ret = '~'
        for i in txt:
            x = (~ord(i)) & 0xFF
            ret += '%%%02x' % x
        return ret

    @staticmethod
    def drevCode(x=''):
        x = 'd0%99%93%9e%98%d1%8b%87%8b'.replace('%', '')
        x = CharF.str2num(x, spl=2)
        ret = ''
        for i in x:
            ret += chr((~i) & 0xFF)
        return ret


p = Filler.print
w = Filler.write


def CRC32(st=''):
    if isinstance(st, str): st = bytes(st, 'utf-8')
    return '%08X' % (crc32(st) & 0xffffffff)


def MD5s(st='', ) -> str:
    if isinstance(st, str): st = bytes(st, 'utf-8')
    m = hashlib.md5(st)
    return m.hexdigest()


def MD5f(fn='') -> str:
    with open(fn, 'rb') as fp:
        data = fp.read()
    return hashlib.md5(data).hexdigest()


def SHA1(s=''):
    return hashlib.sha1(s.encode()).hexdigest()


def SHA1f(fn=''):
    with open(fn, 'rb') as fp:
        data = fp.read()
    return hashlib.sha1(data).hexdigest()


class KFJC:
    @staticmethod
    def vig(ctext='', N=100, maxl=30):
        KFJC.Dc(ctext, N, maxl, pycipher.Vigenere)

    @staticmethod
    def vigf(fn='', N=100, maxl=30):
        ctext = open('fn', 'r').read()
        KFJC.Dc(ctext, N, maxl, pycipher.Vigenere)

    @staticmethod
    def auto(ctext='', N=100, maxl=30):
        KFJC.Dc(ctext, N, maxl)

    @staticmethod
    def autof(fn='', N=100, maxl=30):
        ctext = open('fn', 'r').read()
        KFJC.Dc(ctext, N, maxl)

    @staticmethod
    def Dc(text='', N=100, maxl=30, keyClass=pycipher.Autokey):
        ctext = ''
        for i in text.upper():
            if i.isupper():
                ctext += i
        qgram = ngram_score('quadgrams.txt')
        trigram = ngram_score('trigrams.txt')
        ctext = re.sub(r'[^A-Z]', '', ctext.upper())

        # keep a list of the N best things we have seen, discard anything else
        class nbest(object):
            def __init__(self, N=1000):
                self.store = []
                self.N = N

            def add(self, item):
                self.store.append(item)
                self.store.sort(reverse=True)
                self.store = self.store[:self.N]

            def __getitem__(self, k):
                return self.store[k]

            def __len__(self):
                return len(self.store)

        # init
        ret1 = []
        ret2 = []

        for KLEN in range(2, maxl):
            rec = nbest(N)

            for i in permutations('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 3):
                key = ''.join(i) + 'A' * (KLEN - len(i))
                pt = keyClass(key).decipher(ctext)
                score = 0
                for j in range(0, len(ctext), KLEN):
                    score += trigram.score(pt[j:j + 3])
                rec.add((score, ''.join(i), pt[:30]))

            next_rec = nbest(N)
            for i in range(0, KLEN - 3):
                for k in range(N):
                    for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                        key = rec[k][1] + c
                        fullkey = key + 'A' * (KLEN - len(key))
                        pt = keyClass(fullkey).decipher(ctext)
                        score = 0
                        for j in range(0, len(ctext), KLEN):
                            score += qgram.score(pt[j:j + len(key)])
                        next_rec.add((score, key, pt[:30]))
                rec = next_rec
                next_rec = nbest(N)
            bestkey = rec[0][1]
            pt = keyClass(bestkey).decipher(ctext)
            bestscore = qgram.score(pt)
            for i in range(N):
                pt = keyClass(rec[i][1]).decipher(ctext)
                score = qgram.score(pt)
                if score > bestscore:
                    bestkey = rec[i][1]
                    bestscore = score
            ctTmp = keyClass(bestkey).decipher(ctext).lower()
            contx0 = 0
            outstr = ''
            for i in range(len(text)):
                if text[i].isalpha():
                    outstr += ctTmp[contx0]
                    contx0 += 1
                else:
                    outstr += text[i]

            print(outstr, '|%15f,%2d,%-30s' % (bestscore, KLEN, bestkey) + '|')
            ret1.append(keyClass(bestkey).decipher(ctext))
            ret2.append('autokey:' + bestkey)


from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
import binascii


class SM4a:

    @staticmethod
    def Ec_ECB(txt="", key=""):
        key = key.encode()
        value = txt.encode()
        crypt_sm4 = CryptSM4()
        crypt_sm4.set_key(key, SM4_ENCRYPT)
        encrypt_value = crypt_sm4.crypt_ecb(value)  # bytes类型
        print("encrypt value = ", binascii.b2a_hex(encrypt_value).decode())
        return binascii.b2a_hex(encrypt_value).decode();

    @staticmethod
    def Ec_BCB(txt="", key="", vi=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'):
        key = key.encode()
        txt = txt.encode()
        crypt_sm4 = CryptSM4()
        crypt_sm4.set_key(key, SM4_DECRYPT)
        encrypt_value = crypt_sm4.crypt_cbc(vi, txt)  # bytes类型
        print("encrypt value = ", binascii.b2a_hex(encrypt_value).decode())
        return binascii.b2a_hex(encrypt_value).decode();

    @staticmethod
    def Dc_ECB(txt="", key=""):
        key = key.encode()
        crypt_sm4 = CryptSM4()
        encrypt_value = binascii.a2b_hex(txt)
        crypt_sm4.set_key(key, SM4_DECRYPT)
        decrypt_value = crypt_sm4.crypt_ecb(encrypt_value)  # bytes类型
        print("decrypt value = ", decrypt_value)
        return decrypt_value

    @staticmethod
    def dc_BCB(txt="", key="", vi=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'):
        key = key.encode()
        crypt_sm4 = CryptSM4()
        encrypt_value = binascii.a2b_hex(txt)
        crypt_sm4.set_key(key, SM4_DECRYPT)
        decrypt_value = crypt_sm4.crypt_cbc(vi, encrypt_value)  # bytes类型
        print("decrypt value = ", decrypt_value)
        return decrypt_value


if __name__ == "__main__":
    a = 'cjV5RyBscDlJIEJqTSB0RmhCVDZ1aCB5N2lKIFFzWiBiaE0g'
    p(BaseX.Dc(a))
    pass;
