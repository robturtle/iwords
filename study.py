#!/usr/bin/env python
# Filename: study.sh
# Author:   LIU Yang
# Create Time: Mon Aug 19 21:55:58 HKT 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
# Brief: Use this to learn new words

import shelve, sys, getopt
import wordlist, learn_interface
from config import DB_name

mode = 'learn'

# Handling options
shortargs = 'r'
longargs  = ['review']
opts, args = getopt.getopt(sys.argv[1:], shortargs, longargs)
for opt, value in opts:
    if opt in ['-r', '--review']:
        mode = 'review'

# Prepare data
db = shelve.open(DB_name)
wlist, partlist = wordlist.generate_wordlist(mode)

# Start learning
learn_interface.study(mode, db, wlist)

wordlist.writestat()
db.close()
