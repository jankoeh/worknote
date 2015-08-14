# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 16:34:08 2015

@author: koehler
"""
from __future__ import unicode_literals

def parse_index(index):
    from numpy import int64, array
    if type(index) == str:
        try:
            index = [int(x) for x in index.split(':')]
        except ValueError:
            raise ValueError('Invalid index notation: %s'%index)
        return index
    elif type(index) in [int, int64]:
        return [index,]
    elif type(index) in [list, tuple, array]:
        return [int(x) for x in index]
    else:
        raise ValueError('Invalid value for index: ' + str(index))

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
    def add_item(self, item, index=[]):
        """
        Adds an item to the items list

        Args
        ----
        item : NoteItem
            subitem to add to
        index : list or None
        """
        if index == []:
            index = [len(self.items),]
        index = parse_index(index)
        if len(index) == 1:
            self.items.insert(index[0], item)
        else:
            self[index[0:1]].add_item(item, index = index[1:])
    def pop(self, index = []):
        """
        Remove an item from the items list and return it

        Args
        ----
        index : list or None
        """
        if index == []:
            index = [-1,]
        index = parse_index(index)
        try:
            if len(index) == 1:
                return self.items.pop(index[0])
            else:
                return self[index[0:1]].pop(index[1:])
        except IndexError:
            raise IndexError("Invalid Index "+str(index))
    def __str__(self):
        text = self.__class__.__name__
        for item in self.items:
            text += "\n"+str(item)
        return text

    def __getitem__(self, index):
        if index == []:
            index = [-1,]
        index = parse_index(index)
        if len(index) == 1:
            try:
                res = self.items[index[0]]
            except IndexError:
                return None
            return res
        else:
            try:
                res = self.items[index[0]][index[1:]]
            except IndexError:
                return None
            return res

class List(NoteContainer):
    """
    The List environment
    """
    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)
        self.head['Beamer'] = '\\begin{itemize}\n'
        self.foot['Beamer'] = '\\end{itemize}\n'
        self.head['Markdown'] = "\n"
        self.foot['Markdown'] = "\n"        
    def __str__(self):
        text = self.__class__.__name__
        for i in xrange(len(self.items)):
            text += "\n    %d %s"%(i, self.items[i])
        return text
    def get_text(self, style = 'Beamer'):
        if style == 'Report':
            style = 'Beamer'
        return super(List, self).get_text(style = style)
        
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
        if style in ['Beamer', 'Report']:
            return "\\item {} \n".format(self.data)
        else: #Other styles need ne be handled by enumerate as well
            return "  - {} \n".format(self.data)
    def __str__(self):
        return self.__class__.__name__ + ': ' + self.data[:10] + '...'

class ListItem(NoteItem):
    """
    Item of a List
    """
    def clean_data(self, data):
        if data.strip()[:2] == "* ":
            data = data.strip()[2:]
        return set_unicode(data)
    def get_text(self, style):
        if style in ['Beamer', 'Report']:
            return "\\item {} \n".format(self.data)
        elif style in ["Markdown"]:
            return "  * {} \n".format(self.data)
        else:
            print "Defaulting to Markdown"
            return "  * {} \n".format(self.data)
    def __str__(self):
        return self.__class__.__name__ + ': ' + self.data[:10] + '...'

class Equation(NoteItem):
    """
    An Equation
    """
    def clean_data(self, data):
        data = set_unicode(data)
        data = data.strip().strip("$$")
        return data
    def get_text(self, style):
        if style in ['Beamer', 'Report', 'Markdown']:
            return "$$ {} $$".format(self.data)
        else:
            return "$$ {} $$".format(self.data)

class Text(NoteItem):
    """
    Some normal text
    """
    def get_text(self, style):
        if style in ['Beamer', 'Report']:
            return self.data.replace("\n", "~\\\\\n")
        elif style in ['Markdown']:
            text = self.data
            if self.data.strip()[-2:] != "\n":
                text = text+"\n"
            return text.replace("\n", "\n\n")
        else:
            return self.data
    def __str__(self):
        return self.__class__.__name__ + ': ' + self.data[:10] + '...'

class Code(NoteItem):
    """
    Some source code fragment
    """
    def get_text(self, style):
        if style in ['Beamer', 'Report']:
            text = self.data.replace('\n', '~\\\\\n')
            text = text.replace(' ', '~')
            text = text.replace('_', '\_')
            text = '\\texttt{' + text + '}'
        else:
            text = '```\n' + self.data + '\n```\n'
        return text


class Value(NoteItem):
    """
    A numerical value with units and a description
    """
    def __init__(self, var, precision=3, desc=None, units=None, error=None,
                 **kwargs):
        super(Value, self).__init__(str(var), **kwargs)        
        self.var = var
        self.precision = int(precision)
        self.desc = set_unicode(desc)
        self.units = set_unicode(units)
        self.error = error
        self.units_wrapper = {}
        self.units_wrapper['Beamer'] = '$%s$'
        self.units_wrapper['Markdown'] = '%s'
        self.unit_formatter = {}
        self.unit_formatter['Beamer'] = '\\mathsf{%s}'
        self.unit_formatter['Markdown'] = '%s'
        self.value_formatter = {}
        self.value_formatter['Beamer'] = '\\texttt{%s}'
        self.value_formatter['Markdown'] = '%s'
        self.cr_formatter = {}
        self.cr_formatter['Beamer'] = '\\\\\n'
        self.cr_formatter['Markdown'] = '\n\n'
        self.error_separator = {}
        self.error_separator['Beamer'] = ' $\pm$ '
        self.error_separator['Markdown'] = ' +/- '

    def get_text(self, style):
        import numpy
        if style == 'Report':
            style = 'Beamer'
        if type(self.var) in [int, numpy.int64]:
            fmtstr = u'{var:d}'
            res = fmtstr.format(var=self.var)
        elif type(self.var) in [float, numpy.float64]:
            if numpy.ceil(numpy.log10(self.var)) < 0 and \
                abs(numpy.ceil(numpy.log10(self.var))) >= self.precision:
                outfmt = 'e'
            else:
                outfmt = 'f'
            fmtstr = u'{var:0.' + str(self.precision) + outfmt + '}'
            res = fmtstr.format(var=self.var)
        if not self.error is None:
            res += self.error_separator[style] + fmtstr.format(var=self.error)
        res = self.value_formatter[style]%res
        if not self.desc is None:
            res = self.desc + ': ' + res
        if not self.units is None:
            res += ' ' + self.units_wrapper[style]%self.format_units(style)
        return res + self.cr_formatter[style]
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
    def __str__(self):
        return self.__class__.__name__ + ': {val:0.5g}'.format(val = self.var)

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
        if style in ['Beamer', 'Report']:
            text = "\\includegraphics[width=%g\\textwidth]{%s}\n"%(self.size, self.data)
            if self.align:
                text = "\\begin{%s}\n %s \\end{%s}"%(self.align, text, self.align)
            return text
        elif style in ['Markdown']:
            text = '![Image](%s)'%(self.data)
            return text
        else:
            return self.data
    def __str__(self):
        return self.__class__.__name__ + ': ' + self.data


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
        if style in ['Beamer', 'Report']:
            if self.size == 'auto' and style == 'Beamer':
                size = 'tiny'
                if len(self.data) < 25:
                    size = 'scriptsize'
                if len(self.data) < 22:
                    size = 'footnotesize'
                if len(self.data) < 18:
                    size = 'normalsize'
            elif self.size == 'auto':
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
        elif style in ['Markdown']:
            table = ""
            table_items = [[str(i) for i in line] for line in self.data]
            maxlen = []
            for i in xrange(len(table_items[0]))    :
                maxlen.append(max([len(line[i]) for line in table_items]))
            line  = table_items[0]
            table += "| "
            for i in xrange(len(line)):
                table += line[i] + " "*(maxlen[i]-len(line[i])) + " | "
            table += "\n|"
            for i in xrange(len(line)):
                table += "-"*(maxlen[i]+2) + "|"
            table += "\n"
            for line in table_items[1:]:
                table += "| "
                for i in xrange(len(line)):
                    table += line[i] + " "*(maxlen[i]-len(line[i])) + " | "
                table += "\n"
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
        self.data = title
        self.head['Beamer'] = "\\frame{\\frametitle{%s}\n"%title
        self.foot['Beamer'] = '}\n'
        self.head['Report'] = "\\section{%s}\n"%title
        self.foot['Report'] = '\n\n'
        self.head['Markdown'] = "## {}\n".format(title)
        self.foot['Markdown'] = "\n\n"
        
    def clean_data(self, title):
        title = set_unicode(title)
        if len(title.split("\n")) == 2 and \
             len(title.split("\n")[1]) >= 3 and \
             title.split("\n")[1][:3] == '---':
            title = title.split("\n")[0]
        return title

    def add_item(self, item, index=[], **kwargs):
        """
        Adds an item to a slide
        """
        listitem_handlers = {ListItem: List, EnumItem: Enumerate}
        if type(item) in listitem_handlers:
            if (type(self[index[0:1]]) == List and type(item) == ListItem) or \
                (type(self[index[0:1]]) == Enumerate and type(item) == EnumItem):
                self[index[0:1]].add_item(item, index = index[1:2])
            else:
                listitem = item
                item = listitem_handlers[type(listitem)](**kwargs)
                item.add_item(listitem)
                super(Slide, self).add_item(item, index=index[0:1])
        else:
            super(Slide, self).add_item(item, index=index[0:1])
    def __str__(self):
        text = "Slide: " + set_unicode(self.data)
        for i in xrange(len(self.items)):
            text += "\n  %d %s"%(i, self.items[i])
        return text



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
