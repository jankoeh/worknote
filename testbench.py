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
wn("First slide title", cat='slide')
wn("The Problem we want to solve:", cat='text')
wn("f=\sqrt{x}", cat='equation')
# do some python work ...
from pylab import *
plot(sqrt(arange(10)))
wn("Slide with figure on it", cat='slide')
wn(gcf(), cat='figure', size=0.8)
wn("Slide with a list on it", cat='slide')
wn('some ist item', cat='list')
wn('  * implicit list declaration via "* "')
wn("implicit declaration of text")
#implicit declaration of a table
wn([['First column','Second Column', 'Third Column'],[1.,2.,3.],[4,5,6]])
wn.build_pdf()   #build function to be implemented , see ./test/beamer.tex
wn1_output = wn.get_text()
wn.save()

wn2 = Worknote('./test')
wn2.load()
wn2_output = wn.get_text()
if wn1_output == wn2_output:
    print 'Saving and loading successful.'
else:
    print 'ERROR: There were differences in the saved and loaded data'
