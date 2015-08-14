# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 13:55:18 2015

@author: koehler
"""

from pylab import *

fig = figure(figsize=(8,6))
plot(arange(10))

from worknote import Worknote
wn = Worknote("./test", load_if_used = False)
wn.set_metadata(title = 'Worknotes', author = 'John Doe', 
                date = '\\today', subtitle="The story of an awesome toolkit")
wn("First slide title with unicode", cat='slide')
wn("The Problem we want to solve:", cat='text')
wn("f=\sqrt{x}", cat='equation')
# do some python work ...
plot(sqrt(arange(10)))
xlabel("fluor/MeV")
ylabel("Intensity g s/Liter")
wn("Slide implicite generation\n------------------")
wn(gcf(), cat='figure', size=.8)
wn("Slide with a list on it", cat='slide')
wn('some list item', cat='list')
wn('  * implicit list declaration via "* "')
wn("implicit declaration of text")
#implicit declaration of a table
wn([['First column','Second Column', 'Third Column'],[1.,2.,3.],[4,5,6]])
wn("Demonstrating value functionality", cat='slide')
wn(pi, desc = 'Value of pi')
wn(pi, precision = 5, desc = 'More precise value of pi')
wn('We can also automatically handle values smaller than the precision...\n')
wn(pi/1e8, desc = 'A really small value')
wn('... as well as units:\n')
wn(9.81, desc = 'Earth gravity acceleration', units = 'm/s^2', precision = 2)
wn('And errors:\n')
wn(pi, precision = 2, error = pi/10)
wn('And we break automatically after a text line...\n And continue ...')
wn("Demonstrating enumerated lists", cat='slide')
wn("My first point", cat='enumerate')
wn("  # My second point")
wn("# My third point")
for i in [15, 18, 23, 34]:
    wn("Test table sizes - %d lines"%i, cat='slide')
    wn([['zahlen']+range(10)]*i, size='auto')
wn('Source code printing demonstration', cat = 'slide')
wn('''def set_unicode(text):
    """
    Return unicode string

    Args:
    -----
    text : str, unicode
        Text can be string or unicode

    Returns
    -------
    text : unicode
    """
    if type(text) == str:
        text = unicode(text, 'utf-8')
    return text''', cat = 'code')
wn.build()   #build function to be implemented , see ./test/beamer.tex
wn.build(style='Report')
wn.build(style='Markdown')
wn1_output = wn.get_text()
wn.save()
wn2 = Worknote()
wn2.load('./test')
wn2_output = wn.get_text()
if wn1_output == wn2_output:
    print 'Saving and loading successful.'
else:
    print 'ERROR: There were differences in the saved and loaded data'
    
print unicode(wn)
