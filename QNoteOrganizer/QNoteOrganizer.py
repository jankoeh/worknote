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
        self.item_buffer= []                                         
        self.tb_cut.clicked.connect(self.delete_item)
        self.tb_insert.clicked.connect(self.insert_item)


    def get_item_tree(self):
        """
        Returns a list of the selected item and its parents
        I.e. [Ancestor, Parent, selected_item]
        """
        tree = []
        tree.append(self.itemView.currentItem())
        if not tree[-1]:
            return
        while tree[-1].parent():
            tree.append(tree[-1].parent())
        tree.reverse()
        return tree
    def get_indices(self, tree):
        """
        get the indices for a tree
        """
        indices = []
        indices.append(self.itemView.indexOfTopLevelItem(tree[0]))
        for i in xrange(1, len(tree)):
            indices.append(tree[i-1].indexOfChild(tree[i]))
        return indices
        
    def delete_item(self):
        """
        Delete selected item
        """
        tree = self.get_item_tree()
        indices = self.get_indices(tree)
        if len(tree) == 1:
            wn_item = self.worknote.items.pop(indices[-1])
            tv_item = self.itemView.takeTopLevelItem(indices[-1])
        elif len(tree) == 2:
            wn_item = self.worknote.items[indices[0]].items.pop(indices[1])
            tv_item = tree[-2].takeChild(indices[-1])
        elif len(tree) == 3:
            wn_item = self.worknote.items[indices[0]].items[indices[1]].items.pop(indices[2])
            tv_item = tree[-2].takeChild(indices[-1])
        else:
            print "Data not understood"
        self.item_buffer.append([wn_item, tv_item])            

    def insert_item(self):
        """
        Insert item from buffer
        """
        wn_item, tv_item = self.item_buffer.pop(-1)
        tree = self.get_item_tree()
        indices = self.get_indices(tree)
        print indices
        
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
