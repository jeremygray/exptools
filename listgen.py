#!/usr/bin/env python

"""word-list generator for creative pressure experiment

three similar lists: 36 nouns each, balanced for word length, KF word freq, Barch constraint
3 conditions: normal, creative, average

need 108 trials (noun, condition, color), as two .csv files (54 trials each)
3 counterbalanced conditions, with 2 of each type in a row, mini-blocked
use the lists in sequential order from within the experiment

results stored in two files 'firsthalf.csv', 'secondhalf.csv'
"""


from random import shuffle
import numpy as np


# for counterbalancing lists x prompts:
ctrBalance = 0  # 0, 1, or 2

# define header = var names in python in the experiment script
header = 'noun,prompt,cueColor'

# Kucera Francis word norm data:
k = open('KFwordfreq.txt', 'r').readlines()
kf = {}
for wf in k:
    if len(wf) < 2: continue
    w, f = wf.split()
    kf[w] = int(f)

# constraint (from Barch dataset)
k = open('constraint.csv', 'r').readlines()
con = {}
for wf in k[1:]:
    if len(wf) < 2: continue
    w, c = wf.split(',')
    con[w.lower()] = float(c.strip())

# word lists for the study, 108 nouns in three similar lists:
#alist = open('a.txt', 'r').read().split()
#blist = open('b.txt', 'r').read().split()
#clist = open('c.txt', 'r').read().split()

alist = ['bread', 'oath', 'flower', 'yard', 'boot', 'grass', 'hand', 'artist', 'cannon', 'lamp', 'taxi', 'bucket', 'note', 'belt', 'candle', 'ship', 'shoe', 'clay', 'tree', 'needle', 'card', 'rose', 'paper', 'story', 'mile', 'radio', 'idea', 'gift', 'lung', 'meat', 'cake', 'bullet', 'water', 'stove', 'car', 'debt']
blist = ['floor', 'muscle', 'home', 'leaf', 'key', 'brush', 'infant', 'word', 'beach', 'drum', 'dish', 'bag', 'hammer', 'store', 'baby', 'letter', 'pill', 'poem', 'tool', 'soap', 'couch', 'golf', 'soup', 'feet', 'fork', 'pool', 'banana', 'pillow', 'plane', 'drug', 'mirror', 'jeep', 'band', 'pipe', 'shirt', 'door']
clist = ['bow', 'safe', 'hair', 'tongue', 'phone', 'tooth', 'bird', 'street', 'glass', 'razor', 'sofa', 'fist', 'money', 'coal', 'horn', 'blade', 'ring', 'shovel', 'rock', 'house', 'finger', 'snow', 'cart', 'manual', 'pistol', 'towel', 'gun', 'lawn', 'office', 'dress', 'hole', 'pond', 'pencil', 'beef', 'maid', 'road']

# check KF values for specific words, to see good candidates to swap between lists:
#for w in ['sofa','leaf','hammer','taxi']:
#    print w, kf[w]

# check list similarity
for lst in [alist, blist, clist]:
    a = [len(b) for b in lst]
    k = [kf[b] for b in lst]
    c = [con[b] for b in lst]
    #print lst[0], np.mean(a), np.std(a), np.mean(k), np.std(k), np.mean(c), np.std(c)

shuffle(alist)
shuffle(blist)
shuffle(clist)

# counterbalance lists x conditions:
if ctrBalance == 1:
    alist, blist, clist = blist, clist, alist
elif ctrBalance == 2:
    alist, blist, clist = clist, alist, blist

# generate prompts (n=108, for 108 trials)
prompts = ['normal', 'creative', 'average']
colors = {'normal': 'darkgreen', 'creative': 'darkblue', 'average': 'darkred'}
promptList = []
for i in range(18):
    shuffle(prompts)
    for p in prompts:  # double each one, for two in a row
        promptList.append(p)
        promptList.append(p)

# make two .csv files, each with a header row and half the prompt info:
alistCtr = 0
blistCtr = 0
clistCtr = 0
start = 0
for filename in ['firsthalf.csv', 'secondhalf.csv']:
    with open(filename, 'wb') as fd:
        fd.write(header + '\n')
        for p in promptList[start:start + 54]:
            if p == 'normal':
                word = alist[alistCtr]
                alistCtr += 1
            elif p == 'creative':
                word = blist[blistCtr]
                blistCtr += 1
            elif p == 'average':
                word = clist[clistCtr]
                clistCtr += 1
            fd.write(','.join([word, p, colors[p]]))
            fd.write('\n')
    start += 54
