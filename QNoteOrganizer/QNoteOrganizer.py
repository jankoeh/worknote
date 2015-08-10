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

    def get_tree(self):
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
    def delete_item(self):
        """
        Delete selected item
        """
        tree = self.get_tree()
        slide_item = tree.pop(0)
        slide_index = self.itemView.indexOfTopLevelItem(slide_item)
        if len(tree) == 0:
            wn_item = self.worknote.items.pop(slide_index)
            tv_item = self.itemView.takeTopLevelItem(slide_index)
            self.item_buffer.append([wn_item, tv_item])
            return
        item = tree.pop(0)
        item_index = slide_item.indexOfChild(item)
        if len(tree) == 0:
            wn_item = self.worknote.items[slide_index].items.pop(item_index)
            tv_item = slide_item.takeChild(item_index)
            self.item_buffer.append([wn_item, tv_item])            
            return
        subitem = tree.pop(0)
        subitem_index = item.indexOfChild(subitem)
        if len(tree)== 0:
            wn_item = self.worknote.items[slide_index].items[item_index].items.pop(subitem_index)
            tv_item = item.takeChild(subitem_index)
            self.item_buffer.append([wn_item, tv_item])
        else:
            print "Data not understood"
    def insert_item(self):
        """
        Insert item from buffer
        """
        wn_item, tv_item = self.item_buffer.pop(-1)
        
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
