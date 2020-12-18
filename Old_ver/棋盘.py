''' Code by James Lyons for practicalcryptography.com 2016
All code is released under MIT licence '''
import random
from ngram_score import ngram_score
import re
import sys
from itertools import combinations

''' decrypt a straddle checkerboard cipher using the provided key
The first return value is an integer, 0 if the key is invalid, 1
if the key is valid. output is the decrypted text.'''


def scdecrypt(ctext, key):
    dotpos = []
    for i, k in enumerate(key):
        if k == '.': dotpos.append(i)
    output = ""
    flag = 0  # which row of the key are we in
    for cc in ctext:
        c = int(cc)
        if key[c] != '.' and flag == 0:
            output += key[c]
        elif flag == 1:
            if key[10 + c] == '.': return 0, ""
            output += key[10 + c]
            flag = 0
        elif flag == 2:
            if key[20 + c] == '.': return 0, ""
            output += key[20 + c]
            flag = 0
        elif c == dotpos[0]:
            flag = 1
        elif c == dotpos[1]:
            flag = 2
        else:
            return 0, output
    return 1, output


''' compute the index of coincidence for a piece of text '''


def ic(text):
    freq = {}
    for letter in text:
        if letter in freq:
            freq[letter] += 1.
        else:
            freq[letter] = 1.
    freqsum = 0.
    for letter in freq.keys():
        freqsum += freq[letter] * (freq[letter] - 1)
    N = len(text)
    IC = freqsum / (N * (N - 1))
    return IC


# get a list of all possible dot positions
first10 = combinations(range(10), 2)
all_dot_positions = [[i[0], i[1], 28, 29] for i in first10]

ctext = '6909746723099383772753870703607230943837727093872638757438333832743772974928387272384175943874720383270'
# we have all possible dot positions, try decrypting with each and see if we can discard any
texts = []
for d in all_dot_positions:
    key = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for pos in d: key.insert(pos, '.')
    # see if each key can be used to decrypt the ciphertext, keep it if yes
    valid, ptext = scdecrypt(ctext, key)
    if valid == 0:  # shuffle the dots till it works
        for p3, p4 in combinations(range(10, 30), 2):
            key = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            d = [d[0], d[1], p3, p4]
            for pos in d: key.insert(pos, '.')
            valid, ptext = scdecrypt(ctext, key)
            if valid == 1: break
    if valid == 0: continue  # we couldn't find any valid keys for this one
    texts.append((ic(ptext), ptext, ''.join(key)))

# print the IC, text, and decryption key for all the candidates
texts.sort()
for i, j in enumerate(range(len(texts))):
    print
    '%0.3f' % texts[j][0], texts[j][1], '\t', texts[j][2]
