import sys
from PySide6 import QtCore, QtWidgets
from widgets.DilbertWidget import DilbertWidget
from widgets.XkcdWidget import XkcdWidget

import signal


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widgets = [XkcdWidget(), DilbertWidget()]
        self.tabNames = ["XKCD", "Dilbert"]
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setDocumentMode(True)
        self.installEventFilter(self)
        self.scrollAreas = []
        for i in range(0, len(self.widgets)):
            self.scrollAreas.append(QtWidgets.QScrollArea(self))
            self.scrollAreas[i].viewport().setObjectName("comicViewPort")
            self.scrollAreas[i].setWidget(self.widgets[i])
            self.tabs.addTab(self.scrollAreas[i], self.tabNames[i])
        self.tabs.currentChanged.connect(self.initWidget)
        self.setCentralWidget(self.tabs)
        self.setFixedSize(800, 600)

    def eventFilter(self, obj, ev):
        if (ev.type() == QtCore.QEvent.Show):
            self.initWidget(0)
        return False

    def initWidget(self, no: int):
        print("Widget called ", no)
        self.widgets[no].getLatest()
        self.widgets[no].initUI()


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    with open("src/styles.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    app.exec()


if __name__ == '__main__':
    main()
