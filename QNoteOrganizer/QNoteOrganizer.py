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
        #self.itemView.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.tb_cut.clicked.connect(self.delete_item)
    def delete_item(self):
        tree = []
        tree.append(self.itemView.currentItem())
        if not tree[-1]:
            return
        while tree[-1].parent():
            tree.append(tree[-1].parent())
        tree.reverse()
        slide_item = tree.pop(0)
        slide_index = self.itemView.indexOfTopLevelItem(slide_item)
        if len(tree) == 0:
            self.worknote.items.pop(slide_index)
            self.itemView.takeTopLevelItem(slide_index)
            return
        item = tree.pop(0)
        item_index = slide_item.indexOfChild(item)
        if len(tree) == 0:
            self.worknote.items[slide_index].items.pop(item_index)
            slide_item.takeChild(item_index)
            return
        subitem = tree.pop(0)
        subitem_index = item.indexOfChild(subitem)
        if len(tree)== 0:
            self.worknote.items[slide_index].items[item_index].items.pop(subitem_index)
            item.takeChild(subitem_index)
        else:
            print "Data not understood"
        
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
