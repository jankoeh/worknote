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
    def __init__(self, figure, workdir, size=1, gfxfmt = 'pdf', **kwargs):
        super(Figure, self).__init__(**kwargs)
        from os import path, listdir
        self.head['Beamer'] = "\\includegraphics[width=%g\\textwidth]{"%(size)
        self.foot['Beamer'] = "}\n"
        
        files = listdir(workdir)
        non_fig_files = [workdir + '.worknote']
        for filename in non_fig_files:
            if filename in files:
                files.remove(filename)
        #We do len + 1 here to avoid having the files starting with fig0
        fn_figure = 'fig' + str(len(files) + 1)

        if type(figure) == str:
            from shutil import copyfile
            fn_figure += '.' + path.splitext(path.basename(figure))[1]
            copyfile(figure, path.join(workdir,fn_figure))
        else:
            fn_figure += '.' + gfxfmt
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
    def __init__(self, workdir = None, title='', author='', **kwargs):
        super(Worknote, self).__init__(**kwargs)
        self.set_workdir(workdir)
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
            if cat in ['figure', 'figurepage'] and self.workdir is None:
                print 'Cannot add figure until working directory is set'
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
        
    def set_workdir(self, workdir):
        """
        Set the working directory
        
        Args
        ----
        workdir : str
            Path of the working directory to use. If the last directory does
            not exist, it will be created.
        """
        from os.path import exists
        if not workdir is None:
            self.workdir = workdir
            if not exists(self.workdir):
                from os import mkdir
                try:
                    mkdir(self.workdir)
                except OSError:
                    print "ERROR: Unable to create working directory"
        else:
            print 'WARNING: No working directory set'
            print '\tUnable to save or add figures'
            self.workdir = None
            
    def save(self):
        """
        Save the worknotes to the working directory
        """
        import cPickle
        from os.path import join
        with open(join(self.workdir,
                       self.workdir + '.worknote'), 'wb') as outfile:
            cPickle.dump(self.head, outfile, cPickle.HIGHEST_PROTOCOL)
            cPickle.dump(self.foot, outfile, cPickle.HIGHEST_PROTOCOL)
            cPickle.dump(self.items, outfile, cPickle.HIGHEST_PROTOCOL)
    
    def load(self, workdir = None):
        """
        Load the worknotes from a working directory
        """
        import cPickle
        from os.path import join
        if self.workdir is None:
            if workdir is None:
                from os import OSError
                raise OSError('No working directory given')
                return
            self.set_workdir(workdir)
        with open(join(self.workdir,
                       self.workdir + '.worknote'), 'rb') as infile:
            self.head = cPickle.load(infile)
            self.foot = cPickle.load(infile)
            self.items = cPickle.load(infile)
