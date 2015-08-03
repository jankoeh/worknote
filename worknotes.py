# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:09:57 2015

@author: koehler
"""
from __future__ import unicode_literals


class NoteItem(object):
    def __init__(self, data='', **kwargs):
        self.kwargs = kwargs
        self.data = self.clean_data(data)
    def get_text(self, style='Beamer'):
        """
        Returns the ASCII tex string
        """
        return self.data
    def clean_data(self, data):
        """
        Remove any style specific marks from data
        """
        return data
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
        self.head = {'default' : ''}
        self.foot = {'default' : ''}
        self.items = []

    def get_text(self, style='Beamer'):
        """
        Returns the ASCII tex string
        """
        if style not in self.head:
            style = 'default'
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
    def clean_data(self, data):
        if data.strip()[:2] == "* ":
            data = data.strip()[2:] 
        return data
    def get_text(self, style):
        if style in ['Beamer', 'LaTeX']:
            return "\\item {} \n".format(self.data)
        elif style in ["Markdown"]:
            return "  * {} \n".format(self.data)
        else:
            print "Defaulting to Markdown"
            return "  * {} \n".format(self.data)

        
class Equation(NoteItem):
    """
    An Equation
    """
    def clean_data(self, data):
        data =  data.strip().strip("$$")
        return data
    def get_text(self, style):
        if style in ['Beamer', 'LaTeX']:
            return "$$ {} $$".format(self.data)
        else:
            return "$$ {} $$".format(self.data)
            


        
class Figure(NoteItem):
    """
    A Figure
    """
    def __init__(self, data, workdir, size=1, gfxfmt='pdf', align='center', **kwargs):
        self.workdir = workdir
        self.size = size
        self.gfxfmt = gfxfmt
	self.align = align
        super(Figure, self).__init__(data, **kwargs)
    def clean_data(self, data):
        from os import path
        from glob import glob
        files = glob(path.join(self.workdir, 'fig[0-9]*'))
        #We do len + 1 here to avoid having the files starting with fig0
        fn_figure = 'fig' + str(len(files) + 1)
        if type(data) == str:
            from shutil import copyfile
            fn_figure += '.' + path.splitext(path.basename(data))[1]
            copyfile(data, path.join(self.workdir,fn_figure))
        else:
            fn_figure += '.' + self.gfxfmt
            data.savefig(path.join(self.workdir,fn_figure))
        return fn_figure
    def get_text(self, style):
        if style in ['Beamer', 'LaTeX']:
            text = "\\includegraphics[width=%g\\textwidth]{%s}\n"%(self.size, self.data)
            if self.align:
                text = "\\begin{%s}\n %s \\end{%s}"%(self.align, text, self.align)
            return text
        else:
            self.data

class Table(NoteItem):
    """
    Pass a list (of lists) or a numpy 2D array as argument
    """
    def get_text(self, style):
        if style in ['Beamer', 'LaTeX']:
            data = self.data
            table = "\\begin{center}\n\\begin{tabular}{%s}\n \\hline\n"%('c'*len(data[0]))
            if type(data[0][0]) == str:
                table  += "&".join([str(i) for i in data[0]]) + "\\\\ \n \hline "
                data = data[1:]
            for line in data:
                table  += "&".join([str(i) for i in line]) + "\\\\ \n"
            table +="\\hline \\hline\n \\end{tabular}\n\\end{center}\n"
            return table
        else:
            return str(self.data)

class Slide(NoteContainer):
    """
    One Slide of a Worknote
    
    """
    def __init__(self, title, **kwargs):
        super(Slide, self).__init__(**kwargs)
        title = self.clean_data(title)
        self.head['Beamer'] = "\\frame{\\frametitle{%s}\n"%title
        self.foot['Beamer'] = '}\n'
        self.head['Markdown'] = "{}\n".format(title) + "-"*len(title)+"\n"
        self.foot['Markdown'] = "\n"
    def clean_data(self, title):
        if len(title.split("\n"))==2 and \
             len(title.split("\n")[1])>=3 and \
             title.split("\n")[1][:3] == '---':
            title = title.split("\n")[0]
        return title
        
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
         'figurepage': Figure,
         'table' : Table}

def find_category(item):
    """
    Determines item category from item type and content
    
    Args
    ----
    item : arbitrary
        Arbitrary valid item
    
    Returns
    -------
    cat : str
        The determined item category
    """
    import numpy
    import matplotlib
    from os import path
    if type(item) == str:
        if path.splitext(item)[1] in ['.pdf', '.jpg', '.png', '.jpeg']:
            cat = 'figure'
        elif item.strip()[:2] == "$$" and item.strip()[-2:] == "$$":
            cat = 'equation'
        elif item.strip()[:2] == "* ":
            cat = 'list'
        elif len(item.split("\n"))==2 and \
             len(item.split("\n")[1])>=3 and \
             item.split("\n")[1][:3] == '---':
            cat = 'slide'
        else:
            cat = 'text'
    elif type(item) == matplotlib.figure.Figure:
        cat = 'figure'
    elif type(item) == list or type(item) == numpy.ndarray:
        cat = 'table'
    else:
        print "Category of item not recognized: %s"%type(item)
        cat = None
    return cat
        
class Worknote(NoteContainer):
    """
    Class That allows to drop comments in figures into a presentation while 
    interactively working with python
    
    Args
    ----
    workdir : str
        represents project name and  working directory that will be created
    title : str
        Title of document
    author : str
        Author name           
    """
    def __init__(self, workdir = None, title='', author='', date = '',
                 **kwargs):
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
        self.metadata = {}
        self.metadata['title'] = title
        self.metadata['author'] = author
        self.metadata['date'] = date            

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
            
    def build_pdf(self, style='Beamer'):
        from os import path
        import codecs
        f_out = codecs.open(path.join(self.workdir, style+".tex"), 'w', 
                            encoding='utf-8') 
        f_out.write(self.get_text(style=style))
        f_out.close()       
        print "Building pdf"
        from subprocess import call
        build = call(["pdflatex", style+".tex"], cwd=self.workdir)
        if build==0:
            print "Building sucessful: %s"%path.join(self.workdir, style+".pdf")
        else:
            print "Errors encountered during build"
            print "Check %s for problems"%path.join(self.workdir, style+".tex")
        
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
            cPickle.dump(self.metadata, outfile, cPickle.HIGHEST_PROTOCOL)
    
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
            self.metadata = cPickle.load(infile)

def value(var, verbosity = 0):
    #I have an idea of how this should work, for now it is a placeholder bc 
    #it's late today
    return str(var)
