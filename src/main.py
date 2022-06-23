import sys
from PySide6 import QtCore, QtWidgets
from widgets.XkcdWidget import XkcdWidget

import signal
import time


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


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        print("Got kill")
        self.kill_now = True


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
