class FileF:
    @staticmethod
    def s2f(fn='data.txt', txt='', cs='utf-8', errs='ignore'):
        with open(fn, 'w', encoding=cs, errors=errs) as f:
            f.write(txt)
            f.close()

    @staticmethod
    def l2f(fn='data.txt', txt=[], cs='utf-8', errs='ignore'):
        with open(fn, 'w', encoding=cs, errors=errs) as f:
            for t in txt:
                f.write(t)
            f.close()

    @staticmethod
    def f2int(fn='data.txt', orders='big'):
        with open(fn, 'rb') as f:
            hex_c = f.read()
        return int.from_bytes(hex_c, byteorder=orders)

    @staticmethod
    def l2bf(fn='data.txt', dat=b''):
        bst = b''
        if isinstance(dat, str):
            bst = bytes(dat, 'utf-8')
        elif isinstance(dat, list):
            bst = bytes(dat)
        else:
            bst = dat
        with open(fn, 'wb') as f:
            f.write(bst)
            f.close()

    @staticmethod
    def f2s(fn='data.txt', cs='utf-8', errs='ignore'):
        f = open(fn, 'r', encoding=cs, errors=errs)
        s = f.read()
        f.close()
        return s

    @staticmethod
    def f2l(fn='data.txt', cs='utf-8', errs='ignore'):
        ret = []
        with open(fn, 'r', encoding=cs, errors=errs) as f:
            f.seek(0, 2)  # 指针移动到文件末尾
            size = f.tell()  # 此时指针的位置即文件末尾的位置
            f.seek(0, 0)  # 把指针移回文件开头
            while f.tell() < size:  # 如果指针在size之前
                s = f.readline().rstrip("\n")  # 用readline()读一行
                if s.strip() == '':  # 如果读到的是空行
                    continue  # 跳过该行
                ret.append(s)
        f.close()
        return ret

    @staticmethod
    def bf2l(fn='data.txt'):
        with open(fn, 'rb') as f:
            return f.read()

    @staticmethod
    def rev(fn1="", fn2=""):
        open(fn2, 'wb').write(open(fn1, 'rb').read()[::-1])
