import gmpy2
import libnum
import opensource.RSAwienerHacker as RSAwienerHacker
import Crypto.PublicKey.RSA as rsaKey

'''RSA脚本库-缺unusual系列1、2、4、5
---------------------------------------------------------------------
dyze        |e有多个因子
------------|--------------------------------------------------------
dyzn        |n有多个因子
------------|--------------------------------------------------------
cdn         |已知dnc 常规解法
------------|--------------------------------------------------------
pqec        |已知 pqec
------------|--------------------------------------------------------
dpenc       |已知 dp e n c
------------|--------------------------------------------------------
dpdqqpc     |已知 dp，dq，p，q，c
------------|--------------------------------------------------------
gmgj        |共模攻击 已知 n,e*2，c*2， 明文，n相同
------------|--------------------------------------------------------
demsn       |广播攻击 c，e，n*2 同一明文， n有公约数
------------|--------------------------------------------------------
smalle      |n,c,e e很小 比如3
------------|--------------------------------------------------------
bige        |n,c,e e很大 和c差不多长
------------|--------------------------------------------------------
npk         | n=p^k
------------|--------------------------------------------------------
readKey     |读取写key文件
creatKey    |
------------|--------------------------------------------------------
zgwgj       |已知高位攻击 知道p或q的高位
------------|--------------------------------------------------------
dxsrsa1     |N，C均为多项式
---------------------------------------------------------------------'''



def ned2qp(n, e, d):
    p = 1
    q = 1
    import random
    while p == 1 and q == 1:
        k = d * e - 1
        g = random.randint(0, n)
        while p == 1 and q == 1 and k % 2 == 0:
            k /= 2
            y = pow(g, k, n)
            if y != 1 and gmpy2.gcd(y - 1, n) > 1:
                p = gmpy2.gcd(y - 1, n)
                q = n / p
    return p, q

