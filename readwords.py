#!/usr/bin/env python
# Filename: readwords.sh
# Author:   LIU Yang
# Create Time: Sat Aug 17 20:15:44 HKT 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com

import fileinput, shelve
import re, sys
import config, word

wordbook = dict()
partkeys = ['n.', 'v.', 'vt.', 'vi.', 'adj.', 'adv.', 'prep.', 'IDIOM',
		    'n',  'v',  'vt',  'vi',  'adj',  'adv',  'prep',]

def match_pattern(items, patterns):
	if items[2] in patterns: # First meaning of word
		#       index     word name     meaning
		return [items[0], items[1], ' '.join(items[2:])]
	elif items[1] in patterns: # Rest meanings of word
		#       index     word name     meaning
		return [items[0], None, ' '.join(items[1:])]
	else:
		return []



def get_combine(items, joiner):
	return [joiner.join([lkey, rkey])
	  for lkey in partkeys
	  for rkey in partkeys]



def match_idiom(items, patterns):
    # Note that there may be some space separated word
	for idx, item in enumerate(items):
		if item in patterns:
            #       index     word name     meaning
			return [items[0], ' '.join(items[1:idx]), ' '.join(items[idx:])]
	return []



for line in fileinput.input():

	items = line.split()

	# pattern like 'adj./v.'
	combine = get_combine(items, '/')

    # split index, word name and meaning

	res = match_pattern(items, combine)
	if res == []:
        # single key
		res = match_pattern(items, partkeys)

	if res == []:
		res = match_idiom(items, combine)

	if res == []:
		res = match_idiom(items, partkeys)

	if res == []:
		sys.stderr.write('ERR: partkey not found in line: %s' % line)

    # do cache
	index, wname, mean = res
	if wordbook.has_key(index):
		wordbook[index] = wordbook[index] + word.word(wname, mean)
	else:
		wordbook[index] = word.word(wname, mean)
	# End reading from file #

# store into database
word_db = shelve.open(config.DB_name)
for idx in wordbook:
	word_db[idx] = wordbook[idx]
word_db.close()

if __name__ == '__main__':
	db_in = shelve.open(config.DB_name)
	for idx in db_in.keys():
		print db_in[idx]
	db_in.close()
