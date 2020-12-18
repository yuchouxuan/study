# encoding=utf-8
from scapy.all import *
import re
import datetime


def test(page):
    '''
    第一层是数据链路层，第二层是ip层，第三层是tcp层——>包含端口号、http报文,第四层是应用层
    其中每一层均为上一层的payload成员
    '''
    for f in page.payload.payload.payload.fields_desc:
        # f.name为Raw的字段名称——>load：传输的http请求信息
        fvalue = page.payload.payload.getfieldval(f.name)
        reprval = f.i2repr(page.payload.payload, fvalue)  # 转换成十进制字符串
        if 'HTTP' in reprval:
            lst = str(reprval).split(r'\r\n')
            la = re.findall('(GET )|(POST )', lst[0])
            if la != []:
                if la[0][0] == '':
                    with open('sql.txt', 'r+') as file:
                        for fi in file.readlines():
                            if fi.strip('\n') in str(lst[-1]).lower():
                                try:
                                    i = datetime.datetime.now()
                                    print("[!]您正在被攻击！")
                                    print('[*]攻击时间是\t' + str(i))
                                    beiattack = re.findall('Host: \w{3}\.\w{3}\.\w{3}\.\w{3}', str(lst))
                                    print('[*]被SQL注入攻击的IP为\t' + beiattack[0].strip("Host: "))
                                    print('[*]攻击的payload是\t' + lst[-1].strip('\''))
                                    print('[*]提交的方式为\tPOST')
                                    with open('danger.log', 'a+') as f:
                                        f.write(
                                            "[!]您正在被攻击！\n [*]攻击时间是\t%s\n[*]被SQL注入攻击的IP为\t%s\n[*]攻击的payload是\t%s\n[*]提交的方式为\t POST\n\n" % (
                                                str(i), beiattack[0], lst[-1]))
                                except:
                                    pass
                if la[0][1] == '':
                    with open('sql.txt', 'r+') as file:
                        for fi in file.readlines():
                            if fi.strip('\n') in str(lst[0]).lower():
                                try:
                                    i = datetime.datetime.now()
                                    print("[!]您正在被攻击！")
                                    beiattack = re.findall('Host: \w{3}\.\w{3}\.\w{3}\.\w{3}', str(lst))
                                    print('[*]攻击时间是\t' + str(i))
                                    print('[*]被SQL注入攻击的IP为\t' + beiattack[0].strip("Host: "))
                                    print('[*]攻击的payload是\t' + lst[0].strip('\'GET '))
                                    print('[*]提交的方式为\tGET')
                                    with open('danger.log', 'a+') as f:
                                        f.write(
                                            "[!]您正在被攻击！\n[*]攻击时间是\t%s\n [*]被SQL注入攻击的IP为\t%s\n[*]攻击的payload是\t%s\n[*]提交的方式为\t GET\n\n" % (
                                                str(i), beiattack[0], lst[0]))
                                except:
                                    pass


def main():
    # 无限抓取通过VMware Virtual Ethernet Adapter for VMnet8网卡并且主机为192.168.209.137的数据包并传给回调函数test
    a = sniff(filter='host 192.168.209.137', iface="VMware Virtual Ethernet Adapter for VMnet8", prn=test, count=0)


if __name__ == '__main__':
    main()
