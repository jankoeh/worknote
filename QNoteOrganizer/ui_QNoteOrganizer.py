# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_QNoteOrganizer.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_QNoteOrganizer(object):
    def setupUi(self, QNoteOrganizer):
        QNoteOrganizer.setObjectName(_fromUtf8("QNoteOrganizer"))
        QNoteOrganizer.resize(628, 510)
        self.horizontalLayout = QtGui.QHBoxLayout(QNoteOrganizer)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.itemView = QtGui.QTreeWidget(QNoteOrganizer)
        self.itemView.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.itemView.setHeaderHidden(False)
        self.itemView.setColumnCount(2)
        self.itemView.setObjectName(_fromUtf8("itemView"))
        self.itemView.headerItem().setText(0, _fromUtf8("1"))
        self.itemView.headerItem().setText(1, _fromUtf8("2"))
        self.verticalLayout_2.addWidget(self.itemView)
        self.label = QtGui.QLabel(QNoteOrganizer)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.bufferView = QtGui.QListWidget(QNoteOrganizer)
        self.bufferView.setMaximumSize(QtCore.QSize(16777215, 100))
        self.bufferView.setObjectName(_fromUtf8("bufferView"))
        self.verticalLayout_2.addWidget(self.bufferView)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tb_insert = QtGui.QToolButton(QNoteOrganizer)
        self.tb_insert.setObjectName(_fromUtf8("tb_insert"))
        self.verticalLayout.addWidget(self.tb_insert)
        self.tb_cut = QtGui.QToolButton(QNoteOrganizer)
        self.tb_cut.setObjectName(_fromUtf8("tb_cut"))
        self.verticalLayout.addWidget(self.tb_cut)
        self.tb_down = QtGui.QToolButton(QNoteOrganizer)
        self.tb_down.setObjectName(_fromUtf8("tb_down"))
        self.verticalLayout.addWidget(self.tb_down)
        self.tb_edit = QtGui.QToolButton(QNoteOrganizer)
        self.tb_edit.setObjectName(_fromUtf8("tb_edit"))
        self.verticalLayout.addWidget(self.tb_edit)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(QNoteOrganizer)
        QtCore.QMetaObject.connectSlotsByName(QNoteOrganizer)

    def retranslateUi(self, QNoteOrganizer):
        QNoteOrganizer.setWindowTitle(_translate("QNoteOrganizer", "QNoteOrganizer", None))
        self.label.setText(_translate("QNoteOrganizer", "Removed item buffer:", None))
        self.tb_insert.setToolTip(_translate("QNoteOrganizer", "Insert item from buffer into Worknote", None))
        self.tb_insert.setText(_translate("QNoteOrganizer", "->", None))
        self.tb_cut.setToolTip(_translate("QNoteOrganizer", "Delete item from Worknote", None))
        self.tb_cut.setText(_translate("QNoteOrganizer", "X", None))
        self.tb_down.setText(_translate("QNoteOrganizer", "...", None))
        self.tb_edit.setText(_translate("QNoteOrganizer", "...", None))

