#!/usr/bin/env python
# Filename: readgre.sh
# Author:   LIU Yang
# Create Time: Sun Aug 25 03:04:20 HKT 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com

import fileinput, shelve
import word
from config import GRE_DB

wordbook = dict()

windex = 10000 # Magic number 4 GRE words, no portable issue HA HA HA!
for line in fileinput.input():
    items = line.split()
    name, mean = items[0], ' '.join(items[1:])

    wordbook[windex] = word.word(name, mean)
    windex += 1

for idx in wordbook:
    print idx, wordbook[idx]

gre_db = shelve.open(GRE_DB)
for windex in wordbook:
    gre_db[str(windex)] = wordbook[windex]
gre_db.close()
