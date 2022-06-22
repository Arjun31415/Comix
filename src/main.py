import sys
from PySide6 import QtCore, QtWidgets
from widgets.XkcdWidget import XkcdWidget


# BUG:
# 1. https://xkcd.com/2613/ image is not fully seen in the w
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.xkcdWidget = XkcdWidget()
        self.setCentralWidget(self.xkcdWidget)
        self.setFixedSize(800, 600)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
