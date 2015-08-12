# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:09:57 2015

@author: koehler
"""
from __future__ import unicode_literals
import items

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
    try:
        from matplotlib.figure import Figure as MPL_Figure
    except ImportError:
        MPL_Figure = None
    from os import path
    if type(item) in [str, unicode]:
        if path.splitext(item)[1] in ['.pdf', '.jpg', '.png', '.jpeg']:
            cat = 'figure'
        elif item.strip()[:2] == "$$" and item.strip()[-2:] == "$$":
            cat = 'equation'
        elif item.strip()[:2] == "* ":
            cat = 'list'
        elif item.strip()[:2] == "# ":
            cat = 'enumerate'
        elif len(item.split("\n")) == 2 and \
            len(item.split("\n")[1]) >= 3 and \
            item.split("\n")[1][:3] == '---':
            cat = 'slide'
        else:
            cat = 'text'
    elif type(item) == MPL_Figure and MPL_Figure != None:
        cat = 'figure'
    elif type(item) == list or type(item) == numpy.ndarray:
        cat = 'table'
    elif type(item) in [float, numpy.float64, int, numpy.int64]:
        cat = 'value'
    else:
        cat = None
        raise TypeError("Category of item not recognized: %s"%type(item))
    return cat

class Worknote(items.NoteContainer):
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
    date : str
        Date of document
    subtitle : str
        Document subtitle
    """
    def __init__(self, workdir=None, title='', author='', date='',
                 subtitle='', **kwargs):
        super(Worknote, self).__init__(**kwargs)
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
%%%METADATA%%%
\\begin{document}
%%%TITLEPAGE%%%
        """
        self.foot['Beamer'] = "\\end{document}"
        self.head['Report'] = """
