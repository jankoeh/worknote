# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 13:14:49 2015

@author: koehler
"""

from worknotes import Worknote
from QNoteOrganizer import edit_note

wn = Worknote('./test')
wn("First slide ", cat='slide')
wn("Text")
wn("*  bbb")
wn("Second slide ", cat='slide')
wn("# enumerated")
wn("bla")
edit_note(wn)