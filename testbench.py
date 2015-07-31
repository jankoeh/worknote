# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 13:55:18 2015

@author: koehler
"""

from worknotes import Worknote
wn = Worknote("./")
wn("test", cat='slide')
wn("test text", cat='text')
wn("Slide2", cat='slide')
print wn.get_tex()

