# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 13:55:18 2015

@author: koehler
"""

from pylab import *

fig = figure("")
plot(arange(10))

from worknotes import Worknote
wn = Worknote("./test")
wn("test", cat='slide')
wn("test text", cat='text')
wn("x=\sqrt{4}", cat='equation')
wn("$$ x\cdot2 $$")
wn("Slide2", cat='slide')
wn("item1", cat='list')
wn("item2", cat='list')
wn("Die Figure", cat='slide')
wn(fig)
wn('  * item 3')
wn(fig, cat='figurepage')
print wn.get_text()
print
wn.save()
wn2 = Worknote('./test')
wn2.load()
print wn.get_text()
