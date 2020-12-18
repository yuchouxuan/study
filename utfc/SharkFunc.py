class st_USB:
    normalKeys = {"04": "a", "05": "b", "06": "c", "07": "d", "08": "e", "09": "f", "0a": "g", "0b": "h", "0c": "i",
                  "0d": "j", "0e": "k", "0f": "l", "10": "m", "11": "n", "12": "o", "13": "p", "14": "q", "15": "r",
                  "16": "s", "17": "t", "18": "u", "19": "v", "1a": "w", "1b": "x", "1c": "y", "1d": "z", "1e": "1",
                  "1f": "2", "20": "3", "21": "4", "22": "5", "23": "6", "24": "7", "25": "8", "26": "9", "27": "0",
                  "28": "<RET>", "29": "<ESC>", "2a": "<DEL>", "2b": "\t", "2c": "<SPACE>", "2d": "-", "2e": "=",
                  "2f": "[", "30": "]", "31": "\\", "32": "<NON>", "33": ";", "34": "'", "35": "<GA>", "36": ",",
                  "37": ".", "38": "/", "39": "<CAP>", "3a": "<F1>", "3b": "<F2>", "3c": "<F3>", "3d": "<F4>",
                  "3e": "<F5>", "3f": "<F6>", "40": "<F7>", "41": "<F8>", "42": "<F9>", "43": "<F10>", "44": "<F11>",
                  "45": "<F12>"}
    shiftKeys = {"04": "A", "05": "B", "06": "C", "07": "D", "08": "E", "09": "F", "0a": "G", "0b": "H", "0c": "I",
                 "0d": "J", "0e": "K", "0f": "L", "10": "M", "11": "N", "12": "O", "13": "P", "14": "Q", "15": "R",
                 "16": "S", "17": "T", "18": "U", "19": "V", "1a": "W", "1b": "X", "1c": "Y", "1d": "Z", "1e": "!",
                 "1f": "@", "20": "#", "21": "$", "22": "%", "23": "^", "24": "&", "25": "*", "26": "(", "27": ")",
                 "28": "<RET>", "29": "<ESC>", "2a": "<DEL>", "2b": "\t", "2c": "<SPACE>", "2d": "_", "2e": "+",
                 "2f": "{", "30": "}", "31": "|", "32": "<NON>", "33": "\"", "34": ":", "35": "<GA>", "36": "<",
                 "37": ">", "38": "?", "39": "<CAP>", "3a": "<F1>", "3b": "<F2>", "3c": "<F3>", "3d": "<F4>",
                 "3e": "<F5>", "3f": "<F6>", "40": "<F7>", "41": "<F8>", "42": "<F9>", "43": "<F10>", "44": "<F11>",
                 "45": "<F12>"}

    @staticmethod
    def key_func(fn=''):
        output = []
        keys = open(fn)
        for line in keys:
            try:
                if line[0] != '0' or (line[1] != '0' and line[1] != '2') or line[3] != '0' or line[4] != '0' or line[
                    9] != '0' or line[10] != '0' or line[12] != '0' or line[13] != '0' or line[15] != '0' or line[
                    16] != '0' or line[18] != '0' or line[19] != '0' or line[21] != '0' or line[22] != '0' or line[
                                                                                                              6:8] == "00":
                    continue
                if line[6:8] in st_USB.normalKeys.keys():
                    output += [[st_USB.normalKeys[line[6:8]]], [st_USB.shiftKeys[line[6:8]]]][line[1] == '2']
                else:
                    output += ['[unknown]']
            except:
                pass
        keys.close()

        flag = 0
        print("".join(output))
        for i in range(len(output)):
            try:
                a = output.index('<DEL>')
                del output[a]
                del output[a - 1]
            except:
                pass
        for i in range(len(output)):
            try:
                if output[i] == "<CAP>":
                    flag += 1
                    output.pop(i)
                    if flag == 2:
                        flag = 0
                if flag != 0:
                    output[i] = output[i].upper()
            except:
                pass
        print('output :' + "".join(output))

    @staticmethod
    def mouse_fun(fn='data.txt'):
        nums = []
        keys = open(fn, 'r')
        posx = 0
        posy = 0
        for line in keys:
            if len(line) != 12:
                continue
        x = int(line[3:5], 16)
        y = int(line[6:8], 16)
        if x > 127:
            x -= 256
        if y > 127:
            y -= 256
        posx += x
        posy += y
        btn_flag = int(line[0:2], 16)  # 1 for left , 2 for right , 0 for nothing
        if btn_flag == 1:
            print
            posx, posy
        keys.close()



from utfc.StrFunc import *


def WS_GLOBAL_SPL(txt=''):
    txt = CharF.ReplaceAll(txt, '\t),]<>=', [' ' for _ in range(100)])
    txt = CharF.ReplaceAll(txt, '\'";[]()', ['' for _ in range(100)])
    return txt.split()


class SQLBI:
    sqls = []
    sql_rep = []

    def __init__(self, fn='', kw='select'):  # 假设需要查找的关键字为select
        f = open(fn, 'r', encoding='utf-8').readlines()
        for i in f:
            l = []
            j = i.split()
            for x in j:
                if kw in x:
                    l.append(x)
            if len(l) > 0:
                self.sqls.append(l)
                print(l)


    def rep(self, fumc=WS_GLOBAL_SPL):
        self.sql_rep = []
        for i in self.sqls:
            c = fumc(i[0])
            self.sql_rep.append(c)
            print(c)


    def noEFF(self, pos=3, asc=-1):
        flagd = {}
        for i in self.sql_rep:
            c = i[asc]

            try:
                c = chr(int(c))
            except:
                pass
            flagd[int(i[pos])] = c
        ret = ''
        for i in sorted(flagd.keys()):
            ret += flagd[i]
        print(ret)
        return ret


