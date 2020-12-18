from Afox import *

from pathlib import Path


def test():
    str = ''
    a = 25
    b = 1
    se = requests.Session()

    bu = 'https://www.jjr8.cc/book.php/?a_id='
    for type in range(a, 33):
        for ux in range(b, 2000):
            b = 1
            u = 'https://douyinxjj.com/?s=book/type/%d/%d.html' % (type, ux)
            printbi(type, "%d" % ux, 5)
            try:
                s = htmf.htmf(url=u)
            except:
                s = htmf.htmf(txt='')
                print('INEDXERROR')
            s = s.soup.select('div[class="layui-col-xs12 book-list"]')
            try:
                tmpl = len(s[0].select("a"))
                if tmpl < 1: break;
            except:
                pass
            for x in s:
                v = x.select("a")
                for w in v:
                    url = bu + CharF.mask(w.attrs['href'], '?s=book/view/id/', '.html')
                    name = w.text.replace('\n', '').replace('\r', '')[:-10]
                    name = CharF.ReplaceChar(name, '?.*_\\/:<>|"\'：', '                            ').replace(' ', '')

                    fn = 'd:\\text\\' + name + '.html'
                    mf = Path(fn)
                    text = ''
                    if (not mf.exists()) or len(open(fn, 'rb').read()) < 300:
                        try:
                            text = CharF.mask(se.get(url).text, 'document.write("', '");document.write')
                        except:
                            pass
                        if 'Fatal error' in text:
                            print('x', end=' ')
                        else:
                            if not mf.exists():
                                print('+', end=' ')
                            else:
                                print('*', end=' ')
                            FileF.s2f(fn, text)
                    else:
                        print('=', end=' ')


def addhead():
    head = '''<style type="text/css">
    body,td,th {
    	font-family: "宋体";
    	font-size: 26pt;
    	color: #CCC;
    	line-height:36pt
    }
    body {
    	background-color: #000;
    }
    </style>'''

    ix = 0
    fl = os.listdir('d:\\text\\')
    for i in fl:
        try:
            i = i.replace(' ', '').replace('\t', '').lower()
            if i == 'x': continue
            print('%3d |' % (int(ix * 100 / len(fl))), i, end='\r')
            fnr = 'd:\\text\\' + i
            fnw = 'd:\\text\\x\\' + CharF.ReplaceChar(i, '【】（）', '[]()')

            strx = FileF.f2s(fnr).replace('font', 'fuck')
            strx = strx.replace(' />', '/>')

            FileF.s2f(fnw, head + strx)
        except:
            print('[x]')
        ix += 1


addhead()
