# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:09:57 2015

@author: koehler
"""
from __future__ import unicode_literals


class NoteItem(object):
    def __init__(self, text='', **kwargs):
        self.head = {}
        self.foot = {}
        self.head['Beamer'] = ''
        self.foot['Beamer'] = '\n'
        self.kwargs = kwargs
        self.text = text
    def get_text(self, style='Beamer'):
        """
        Returns the ASCII tex string
        """
        text = ""
        text += self.head[style]
        if type(self.text) == dict:
            text += self.text[style]
        else:
            text += str(self.text)
        text += self.foot[style]
        return text
    def __str__(self):
        return ""
    def __call__(self, item, **kwargs):
        self.add_item(item, **kwargs)
        
class NoteContainer(NoteItem):
    """
    Base class for all TeX objects
    
    Args
    ----
    style : dict
        dict containing format tags
    """
    def __init__(self, **kwargs):
        super(NoteContainer, self).__init__(**kwargs)        
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



class List(NoteContainer):
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
        if item.strip()[:2] == "* ":
            item = item.strip()[2:]
        self.text = item

        
class Equation(NoteItem):
    """
    An Equation
    """
    def __init__(self, equation, **kwargs):
        super(Equation, self).__init__(**kwargs)        
        self.head['Beamer'] = '$$'
        self.foot['Beamer'] = '$$\n'
        equation = equation.strip().strip("$$")
        self.text = equation

        
class Figure(NoteItem):
    """
    A Figure
    """
    def __init__(self, figure, workdir, size=1, **kwargs):
        super(Figure, self).__init__(**kwargs)
        from os import path 
        self.head['Beamer'] = "\\includegraphics[width=%g\\textwidth]{"%(size)
        self.foot['Beamer'] = "}\n"

        if type(figure) == str:
            from shutil import copyfile
            fn_figure =  path.basename(figure)
            copyfile(figure, path.join(workdir,fn_figure))
        else:
            fn_figure = "dummy.pdf"
            figure.savefig(path.join(workdir,fn_figure))
        self.text = fn_figure


class Slide(NoteContainer):
    """
    One Slide of a Worknote
    
    """
    def __init__(self, title, **kwargs):
        super(Slide, self).__init__(**kwargs)
        self.head['Beamer'] = "\\frame{\\frametitle{%s}\n"%title
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
         'text' : NoteItem,
         'equation' : Equation,
         'list' : ListItem,
         'figure' : Figure,
         'figurepage': Figure}

def find_category(item):
    """
    Determines item category from item type and content
    
    Args
    ----
    item : arbitrary
        Arbirary valid item
    
    Returns
    -------
    cat : str
        The determined item category
    """
    import matplotlib
    from os import path
    if type(item) == str:
        if path.splitext(item)[1] in ['pdf', 'jpg', 'png', 'jpeg']:
            cat = 'figure'
        elif item.strip()[:2] == "$$" and item.strip()[-2:] == "$$":
            cat = 'equation'
        elif item.strip()[:2] == "* ":
            cat = 'list'
        else:
            cat = 'text'
    elif type(item) == matplotlib.figure.Figure:
        cat = 'figure'
    else:
        print "Category of item not recognized: %s"%type(item)
        cat = None
    return cat
        
class Worknote(NoteContainer):
    """
    Class That allows to drop comments in figures into a presentation while 
    interactively working with python
    """
    def __init__(self, workdir, title='', author='', **kwargs):
        super(Worknote, self).__init__(**kwargs)
        self.workdir = workdir
        self.head['Beamer'] = """
\\documentclass{beamer}
\\mode<presentation>
{
  \\usetheme{Boadilla}
  %\\usetheme{Pittsburgh}
  %\\setbeamercovered{transparent}
}        
\\setbeamertemplate{footline}[frame number]
\\setbeamertemplate{navigation symbols}{}
\\usepackage[english]{babel}
\\usepackage[utf8]{inputenc}
\\begin{document}
        """
        self.foot['Beamer'] = "\\end{document}"
        

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
            cat = find_category(item)
            if cat == None:
                print "Item not added"
                return
        item = TYPES[cat](item, workdir=self.workdir, **kwargs)
        if cat == 'slide':
            self.items.append(item)
        elif cat == 'figurepage':
            self.items.append(Slide(""))
            self.items[-1].add_item(item)
        else:
            self.items[-1].add_item(item)
    def __call__(self, item, cat=None, **kwargs):
        self.add_item(item, cat, **kwargs)            
            
    def build_pdf(self, filename):
        import codecs
        f_out = codecs.open(filename+".tex", 'w', encoding='utf-8') 
        f_out.write(self.get_text())
        f_out.close()       
        print "Building pdf"
        from subprocess import call
        call(["pdflatex", '-output-directory='+self.workdir, filename+".tex"])


        
        
        
        