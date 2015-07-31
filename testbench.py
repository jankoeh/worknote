# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 13:55:18 2015

@author: koehler
"""

from worknotes import Worknote
wn = Worknote("./")
wn("test", cat='slide')
wn("test text", cat='text')
wn("x=\sqrt{4}", cat='equation')
wn("Slide2", cat='slide')
wn("item1", cat='list')
wn("item1", cat='list')

print wn.get_text()