\\documentclass{article}
\\usepackage[english]{babel}
\\usepackage[utf8]{inputenc}
\\usepackage{graphicx}
\\usepackage{a4wide}
\\usepackage{color}
%%%METADATA%%%
\\begin{document}
%%%TITLEPAGE%%%
        """
        self.foot['Report'] = "\\end{document}"
        self.head['Markdown'] = '%%%METADATA%%%'
        self.foot['Markdown'] = ''
        self.metadata = Metadata()
        self.set_metadata(title, author, date, subtitle)
        if 'load_if_used' in kwargs:
            load_if_used = kwargs.pop('load_if_used')
        else:
            load_if_used = True
        self.set_workdir(workdir, load_if_used=load_if_used)

    def add_item(self, item, index=[], **kwargs):
        """
        Insert the item at the given index.
        
        Args
        ----
        index : list
            A valid index assignment
        item : NoteItem
            A valid NoteItem (or subclass) object
        """
        if type(item) == items.Slide:
            super(Worknote, self).add_item(item, index=index)
        else:
            self[index[0:1]].add_item(item, index=index[1:])


    def __call__(self, item, cat=None, index=[], **kwargs):
        """
        Adds an item to the last slide

        Args
        ----
        items : various
            item to add to slide, can be str, fig, ...
        cat : str
            Category of item. If none is given, it will be determined
            through the type function
        index : int or str or iterable or []
            Index must be either an integer index, an iterable list of integer
            indices or an index notation of the style 'i:j:k' where indices are
            separated by colons. If index an empty list, the item will be 
            appended to the last element.
        **kwargs : keyword arguments
            Args like figsize etc
        """
        if cat == None:
            cat = find_category(item)
        if cat in ['figure', 'figurepage'] and self.workdir is None:
            print 'Cannot add figure until working directory is set'
            return
        item = items.TYPES[cat](item, workdir=self.workdir, **kwargs)
        index = items.parse_index(index)
        if cat == 'figurepage':
            item = items.Slide("").add_item(item)
            index = index[0:1]
        elif cat == 'slide':
            index = index[0:1]
        self.add_item(item, index)

    def build(self, style='Beamer'):
        """
        Generate output in a given style
        Argument style is currently unused and default Beamer

        Args
        ----
        style : str
            Build format (default = 'Beamer'). Options are:
              * 'Beamer' - Build Beamer.tex  and generate Beamer.pdf
              * 'Beamer.tex' - Build Beamer.tex
              * 'Report' - Build Report.pdf
              * 'Report.tex' - Build Report.tex
              * 'Markdown' - Build Report.md
              * More to come!
        """
        from os import path
        import codecs
        build_pdf = True
        if style[-4:] == '.tex':
            build_pdf = False
            style = style[:-4]
        if style in ['Beamer', 'Report']:
            f_out = codecs.open(path.join(self.workdir, style+".tex"), 'w',
                                encoding='utf-8')
        elif style in ['Markdown']:
            f_out = codecs.open(path.join(self.workdir, "Report.md"), 'w',
                                encoding='utf-8')
            build_pdf = False
        f_out.write(self.get_text(style=style))
        f_out.close()
        if build_pdf:
            print "Building pdf"
            from subprocess import call
            import os
            FNULL = open(os.devnull, 'w')
            build = call(["pdflatex", style+".tex"], 
                         cwd=self.workdir, 
                         stdout=FNULL)
            if build == 0:
                print "Building sucessful: %s"%path.join(self.workdir, style+".pdf")
            else:
                print "Errors encountered during build"
                print "Check %s for problems"%path.join(self.workdir, style+".tex")

    def build_pdf(self, style='Beamer'):
        """
        Generate output in a given style
        Argument style is currently unused and default Beamer
        """
        print "Deprecated! Use build() instead of build_pdf()"
        self.build(style)

    def set_workdir(self, workdir, load_if_used=False):
        """
        Set the working directory. If load_if_used is True or there are no
        items in the current notes, any worknotes present in the directory will
        automatically be loaded.

        Args
        ----
        workdir : str
            Path of the working directory to use. If the last directory does
            not exist, it will be created.
        """
        from os.path import exists, join, expanduser, expandvars
        if not workdir is None:
            self.workdir = expanduser(expandvars(workdir))
            if not exists(self.workdir):
                from os import mkdir
                try:
                    mkdir(self.workdir)
                except OSError:
                    print "ERROR: Unable to create working directory"
            else:
                if exists(join(self.workdir, 'notedata.worknote')):
                    if load_if_used or len(self.items) == 0:
                        self.load(verbosity=1)
                    else:
                        print 'WARNING:', self.workdir, 'is already in use.'
                        print '\tSaving will overwrite the saved content.'
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
                       'notedata.worknote'), 'wb') as outfile:
            cPickle.dump(self.head, outfile, cPickle.HIGHEST_PROTOCOL)
            cPickle.dump(self.foot, outfile, cPickle.HIGHEST_PROTOCOL)
            cPickle.dump(self.items, outfile, cPickle.HIGHEST_PROTOCOL)
            cPickle.dump(self.metadata, outfile, cPickle.HIGHEST_PROTOCOL)

    def load(self, workdir=None, verbosity=0):
        """
        Load the worknotes from a working directory

        Args
        ----
        workdir : str
            The directory to load from. Can be passed as None to use the
            workdir previously set (e.g. using set_workdir or during init).
        verbosity : int
            Select output verbosity. Defaults to 0 (= no output)
        """
        import cPickle
        from os.path import join, exists
        if self.workdir is None:
            if workdir is None:
                raise OSError('No working directory given')
            self.set_workdir(workdir)
        if verbosity > 0:
            print 'Loading existing worknote from "%s"...'%self.workdir
        if exists(join(self.workdir, self.workdir + '.worknote')):
            print 'WARNING: Old savefile naming in use, moving saved notes...'
            from shutils import copyfile
            copyfile(join(self.workdir, self.workdir + '.worknote'),
                     join(self.workdir, 'notedata.worknote'))
        with open(join(self.workdir,
                       'notedata.worknote'), 'rb') as infile:
            self.head = cPickle.load(infile)
            self.foot = cPickle.load(infile)
            self.items = cPickle.load(infile)
            self.metadata = cPickle.load(infile)

    def set_metadata(self, title="", author="", date="", subtitle=""):
        """
        Set the metadata used to generate a title page, if any is present.
        Set any field to an empty string ('') to remove it from output.
        Pass None for any field to keep current value.

        Args
        ----
        title : str
        author : str
        date : str
        """
        self.metadata.set_metadata(title=title, author=author, date=date,
                                   subtitle=subtitle)

    def get_text(self, style='Beamer'):
        """
        Returns the ASCII tex string
        """
        if style not in self.head:
            style = 'default'
        text = ""
        text += self.head[style]
        text = text.replace('%%%METADATA%%%', self.metadata.get_metadata(style))
        if not len(self.metadata) == 0:
            text = text.replace('%%%TITLEPAGE%%%', self.metadata.get_titlepage(style))
        else:
            text = text.replace('%%%TITLEPAGE%%%', '')
        for item in self.items:
            text += item.get_text(style)
        text += self.foot[style]
        return text

    def __str__(self):
        text = u"Worknote: " + str(self.metadata)
        for i in xrange(len(self.items)):
            text += "\n%d %s"%(i, self.items[i].__str__())
        return text

    def remove(self, index = []):
        """
        Remove the item at the given index.
        
        Args
        ----
        index : int or str or iterable
            Index must be either an integer index, an iterable list of integer
            indices or an index notation of the style 'i:j:k' where indices are
            separated by colons
        """
        self.pop(index)
        

    def move(self, src_index, dest_index):
        """
        Move the object at src_index to the dest_index
        
        Args
        ----
        src_index : int or str or iterable
            The source index. Index must be either an integer index, an 
            iterable list of integer indices or an index notation of the 
            style 'i:j:k' where indices are separated by colons
        dest_index : int or str or iterable
            The destination index
        """
        import items
        src_index = items.parse_index(src_index)
        dest_index = items.parse_index(dest_index)
        if type(self[src_index]) == items.Slide:
            dest_index = dest_index[0:1]
        elif type(self[src_index]) in [items.ListItem, items.EnumItem]:
            dest_index = dest_index[0:3]
        else:
            dest_index = dest_index[0:2]
        item = self.pop(src_index)
        self.add_item(item, dest_index)
        
class Metadata(object):
    """
    Class to handle metadata

    Args
    ----
    title : str
    author : str
    date : str
    subtitle : str
    """
    def __init__(self, title='', author='', date='', subtitle=''):
        self.metadata = {}
        self.formatter = {}
        self.formatter['title'] = {}
        self.formatter['title']['Beamer'] = '\\title{%s}\n'
        self.formatter['title']['Report'] = '\\title{%s}\n'
        self.formatter['title']['Markdown'] = '# %s\n'
        self.formatter['subtitle'] = {}
        self.formatter['subtitle']['Beamer'] = '\\subtitle{%s}\n'
        self.formatter['subtitle']['Report'] = '\\subtitle{%s}\n'
        self.formatter['subtitle']['Markdown'] = '    %s\n'
        self.formatter['date'] = {}
        self.formatter['date']['Beamer'] = '\\date{%s}\n'
        self.formatter['date']['Report'] = '\\date{%s}\n'
        self.formatter['date']['Markdown'] = '    %s\n\n'
        self.formatter['author'] = {}
        self.formatter['author']['Beamer'] = '\\author{%s}\n'
        self.formatter['author']['Report'] = '\\author{%s}\n'
        self.formatter['author']['Markdown'] = '    %s\n'
        
        self.titlepage_generator = {}
        self.titlepage_generator['Beamer'] = "\\frame[plain]{\\titlepage}\n"
        self.titlepage_generator['Report'] = "\\maketitle\n"
        self.titlepage_generator['Markdown'] = ""
        self.supported_metadata = {}
        self.supported_metadata['Beamer'] = ['title', 'author', 'date', 'subtitle']
        self.supported_metadata['Report'] = ['title', 'author', 'date']
        self.supported_metadata['Markdown'] = ['title', 'subtitle', 'author', 'date']
        self.set_metadata(title=title, author=author, date=date,
                          subtitle=subtitle)
    def get_metadata(self, style):
        """
        Returns a proper formated metadata string
        """
        metadata_str = ""
        for metadata in self.supported_metadata[style]:
            if self.metadata[metadata]:
                metadata_str += self.formatter[metadata][style]%self.metadata[metadata]
        return metadata_str
    def get_titlepage(self, style):
        """
        Returns a properly formated titelpage string
        """
        return self.titlepage_generator[style]
    def set_metadata(self, title="", author="", date="", subtitle=""):
        """
        Set the metadata used to generate a title page, if any is present.
        Set any field to an empty string ('') to remove it from output.
        Pass None for any field to keep current value.

        Args
        ----
        title : str
        author : str
        date : str
        subtitle : str
        """
        if not 'title' in self.metadata: #initialize
            self.metadata['title'] = ''
        if not 'author' in self.metadata:
            self.metadata['author'] = ''
        if not 'date' in self.metadata:
            self.metadata['date'] = ''
        if not 'subtitle' in self.metadata:
            self.metadata['subtitle'] = ''
        if title:
            self.metadata['title'] = set_unicode(title)
        if author:
            self.metadata['author'] = set_unicode(author)
        if date:
            self.metadata['date'] = set_unicode(date)
        if subtitle:
            self.metadata['subtitle'] = set_unicode(subtitle)
    def __len__(self):
        len = 0
        for key in self.metadata:
            if self.metadata[key]:
                len += 1
        return len
    def __str__(self):
        if 'title' in self.metadata:
            return self.metadata['title']
        return ""

