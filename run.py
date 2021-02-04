import datetime as datetime_hh
import os
import platform

if 'indows' in platform.system():
    os.system('cls')
head_tps = datetime_hh.datetime.now()
print('PROGRAM START:', head_tps)
print('-' * 120)

import test

print()
print('-' * 120)
head_tes = datetime_hh.datetime.now()
print('EXECTIME:', head_tes - head_tps)
