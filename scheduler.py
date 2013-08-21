#!/usr/bin/env python
# Filename: scheduler.sh
# Author:   LIU Yang
# Create Time: Sun Aug 18 23:09:55 HKT 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
# Brief: Make the vocabulary review schedule interactively

import shelve, cPickle
import json
from config import DB_name, wordbook_prefix, statfile

worddb = shelve.open(DB_name, 'w', writeback=True)
word_count = len(worddb.keys())

def ask_choice(prompt, *valid_answers):
	while True:
		print prompt
		answer = raw_input()
		if answer in valid_answers:
			return answer
		else:
			print '''Valid answers are:
%s
please try again!
			''' % str(valid_answers)

planmap = {'1':150, '2':300, '3':600}
select_plan = """How many new words do you want to study per day?
1 => 150 words (If you got 2 Hours/day)
2 => 300 words (If you got 4 Hours/day)
3 => 600 words (If you've paid for the tofel exam in the next 2 week)

Press number(1-3) to confirm [3 for default]:
"""
plan = ask_choice(select_plan, '1', '2', '3')
words_per_day = planmap[plan]
day_count = word_count / words_per_day + 1


print 'Generating schedule, this may take a while, please be patient...'

# Split in parts
word_in_parts = [[] for i in range(day_count)]
partno = 0
counter = 0

fname = wordbook_prefix + str(partno)
outfile = file(fname, 'w+')
for index in worddb:
	worddb[index].partno = partno # assign part NO.
	outfile.write(index + '\n')   # cache in file

	if counter < words_per_day:
		counter += 1
	else:
		outfile.close()
		counter = 0
		partno += 1
		fname = wordbook_prefix + str(partno)
		outfile = file(fname, 'w+')


# Learn & Review scheduling
review_day = [0, 1, 3, 7, 14, 29] # The Nth. day of review
longterm_interval = 30  # Review interval after process above

schedule = file(statfile, 'w+')
schedule_stat = {
  'part_count'        : day_count,
  'current_no'        : 0,
  'have_learnt'       : False,
  'have_reviewed'     : False,
  'review_day'        : review_day,
  'longterm_interval' : longterm_interval,}

schedule.write(json.dumps(schedule_stat, indent=4))
schedule.close()

worddb.close()
