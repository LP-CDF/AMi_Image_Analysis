#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 13:02:46 2024

from https://gist.github.com/DataSolveProblems/972884bb9a53d5b2598e8674acc9e8ab
"""

import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
    


if __name__ == '__main__':
    import json
    app = QApplication(sys.argv)
    fname="/mnt/ARCHIVE/ARCHIVED_DATA/Automated_Visualization/Ludo/images/TEST/Project_database.json"
    with open(fname, "r") as f:
            data_json=json.load(f)
    df=create_DataFrame(data_json)
    model = pandasModel(df)
    view = QTableView()
    view.setModel(model)
    hide=[4,5,6,8,9]
    for i in hide:
        view.setColumnHidden(i,True)
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())