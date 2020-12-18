from subprocess import *
import time


class cmdF:
    cmd = ''

    def __init__(self, c=''):
        self.cmd = c

    def runScript(self, cmdL=[], sl=0.1):
        with  Popen(self.cmd, shell=True, stdin=PIPE, stdout=PIPE) as p:
            for i in cmdL:
                time.sleep(sl)
                p.stdin.write(bytes((i + '\n'), 'utf-8'))
            time.sleep(sl)
