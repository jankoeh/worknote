# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:09:57 2015

@author: koehler
"""
from __future__ import unicode_literals


class NoteItem(object):
    """
    Base class for all TeX objects
    
    Args
    ----
    style : dict
        dict containing format tags
    """
    def __init__(self, **kwargs):
        self.head = {}
        self.foot = {}
        self.head['TeX'] = ''
        self.foot['TeX'] = '\n'
        self.kwargs = kwargs
        self.items = []
    def get_tex(self, style='TeX'):
        """
        Returns the ASCII tex string
        """
        text = ""
        text += self.head[style]
        for item in self.items:
            text += item.get_tex()
        text += self.foot[style]
        return text
        
    def add_item(self, item, **kwargs):
        """
        Adds an item to the items list
        
        Args
        ----
        item : NoteItem
            subitem to add to
        **kwargs : keyowrd arguments
            Args like figsize etc            
        """
        self.items.append(item)   
    def __str__(self):
        return ""
    def __call__(self, item, **kwargs):
        self.add_item(item, **kwargs)


class Text(NoteItem):
    """
    One Slide of a Worknote
    
    """
    def __init__(self, text, **kwargs):
        super(Text, self).__init__(**kwargs)
        self.text = text
    def get_tex(self, style='TeX'):
        return self.text

class Slide(NoteItem):
    """
    One Slide of a Worknote
    
    """
    def __init__(self, title, **kwargs):
        super(Slide, self).__init__(**kwargs)
        self.head['TeX'] = r"\frame{\frametitle{%s)}\n"%title
        self.foot['TeX'] = r'}\n'

TYPES = {'slide' : Slide,
         'text' : Text}

        
class Worknote(NoteItem):
    """
    Class That allows to drop comments in figures into a presentation while 
    interactively working with python
    """
    def __init__(self, workdir, title='', author='', **kwargs):
        super(Worknote, self).__init__(**kwargs)
        self.workdir = workdir
        self.head['TeX'] = "beginnning of doc inc author and title"
        self.foot['TeX'] = "end of document"
        

    def add_item(self, item, cat=None, **kwargs):
        """
        Adds an item to the last slide
        
        Args
        ----
        items : various
            item to add to slide, can be str, fig, ...
        cat : str
            Category of item. If none is given, it will be determined 
            through the type function
        **kwargs : keyowrd arguments
            Args like figsize etc
        """
        if cat == None:
            if type(item) == str:
                cat = 'text'
        item = TYPES[cat](item, **kwargs)
        if cat == 'slide':
            self.items.append(item)
        else:
            self.items[-1].add_item(item)
            
            
    def build_pdf(self, filename):
        import codecs
        f_out = codecs.open(filename+".tex", 'w', encoding='utf-8') 
        f_out.write(self.get_tex('lehrer'))
        f_out.close()       
        print "Building pdf"
        from subprocess import call
        call(["pdflatex", '-output-directory='+self.workdir, filename+".tex"])


        
        
        
        