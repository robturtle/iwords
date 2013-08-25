#!/usr/bin/env python
# Filename: learn_interface.sh
# Author:   LIU Yang
# Create Time: Mon Aug 19 22:18:21 HKT 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com

from random    import shuffle
from threading import Thread
from Queue     import Queue, Empty
from time      import sleep

import os, sys

import word
import wordlist
from getch  import qgetch, stop_qgetch_str

# word counts of round #? in words
r1_wcount = 10
r2_wcount = 60
r3_wcount = 'all'

# time pariod of round #? in minutes
r1_time = 5
r2_time = 30
r3_time = 720 # sleep as daemon until time's up

# time per word in seconds
learn_time = 30
review_time = 10

do_exit = False



def study(mode, DB, wlist):
    if mode == 'learn':
        learn(DB, wlist)
    else:
        review(DB, wlist)



def learn(DB, wlist):
    wsum = len(wlist)

    ## r2 cycle
    no     = 0 # index of wlist
    r2_count = (wsum / r2_wcount + 1
      if wsum % r2_wcount != 0 else wsum + r2_wcount)

    for i in range(r2_count):
        r2_wlist = (wlist[no:no+r2_wcount]
          if no+r2_wcount < wsum else wlist[no:])
        no += len(r2_wlist)

        ## r1 cycle
        r2_sum = len(r2_wlist)
        r1_no = 0
        r1_count = (r2_sum / r1_wcount + 1
          if r2_sum % r1_wcount != 0 else r2_sum / r1_wcount)

        for j in range(r1_count):
            r1_wlist = (r2_wlist[r1_no:r1_no+r1_wcount]
              if r1_no+r1_wcount < len(r2_wlist) else r2_wlist[r1_no:])
            r1_no += len(r1_wlist)

            shuffle(r1_wlist)
            print '\n\n\rCycle 1, NO. {0}'.format(j)
            for windex in r1_wlist:
                study_word(DB, windex, learn_time)
                if do_exit: return

        ## review r2 words
        shuffle(r2_wlist)
        print '\n\n\rCycle 2, NO. {0}'.format(i)
        for windex in r2_wlist:
            study_word(DB, windex, review_time)
            if do_exit: return
        # end of round 2 cycle #

    wordlist.finish_learn()
    wordlist.writestat()
    # TODO then sleep as daemon until the time for round 3 #
    # then wake up and send a notification #

def review(DB, wlist):
    shuffle(wlist)
    for windex in wlist:
        study_word(DB, windex, review_time)
        if do_exit: return
    wordlist.finish_review()
    wordlist.writestat()


study_prompt = '\r(<Space>: show meanings, <Enter>: next word) {0:3}: '
prompt_mask = '\r' + ' ' * len(study_prompt)

def study_word(DB, windex, tick):
    global do_exit
    # need display word's meaning?
    failtime = 5 if tick > 5 else 1
    show_mean = False

    w = DB[windex]
    print '\n\n\r' + w.name

    # Key press event handler
    queue = Queue()
    stop_keys  = ['\n', '\r', os.linesep, 'q']
    valid_keys = stop_keys + [' ']
    keywatcher = Thread(target=qgetch, args=(queue, valid_keys, stop_keys))
    keywatcher.start()

    while True:
        try:
            ch = queue.get_nowait()
        except Empty:
            ch = ''

        if tick < 0 or ch in ['\n', '\r', os.linesep]:
            keywatcher.join() # NOTE This will block the process until you press stop_keys
            return
        elif ch == 'q': # Terminate the whole process
            keywatcher.join()
            do_exit = True
            return
        # TODO elif ch == 'p': pronounce
        elif (tick <= failtime or ch == ' ') and show_mean == False:
            # indicate learner not familiar with this word
            show_mean = True
            w.priority += 1
            DB[windex] = w # invoker is responsible to store DB
            print prompt_mask,
            print w.getmean()
            print study_prompt.format(tick),
        else:
            print study_prompt.format(tick),

        sys.stdout.flush()
        tick -= 1
        sleep(1)

if __name__ == '__main__':
    import shelve
    DB = shelve.open('words.dat')
    wlist = [str(i+1) for i in range(150)]
    time = 20
    #study_word(DB, '1', time)
    #study_word(DB, '2', time)
    #study_word(DB, '3', time)
    #learn(DB, wlist)
    #review(DB, wlist)
