#!/usr/bin/env python
# Filename: query.sh
# Author:   LIU Yang
# Create Time: Sun Aug 18 20:14:15 HKT 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
# Query word from vocabulary database created by "readwords.py"

import shelve, cPickle
import sys, getopt
from config import DB_name

db_read = shelve.open(DB_name)
for index in sys.argv[1:]:
	print db_read[index]
	print
