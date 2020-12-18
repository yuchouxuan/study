def LA2str(t):
    ret = ''
    if isinstance(t, bytes): return t.decode()
    if isinstance(t, tuple) or isinstance(t, list):
        for i in t:
            x = i

            ret += x
    elif isinstance(t, dict):
        for w in dict:
            x = dict[w]
            if isinstance(x, int): x = chr(x)
            ret += x
    return ret;


def List2Array(array):  # 一维变二维
    if isinstance(array[0], list):
        return array
    listA = []
    dirs = int(len(array) ** 0.5)
    for i in range(dirs):
        tmpList = []
        for c in range(dirs):
            tmpList.append(array[i * dirs + c])
        listA.append(tmpList)
    return listA


def Array2List(array):  # 二维变一维
    if not isinstance(array[0], list):
        return array
    listA = []
    for i in array:
        for c in i:
            listA.append(c)
    return listA


class OrderByValue:
    @staticmethod
    def d2l(iDic={}, ord=-1):
        s = sorted(iDic.items(), key=lambda x: (ord) * x[1])
        return s

    @staticmethod
    def d2sl(iDic={}, ord=-1):
        s = sorted(iDic.items(), key=lambda x: (ord) * x[1])
        ch = []
        fen = []
        for it in s:
            ch.append(it[0])
            fen.append(it[1])
        return [ch, fen]

    @staticmethod
    def d2str(iDic={}, ord=-1):
        s = sorted(iDic.items(), key=lambda x: (ord) * x[1])
        rt = ''
        for it in s:
            rt += it[0]
        return rt


def pc(inx):
    if isinstance(inx, list):
        for i in range(len(inx)):
            print(i, ':', inx[i])
    elif isinstance(inx, dict):
        for i in inx:
            print(i, ':', inx(i))
    else:
        print(inx)
