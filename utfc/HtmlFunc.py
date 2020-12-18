import bs4
import requests


class htmf:
    html = ''
    soup = None

    def __init__(self, txt='', url='', fn='', features='html.parser'):
        if url == '' and fn == '':
            self.html = txt
        elif fn == '':
            self.html = requests.get(url).text
        else:
            self.html = open(fn, 'r').read()
        self.soup = bs4.BeautifulSoup(self.html, features=features)
