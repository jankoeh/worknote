# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 12:58:34 2015

@author: koehler
"""
from __future__ import unicode_literals
from .. import worknotes
from PyQt4 import QtCore, QtGui
from ui_QNoteOrganizer import Ui_QNoteOrganizer

class QNoteOrganizer(QtGui.QDialog, Ui_QNoteOrganizer):
    def __init__(self, worknote, parent=None):
        super(QNoteOrganizer, self).__init__(parent)
        self.setupUi(self)
        self.worknote = worknote
        self.itemView.setHeaderLabels(["Type", "Content"])
        for slide in self.worknote.items:
            parent = QtGui.QTreeWidgetItem(self.itemView, 
                                           [slide.__class__.__name__, slide.title])
            for item in slide.items:
                if issubclass(type(item), worknotes.NoteContainer):
                    child = QtGui.QTreeWidgetItem(parent, 
                                                  [item.__class__.__name__, ""])
                    for childitem in item.items:
                        QtGui.QTreeWidgetItem(child, 
                                              [childitem.__class__.__name__, 
                                               childitem.data])
                else:
                    QtGui.QTreeWidgetItem(parent, 
                                          [item.__class__.__name__, str(item.data)])
        self.itemView.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
def edit_note(worknote):
    """
    Starts the QNoteOrganizer 
    """
    import sys
    from PyQt4 import QtGui
    qApp = QtGui.QApplication(sys.argv)
    form = QNoteOrganizer(worknote)
    form.show()
    qApp.exec_()
