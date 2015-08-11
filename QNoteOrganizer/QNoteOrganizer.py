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
        self.item_buffer = []                                         
        self.update_itemViews()
        self.tb_cut.clicked.connect(self.delete_item)
        self.tb_insert.clicked.connect(self.insert_item)

    def update_itemViews(self):
        """
        update the itemView widget
        """
        #empty view
        while self.itemView.topLevelItemCount():
            self.itemView.takeTopLevelItem(0)
        #populate view
        for slide in self.worknote.items:
            parent = QtGui.QTreeWidgetItem(self.itemView, 
                                           [slide.__class__.__name__, slide.data])
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
        QtGui.QTreeWidgetItem(self.itemView, ["", ""]) #add empty element
        #empty buffy
        while self.bufferView.count():
            self.bufferView.takeItem(0)
        #fill buffer        
        for item in self.item_buffer:
             QtGui.QListWidgetItem(item.__class__.__name__+" : "+item.data, 
                                   self.bufferView)
        if len(self.item_buffer):
            self.tb_insert.setEnabled(True)
        else:
            self.tb_insert.setDisabled(True) 
        
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
        if indices[0] >= len(self.worknote.items):
            return #empty last element
        wn_item = self.worknote.pop(indices)
        self.update_itemViews()
        self.item_buffer.insert(0, wn_item)            

    def insert_item(self):
        """
        Insert item from buffer
        """
        wn_item = self.item_buffer.pop(self.bufferView.currentIndex())
        tree = self.get_item_tree()
        indices = self.get_indices(tree)
        self.worknote.insert(indices, wn_item)
        self.update_itemViews()
        
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
