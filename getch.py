#!/usr/bin/env python
# Filename: getch.sh
# Author:   Danny Yoo

from Queue import Empty

class _Getch:
    '''Gets a single character from standard input. Does not echo to the screen.'''
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

stop_qgetch_str = 'terminate key watch'
def qgetch(queue, valid_keys, stop_keys):
    while True:
        ch = getch()
        if ch in valid_keys:
            queue.put(ch)
        if ch in stop_keys:
            return
