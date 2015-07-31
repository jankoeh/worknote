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
        self.head['Beamer'] = ''
        self.foot['Beamer'] = '\n'
        self.kwargs = kwargs
        self.items = []
    def get_text(self, style='Beamer'):
        """
        Returns the ASCII tex string
        """
        text = ""
        text += self.head[style]
        for item in self.items:
            text += item.get_text(style)
        text += self.foot[style]
        return text
        
    def add_item(self, item):
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


class List(NoteItem):
    """
    The List environment
    """
    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)        
        self.head['Beamer'] = '\\begin{itemize}\n'
        self.foot['Beamer'] = '\\end{itemize}\n'

class ListItem(NoteItem):
    def __init__(self, item, **kwargs):  
        super(ListItem, self).__init__(**kwargs)
        self.head['Beamer'] = '\\item '
        self.foot['Beamer'] = '\n'        
        self.item = item
    def get_text(self, style='Beamer'):
        text = ""
        text += self.head[style]
        text += self.item
        text += self.foot[style]
        return text
        
class Equation(NoteItem):
    """
    An Equation
    """
    def __init__(self, equation, **kwargs):
        super(Equation, self).__init__(**kwargs)        
        self.head['Beamer'] = '$$'
        self.foot['Beamer'] = '$$\n'
        self.equation = equation
    def get_text(self, style='Beamer'):
        text = ""
        text += self.head[style]
        text += self.equation
        text += self.foot[style]
        return text
        
class Text(NoteItem):
    """
    Simple Text
    
    """
    def __init__(self, text, **kwargs):
        super(Text, self).__init__(**kwargs)
        self.text = text
    def get_text(self, style='Beamer'):
        return self.text

class Slide(NoteItem):
    """
    One Slide of a Worknote
    
    """
    def __init__(self, title, **kwargs):
        super(Slide, self).__init__(**kwargs)
        self.head['Beamer'] = "\\frame{\\frametitle{%s)}\n"%title
        self.foot['Beamer'] = '}\n'
        
    def add_item(self, item, **kwargs):
        """
        Adds an item to slide
        """
        if type(item) == ListItem:
            if len(self.items)==0 or type(self.items[-1]) != List:
                self.items.append(List(**kwargs))
            self.items[-1].add_item(item)
        else:
            self.items.append(item)
        

TYPES = {'slide' : Slide,
         'text' : Text,
         'equation' : Equation,
         'list' : ListItem}

        
class Worknote(NoteItem):
    """
    Class That allows to drop comments in figures into a presentation while 
    interactively working with python
    """
    def __init__(self, workdir, title='', author='', **kwargs):
        super(Worknote, self).__init__(**kwargs)
        self.workdir = workdir
        self.head['Beamer'] = "beginnning of doc inc author and title\n"
        self.foot['Beamer'] = "end of document"
        

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
        f_out.write(self.get_text())
        f_out.close()       
        print "Building pdf"
        from subprocess import call
        call(["pdflatex", '-output-directory='+self.workdir, filename+".tex"])


        
        
        
        