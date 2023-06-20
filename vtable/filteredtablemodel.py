# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 17:10:33 2023

@author: fergal
"""

from ipdb import set_trace as idebug
from pdb import set_trace as debug
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


import PyQt5.QtWidgets as QtWidget
import PyQt5.QtCore as QtCore
import PyQt5.Qt as Qt
import PyQt5.QtGui as QtGui

class FilteredTableModel(QtCore.QAbstractTableModel):

    def __init__(self, df, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.orig_df = df
        self.sorted_df = df

        self.idx = np.ones(len(df), dtype=bool)

    def setFiltered(self, idx):
        """Set the values of the original dataframe which should be displayed"""
        assert len(idx) == len(self.orig_df)
        try:
            self.idx = idx.values
        except AttributeError:
            self.idx = idx
        print(f"In FTM, idx has {np.sum(self.idx)} True members")
        self.layoutChanged.emit()

    def rowCount(self, index):
        # return len(self.df)
        return np.sum(self.idx)


    def columnCount(self, index):
        return len(self.orig_df.columns)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.displayElement(index)
        elif role == QtCore.Qt.FontRole:
            return self.setFont(index)
        elif role == QtCore.Qt.BackgroundRole:
            return self.setBackground(index)
        else:
            return QtCore.QVariant()

    def displayElement(self, index):
        row = index.row()
        col = index.column()

        colName = self.sorted_df.columns[col]

        colData = self.sorted_df[colName]
        # colData = colData[self.idx]  #Do the filtering

        elt = colData.iloc[row]

        print(f"Displaying data for c,r = {col},{row}")
        if elt is None:
            return ""
        try:
            return "%g"% (elt)
        except TypeError:
            return str(elt)

    def setFont(self, index):
        return QtCore.QVariant()

    def setBackground(self, index):
        row = index.row()
        clr = QtGui.QColor('#FFFFFF')
        if (row % 5) == 5 -1:
            clr = QtGui.QColor('#DDDDFF')
        return QtGui.QBrush(clr)

        # # Mark item as readonly
        # item.setFlags( item.flags() & ~QtCore.Qt.EditRole)

    def sort(self, colNum, order):
        filtered_df = self.orig_df[self.idx]
        colName = self.sorted_df.columns[colNum]

        order = order == QtCore.Qt.AscendingOrder
        self.sorted_df = filtered_df.sort_values(colName, ascending=order)
        self.layoutChanged.emit()


class MainWin(QtWidget.QDialog):
    def __init__(self, df, num=1000, title="Dataframe", parent=None):
        QtWidget.QDialog.__init__(self, parent)
        self.create_layout(df, num, title)

        self.keyReleaseEvent = self.process_key_press
        self.title = "Super Table"
        self.show()

    def create_layout(self, df, num, title):
        self.button = QtWidget.QPushButton("Show/hide Columns")
        # self.button.clicked.connect(self.toggle_selector)

        self.model = FilteredTableModel(df)

        self.tableView = QtWidget.QTableView()
        self.tableView.setModel(self.model)
        self.tableView.setSortingEnabled(True)

        layout = QtWidget.QVBoxLayout()
        layout.addWidget(self.tableView)
        self.setLayout(layout)

        # self.resize(self.table.width(), self.table.height())
        # self.setMaximumSize(self.table.getMaxWidth(), 10000)
        self.setWindowTitle(title)

        # self.selector = selector.ColumnSelector(self.table)
        # self.selector.hide()

    # def toggle_selector(self):
    #     if self.selector.isVisible():
    #         self.selector.hide()
    #     else:
    #         self.selector.show()

    def process_key_press(self, eventQKeyEvent):
        key = eventQKeyEvent.key()
        if key == 81:  #The letter [q]
            self.hide()
            self.close()


def main(df):
    app = QtWidget.QApplication.instance()
    if app is None:
        app = QtWidget.QApplication([])


    win = MainWin(df)
    win.show()
    return win
