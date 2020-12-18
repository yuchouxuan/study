import requests
from base64 import b64decode


def postx(url, payload):
    s = requests.Session()  # 保证一个session这样才能根据给出的随机flag匹配最终flag
    a = s.get(url).headers['flag']
    # flag=b64decode(a).decode()    #解码headers中的flag，但是解码出来需要decode再次解码。
    # key=b64decode(flag.split(':')[1])   #解码出内容为：跑的还不错，给你flag吧: ODgzMTc= ，需要截取:右边内容所以用到split截取以冒号分割的第二个内容。
    # payload={'margin':key}
    r = s.post(url, data=payload)
    print(r.text)
    return r.text


iph = '75.16.16.'
ips = [iph + str(i) for i in range(255)];
print(ips)
