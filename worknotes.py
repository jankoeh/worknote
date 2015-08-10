# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:09:57 2015

@author: koehler
"""
from __future__ import unicode_literals

class NoteItem(object):
    """
    Base Class which stores - reformats and returns data
    """
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
        return set_unicode(data)
    def __str__(self):
        return self.__class__.__name__

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
    def __str__(self):
        text = self.__class__.__name__
        for item in self.items:
            text += "\n"+str(item)
        return text


class List(NoteContainer):
    """
    The List environment
    """
    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)
        self.head['Beamer'] = '\\begin{itemize}\n'
        self.foot['Beamer'] = '\\end{itemize}\n'
    def __str__(self):
        text = self.__class__.__name__
        for i in xrange(len(self.items)):
            text += "\n    %d %s"%(i, self.items[i])
        return text
class Enumerate(List):
    """
    Enumerated list environment
    """
    def __init__(self, **kwargs):
        super(Enumerate, self).__init__(**kwargs)
        self.head['Beamer'] = '\\begin{enumerate}\n'
        self.foot['Beamer'] = '\\end{enumerate}\n'

class EnumItem(NoteItem):
    """
    Item of an enumerated list
    """
    def clean_data(self, data):
        if data.strip()[:2] == "# ":
            data = data.strip()[2:]
        return set_unicode(data)
    def get_text(self, style="Beamer"):
        if style in ['Beamer', 'LaTeX']:
            return "\\item {} \n".format(self.data)
        else: #Other styles need ne be handled by enumerate as well
            return "  - {} \n".format(self.data)

class ListItem(NoteItem):
    """
    Item of a List
    """
    def clean_data(self, data):
        if data.strip()[:2] == "* ":
            data = data.strip()[2:]
        return set_unicode(data)
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
        data = set_unicode(data)
        data = data.strip().strip("$$")
        return data
    def get_text(self, style):
        if style in ['Beamer', 'LaTeX']:
            return "$$ {} $$".format(self.data)
        else:
            return "$$ {} $$".format(self.data)

class Text(NoteItem):
    """
    Some normal text
    """
    def get_text(self, style):
        if style in ['Beamer', 'LaTeX']:
            return self.data.replace("\n", "~\\\\\n")
        else:
            return self.data

class Code(NoteItem):
    """
    Some source code fragment
    """
    def __init__(self, data, **kwargs):
        super(Code, self).__init__(data, **kwargs)
        self.header = {}
        self.header['Beamer'] = '\\texttt{'
        self.footer = {}
        self.footer['Beamer'] = '}'
    def get_text(self, style):
        if style in ['Beamer', 'LaTeX']:
            text = self.data.replace('\n', '~\\\\\n')
            text = text.replace(' ', '~')
            text = text.replace('_', '\_')
            return self.header['Beamer'] + text + self.footer['Beamer']
        else:
            return self.data

class Value(NoteItem):
    """
    A numerical value with units and a description
    """
    def __init__(self, var, precision=3, desc=None, units=None, **kwargs):
        self.var = var
        self.precision = int(precision)
        self.desc = set_unicode(desc)
        self.units = set_unicode(units)
        self.units_wrapper = {}
        self.units_wrapper['Beamer'] = '$%s$'
        self.unit_formatter = {}
        self.unit_formatter['Beamer'] = '\\mathsf{%s}'
        self.value_formatter = {}
        self.value_formatter['Beamer'] = '\\texttt{%s}'
    def get_text(self, style):
        import numpy
        if type(self.var) in [int, numpy.int64]:
            res = u'{var:d}'.format(var=self.var)
        elif type(self.var) in [float, numpy.float64]:
            if numpy.ceil(numpy.log10(self.var)) < 0 and \
                abs(numpy.ceil(numpy.log10(self.var))) >= self.precision:
                outfmt = 'e'
            else:
                outfmt = 'f'
            fmtstr = u'{var:0.' + str(self.precision) + outfmt + '}'
            res = fmtstr.format(var=self.var)
        res = self.value_formatter[style]%res
        if not self.desc is None:
            res = self.desc + ': ' + res
        if not self.units is None:
            res += ' ' + self.units_wrapper[style]%self.format_units(style)
        return res + '\\\\\n'
    def format_units(self, style):
        """
        Formats units into proper style. E.g. m^2 -> \mathsf{m}^2
        """
        import re
        string = self.units
        expr = '[a-zA-Z]+'
        res = u''
        while True:
            match = re.search(expr, string)
            if match:
                res += string[:match.start()]
                res += self.unit_formatter[style]%match.group(0)
                string = string[match.end():]
            else:
                res += string
                break
        return res

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
            copyfile(data, path.join(self.workdir, fn_figure))
        else:
            fn_figure += '.' + self.gfxfmt
            data.savefig(path.join(self.workdir, fn_figure))
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

    Parameters
    ----------
    data : list or numpy.ndarray
        2D list or array which contains lines and columns
        If the first line contains a string - first line is assumed to be the
        title
    size : str
        Can be an arbirary LaTeX fontsize (only relevant for LaTeX right now).
        default='normalsize'. If set to 'auto', size is determined by table
        length. This assumes an empty slide ...
    """
    def __init__(self, data, size='normalsize', **kwargs):
        super(Table, self).__init__(data, **kwargs)
        if size not in ['tiny', 'scriptsize', 'footnotesize', 'small', 'normalsize',
                        'large', 'Large', 'LARGE', 'huge', 'Huge', 'auto']:
            print "Fontsize not recognized, defaulting to auto"
            size = 'auto'
        self.size = size
    def get_text(self, style, size='normalsize'):
        if style in ['Beamer', 'LaTeX']:
            if self.size == 'auto':
                size = 'tiny'
                if len(self.data) < 25:
                    size = 'scriptsize'
                if len(self.data) < 22:
                    size = 'footnotesize'
                if len(self.data) < 18:
                    size = 'normalsize'
            data = self.data
            table = "\n\\begin{center}\n\\begin{%s}\n"%size
            table += "\\begin{tabular}{%s}\n \\hline\n"%('c'*len(data[0]))
            if len(data[0]) > 1 and type(data[0][1]) in [str, unicode]:
                table += "&".join([str(i) for i in data[0]]) + "\\\\ \n \hline "
                data = data[1:]
            for line in data:
                table += "&".join([str(i) for i in line]) + "\\\\ \n"
            table += "\\hline \\hline\n \\end{tabular}\n"
            table += "\\end{%s}\n\\end{center}\n"%size
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
        self.title = title
        self.head['Beamer'] = "\\frame{\\frametitle{%s}\n"%title
        self.foot['Beamer'] = '}\n'
        self.head['Markdown'] = "{}\n".format(title) + "-"*len(title)+"\n"
        self.foot['Markdown'] = "\n"
    def clean_data(self, title):
        title = set_unicode(title)
        if len(title.split("\n")) == 2 and \
             len(title.split("\n")[1]) >= 3 and \
             title.split("\n")[1][:3] == '---':
            title = title.split("\n")[0]
        return title

    def add_item(self, item, **kwargs):
        """
        Adds an item to slide
        """
        if type(item) == ListItem: # Handle Lists
            if len(self.items) == 0 or type(self.items[-1]) != List:
                self.items.append(List(**kwargs))
            self.items[-1].add_item(item)
        elif type(item) == EnumItem: # Handle enumerated Lists
            if len(self.items) == 0 or type(self.items[-1]) != Enumerate:
                self.items.append(Enumerate(**kwargs))
            self.items[-1].add_item(item)
        else:
            self.items.append(item)
    def __str__(self):
        text = "Slide: " + set_unicode(self.title)
        for i in xrange(len(self.items)):
            text += "\n  %d %s"%(i, self.items[i])
        return text

