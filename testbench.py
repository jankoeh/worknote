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
wn("The Problem we want to slove:", cat='text')
wn("f=\sqrt{x}", cat='equation')
# do some python work ...
from pylab import *
plot(sqrt(arange(10)))
wn("Slide with figure on it", cat='slide')
wn(gcf(), cat='figure')
wn("Slide with a list on it", cat='slide')
wn('some ist item', cat='list')
wn('  * implicit list declarationvia "* "')
wn("implicit declaration of text")
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
