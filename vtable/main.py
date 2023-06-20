import PyQt5.QtWidgets as QtWidget
import PyQt5.QtWidgets

import pandas as pd
from . import supertable
from . import selector
from . import loaders

# Ensure PyQt is initialised
app = PyQt5.QtWidgets.QApplication.instance()
if app is None:
    app = PyQt5.QtWidgets.QApplication([])

"""
Sketches at initialising a set of filters 
"""




class MainWin(QtWidget.QDialog):
    def __init__(self, df, num=1000, title="Dataframe", parent=None):
        QtWidget.QMainWindow.__init__(self, parent)
        self.create_layout(df, num, title)

        self.keyReleaseEvent = self.process_key_press
        self.title = "Super Table"
        self.show()
        self.table.table.draw()  #Work around an initial-size issue

    def create_layout(self, df, num, title):
        self.button = QtWidget.QPushButton("Show/hide Columns")
        self.button.clicked.connect(self.toggle_selector)

        self.table = supertable.SuperTableWidget(df, num=num)

        layout = QtWidget.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.resize(self.table.width(), self.table.height())
        self.setMaximumSize(self.table.getMaxWidth(), 10000)
        self.setWindowTitle(title)

        self.selector = selector.ColumnSelector(self.table)
        self.selector.hide()

    def toggle_selector(self):
        if self.selector.isVisible():
            self.selector.hide()
        else:
            self.selector.show()

    def process_key_press(self, eventQKeyEvent):
        key = eventQKeyEvent.key()
        if key == 81:  #The letter [q]
            self.hide()
            self.close()


def future_main(path):
    app = PyQt5.QtWidgets.QApplication.instance()
    if app is None:
        app = PyQt5.QtWidgets.QApplication([])

    loader = loaders.Loaders()
    df = loader.load(path)

    win = MainWin(df)
    win.show()
    return win




import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: vtable filename")
        sys.exit(1)

    path = sys.argv[1]
    loader = loaders.Loader()
    df = loader.load(path)

    win = MainWin(df)
    win.show()
    app.exec()