TYPES = {'slide' : Slide,
         'text' : Text,
         'equation' : Equation,
         'list' : ListItem,
         'enumerate' : EnumItem,
         'figure' : Figure,
         'figurepage': Figure,
         'table' : Table,
         'value' : Value,
         'code': Code}

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
        self.metadata = Metadata()
        self.set_metadata(title, author, date, subtitle)
        if 'load_if_used' in kwargs:
            load_if_used = kwargs.pop('load_if_used')
        else:
            load_if_used = True
        self.set_workdir(workdir, load_if_used=load_if_used)

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
        **kwargs : keyword arguments
            Args like figsize etc
        """
        if cat == None:
            cat = find_category(item)
        if cat in ['figure', 'figurepage'] and self.workdir is None:
            print 'Cannot add figure until working directory is set'
            return
        if not cat in TYPES:
            raise TypeError("Category not recognized: %s"%cat)
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
              * More to come!
        """
        from os import path
        import codecs
        build_pdf = True
        if style[-4:] == '.tex':
            build_pdf = False
            style = style[:-4]
        f_out = codecs.open(path.join(self.workdir, style+".tex"), 'w',
                            encoding='utf-8')
        f_out.write(self.get_text(style=style))
        f_out.close()
        if build_pdf:
            print "Building pdf"
            from subprocess import call
            build = call(["pdflatex", style+".tex"], cwd=self.workdir)
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
                if exists(join(self.workdir, self.workdir + '.worknote')):
                    if load_if_used or len(self.items) == 0:
                        print "Loading existing worknote from %s"%workdir
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
            print 'Loading from', self.workdir
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
        if type(self.metadata) == dict:
            print 'WARNING: Converting metadata from old format'
            print '\tPlease check the metadata for correctness after loading'
            old_md = self.metadata
            self.metadata = Metadata(**old_md)

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
        self.title_formatter = {}
        self.title_formatter['Beamer'] = '\\title{%s}\n'
        self.subtitle_formatter = {}
        self.subtitle_formatter['Beamer'] = '\\subtitle{%s}\n'
        self.date_formatter = {}
        self.date_formatter['Beamer'] = '\\date{%s}\n'
        self.author_formatter = {}
        self.author_formatter['Beamer'] = '\\author{%s}\n'
        self.titlepage_generator = {}
        self.titlepage_generator['Beamer'] = "\\frame[plain]{\\titlepage}\n"
        self.set_metadata(title=title, author=author, date=date,
                          subtitle=subtitle)
    def get_metadata(self, style):
        """
        Returns a proper formated metadata string
        """
        metadata_str = ""
        if self.metadata['title']:
            metadata_str += self.title_formatter[style]%self.metadata['title']
        if self.metadata['subtitle']:
            metadata_str += self.subtitle_formatter[style]%self.metadata['subtitle']
        if self.metadata['date']:
            metadata_str += self.date_formatter[style]%self.metadata['date']
        if self.metadata['author']:
            metadata_str += self.author_formatter[style]%self.metadata['author']
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

def set_unicode(text):
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
    return text

