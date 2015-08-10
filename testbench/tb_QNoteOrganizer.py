# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 13:14:49 2015

@author: koehler
"""
from worknote import Worknote
try:
    from worknote.QNoteOrganizer import edit_note
except ImportError:
    print "This testbench needs to be executed from outside this module"
    print "Copy this file to a higher level and execute"
    import sys
    sys.exit()
wn = Worknote("./test")
wn("First slide ", cat='slide')
wn(" A lot of Text")
wn("*  bbb")
wn("*  Some text")
wn("*  bbb")
wn("Second slide ", cat='slide')
wn("# enumerated")
wn("bla")
wn("Third slide", cat='slide')
wn([['First column','Second Column', 'Third Column'],[1.,2.,3.],[4,5,6]], cat='table')
edit_note(wn)
wn.build()
