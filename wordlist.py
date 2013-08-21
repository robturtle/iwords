#!/usr/bin/env python
# Filename: wordlist.sh
# Author:   LIU Yang
# Create Time: Mon Aug 19 21:55:58 HKT 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
# Brief: Load status and generate word list

import sys, random
import json, shelve
from config import wordbook_prefix, statfile, DB_name

# status datafield
# part_count:  Count of learning units.
# current_no:  Index of learning units. The best practice is 1 unit/day.
# have_learnt: Have this unit been learnt?
# have_reviewed: Have this unit been reviewed?
# review_day: A list indicating the new words in this unit should exist
# ----------  in which review unit.
# ----------  For Example, [2, 4, 8] mean this unit's new words will
# ----------  be shown in the 2th, 4th and 8th review unit from current
# ----------  unit
# longterm_interval: Review interval after processed review_day list.

def loadstat():
    statf = file(statfile, 'r')
    status = json.loads(statf.read())
    statf.close()
    return status

try:
    stat = loadstat()
except IOError:
    sys.stderr.write('ERR: %s not found! Try run schedule.py again' % statfile)

def writestat():
    statf = file(statfile, 'w+')
    statf.write(json.dumps(stat, indent=4))
    statf.close()


try:
    wordbook = [file(wordbook_prefix+str(i), 'r')
      for i in range(stat['part_count'])]
except IOError:
    sys.stderr.write('ERR: %s not found! Try run schedule.py agian.' % wordbook_prefix)




def generate_wordlist(type_):
    '''type_: 'learn'/'review': generate word list for learning/review.
    '''
    current_no = stat['current_no']
    part_count = stat['part_count']
    wordlist   = []

    if type_ == 'learn':
        if current_no < part_count:
            partlist = [current_no]
            wordbook[current_no].seek(0) # TODO Pr1: restore from break piont
            wordlist = [idx.strip() for idx in wordbook[current_no]]
        else:
            return []

    elif type_ == 'review':
        partlist = []
        for partno in range(part_count):
            # if partno is in current_no's review plan
            if (current_no in [partno + interval for interval in stat['review_day']]
               or (current_no - partno) % stat['longterm_interval'] == 0):
                  partlist.append(partno)
                  wordbook[partno].seek(0) # TODO Pr1
                  wordlist.extend([idx.strip() for idx in wordbook[partno]])

    else:
        raise ValueError, "Invalid type name: %s" % type_
    # end if #

    random.shuffle(wordlist)
    return wordlist, partlist
    # end def generate_wordlist #


def finish_learn():
    stat['have_learnt'] = True

def finish_review():
    stat['have_reviewed'] = True
    stat['current_no'] += 1
