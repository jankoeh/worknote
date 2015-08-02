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
wn1_output = wn.get_text()
print wn1_output
print
wn.save()
wn2 = Worknote('./test')
wn2.load()
wn2_output = wn.get_text()
if wn1_output == wn2_output:
    print 'Saving and loading successful.'
else:
    print 'ERROR: There were differences in the saved and loaded data'
