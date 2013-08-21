#!/usr/bin/env python
# Filename: word.sh
# Author:   LIU Yang
# Create Time: Sat Aug 17 15:57:50 HKT 2013
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
# Last change: 2013-08-17 15:59:40
# Brief: Definition of word in my vocabulary book.

class NameConflictError(ValueError):
    "Indicate a reassignment to a word which has had a name"

class word:
    """ A word in vocabulary book """

    def __init__(self, name, *meanings):
        self.name     = name
        self.meanings = list(meanings)
        self.priority = 0 # Frequency of showing up. 0 is lowest
        self.partno   = 0 # Part NO. It's used for the Scheduler.

    def __add__(self, other):
        if self.name == None and other.name != None:
            name = other.name
        elif other.name != None:
            raise NameConflictError, "Err: Name conflict: %s v.s. %s" % (self.name, other.name)
        else:
            name = self.name

        means = self.meanings
        means.extend(other.meanings)
        return word(name, *means)

    def __str__(self):
        s = self.name + '\n'
        s += self.getmean()
        return s

    def getmean(self):
        s = ''
        for mean in self.meanings:
            s += '\r  ' + str(mean) + '\n'
        return s