def pollardRhoAttack(N, B=1000000, a=2):
    CODE_ARG = 0
    CODE_FAIL = 1
    def moduloPower(a, i, N):
        """ Returns a**i (mod N) """
        """ Complexity: O( log(B) * log^2(N) ) """
        val = 1
        while i > 0:
            if i % 2:
                val *= a
                val %= N
            a *= a
            a %= N
            i /= 2
        return val
    """ Implementation of Pollard's Rho - 1 Attack """
    """ Worst Case Complexity: O( ( B * log(B) + log(N) ) * log^2(N) ) """
    # computing a**(B!) (mod N)
    for i in range(2, B + 1):
        # computing a**(i!) (mod N)
        a = moduloPower(a, i, N)
        # computing gcd(a - 1, N)
        d = gmpy2.gcd(a - 1, N)
        if 1 < d and d < N:
            print('Prime Factorization of', N)
            print('(', d, ',', N / d, ')')
            return d

    class rsaQues:
        @staticmethod
        def npk(p, k, e, c):
            phi = (p - 1) * (p ** (k - 1))
            n = p ** k
            d = gmpy2.invert(e, phi)
            m = int(pow(c, d, n))
            print('[HEX]' + hex(m)[2:])
            try:
                print('[STR]' + libnum.n2s(m))
            except:
                pass
            return m

    @staticmethod
    def dyze(p, q, c, e=[4, 3], ):
        n = p * q
        phi = (p - 1) * (q - 1)
        dx = libnum.invmod(e[1], phi)
        dx = gmpy2.powmod(c, dx, n)
        m = gmpy2.iroot(dx, e[0])[0]
        print('[HEX]' + hex(m)[2:])
        try:
            print('[STR]' + libnum.n2s(m))
        except:
            pass
        return m

    @staticmethod
    def dyzn(e, c, p=[2, 3, 5], ):
        n = 1
        for i in p:
            n *= i
        phi = 1
        for i in p:
            phi *= (i - 1)
        d = gmpy2.invert(e, phi)
        m = pow(c, d, n)
        print(libnum.n2s(m))
        return m

    @staticmethod
    def cdn(d, n, c):  # 已知 d n c 常规解法
        m = pow(c, d, n)
        print(libnum.n2s(m))
        return m;

    @staticmethod
    def pqec(p, q, e, c):
        n = p * q
        phi = (p - 1) * (q - 1)
        d = gmpy2.invert(e, phi)
        m = pow(c, d, n)
        print('[HEX]', hex(m)[2:])
        try:
            print(libnum.n2s(m))
            return (libnum.n2s(m))
        except:
            pass
        return m;

    @staticmethod
    # 已知（dp,e,n,c） dp=d%(p-1)
    def dpenc(e, n, dp, c):
        for i in range(1, 65538):
            if (dp * e - 1) % i == 0:
                if n % (((dp * e - 1) // i) + 1) == 0:
                    p = ((dp * e - 1) // i) + 1
                    q = n // (((dp * e - 1) // i) + 1)
                    phi = (p - 1) * (q - 1)
                    d = gmpy2.invert(e, phi) % phi
                    print(libnum.n2s(pow(c, d, n)))

    @staticmethod
    # 已知(dp,dq,q,p,c)
    def dpdqqpc(dp, dq, p, q, c):
        InvQ = gmpy2.invert(q, p)
        mp = pow(c, dp, p)
        mq = pow(c, dq, q)
        m = (((mp - mq) * InvQ) % p) * q + mq
        try:
            print(libnum.n2s(m))
        except:
            print(hex(m))
        return hex(m)[2:]

    @staticmethod
    # 工模攻击 适用情况：明文m、模数n相同，公钥指数e、密文c不同，gcd(e1,e2)==1
    def gmgj(n, c1, c2, e1, e2):
        s = gmpy2.gcdext(e1, e2)
        s1 = s[1]
        s2 = -s[2]
        c2 = gmpy2.invert(c2, n)
        m = (pow(c1, s1, n) * pow(c2, s2, n)) % n
        print(libnum.n2s(m))

    @staticmethod
    # e,同一明文，n有公约数,广播攻击
    def demsn(e, c, n=[]):
        for i in n:
            for j in n:
                if not (i == j):
                    pub_p = gmpy2.gcdext(i, j)
                    if not (pub_p[0] == 1) & (i > j):
                        print(i, j, p[0])
                        a = i, p = pub_p[0]
        q = a / p
        n = p * q
        phi = (p - 1) * (q - 1)
        d = gmpy2.invert(e, phi)
        m = pow(c, d, n)
        print(hex(m))

    @staticmethod
    # 适用于m很小
    def smalle(n, c, e=3):
        m = 0  # res是m
        for k in range(200000000):
            if gmpy2.iroot(c + n * k, e)[1] == 1:
                m = gmpy2.iroot(c + n * k, e)[0]
                print(k, m)
                print(libnum.n2s(m))
                return m

    @staticmethod
    # 适用于 e很大
    def bige(n, e, c):
        d = RSAwienerHacker.hack_RSA(e, n)
        return rsaQues.cdn(d, n, c)

    @staticmethod
    def readKey(fn):
        pk = rsaKey.import_key(open(fn).read())
        print('e=', pk.e)
        print('n=', pk.n)
        return (pk.e, pk.n)

        @staticmethod
        # openssl rsautl -decrypt -in flag.enc -out flag.dec -inkey private.pem
        def creatKey(n, e, d, p, q, fn):
            keypair = rsaKey.construct((n, e, d, p, q))
            private = open(fn, 'wb')
            private.write(keypair.exportKey())
            private.close()


    zgwgj = '''# 已知高位攻击 知道p或q的高位
# git下了一个sage的脚本，不知道好使不好使
n=0x79e0bf9b916e59286163a1006f8cefd4c1b080387a6ddb98a3f3984569a4ebb48b22ac36dff7c98e4ebb90ffdd9c07f53a20946f57634fb01f4489fcfc8e402865e152820f3e2989d4f0b5ef1fb366f212e238881ea1da017f754d7840fc38236edba144674464b661d36cdaf52d1e5e7c3c21770c5461a7c1bc2db712a61d992ebc407738fc095cd8b6b64e7e532187b11bf78a8d3ddf52da6f6a67c7e88bef5563cac1e5ce115f3282d5ff9db02278859f63049d1b934d918f46353fea1651d96b2ddd874ec8f1e4b9d487d8849896d1c21fb64029f0d6f47e560555b009b96bfd558228929a6cdf3fb6d47a956829fb1e638fcc1bdfad4ec2c3590dea1ed3
p=0xd1c520d9798f811e87f4ff406941958bab8fc24b19a32c3ad89b0b73258ed3541e9ca696fd98ce15255264c39ae8c6e8db5ee89993fa44459410d30a0a8af700ae3aee8a9a1d6094f8c757d3b79a8d1147e85be34fb260a970a52826c0a92b46cefb5dfaf2b5a31edf867f8d34d2222900000000000000000000000000000000
p_fake = p+0x100000000000000000000000000000000
pbits = 1024
kbits = pbits-576
pbar = p_fake & (2^pbits-2^kbits)
print ("upper %d bits (of %d bits) is given" % (pbits-kbits, pbits))
PR.<x> = PolynomialRing(Zmod(n))
f = x + pbar
x0 = f.small_roots(X=2^kbits, beta=0.4)[0]  # find root < 2^kbits with factor >= n^0.4
print(hex(x0 + pbar))
'''

dxsrsa1 = '''#N，C均为多项式
e=0x10001
P=2470567871
R.<x> =  PolynomialRing(GF(P))
N=1932231392*x^255 +……
C=922927962*x^254 + ……
#factor(N)
#两个x的最高次幂记录做p'=127；q'=128
#phi=(e^p-1)(e^q-1)
phi=(P^127-1)*(P^128-1)
d = inverse_mod(e, phi)
m = pow(C, d, N)
print(m)
#多项式系数即为明文
'''
