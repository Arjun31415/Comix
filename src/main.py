import sys
import random
from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QPixmap, QMovie, QHelpEvent, QTextObject, QTextDocument, Qt
from ImageDownloader import ImageDownloader
from xkcd import Xkcd
import html


class MyWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.xkcd = Xkcd()
        self.initUI()

        # layout.addWidget(self.movie, 0, 0, 5, 5)
        # self.button.clicked.connect(self.magic)
    def __setlayout(self):
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        self.myLayout = layout

    def generateComicStrip(self, cur: int) -> None:
        if (type(cur) is not int):
            raise ValueError(" cur must be int got: %s" % (type(cur)))
        if (cur == 0):
            comic = self.xkcd.getComic()
        elif (cur == 1):
            comic = self.xkcd.getNextComic()
        elif (cur == -1):
            comic = self.xkcd.getPreviousComic()
        else:
            raise ValueError("cur must be -1,0 or 1, got value: %d" % cur)
        self.text.setToolTip(comic[2])
        self.downloader.start_download(comic[1])

    def initUI(self) -> None:
        self.__setlayout()
        # Buttons
        self.nextButton = QtWidgets.QPushButton("Next")
        self.prevButton = QtWidgets.QPushButton("Prev")

        self.prevButton.clicked.connect(self.getPreviousComic)
        self.nextButton.clicked.connect(self.getNextComic)

        # Main Comic Label
        # self.text = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.text = QtWidgets.QLabel("")

        self.text.installEventFilter(self)

        # Loading Gif
        self.movie = QMovie("assets/pics/loading.gif")
        self.text.setMovie(self.movie)
        self.movie.start()

        # ImageDownloader
        self.downloader = ImageDownloader()
        self.downloader.finished.connect(self.handleFinished)
        self.generateComicStrip(0)

        # Add widgests to layout
        self.myLayout.addWidget(self.text, 0, 0, 10, 10)
        self.myLayout.addWidget(self.nextButton, 11, 1)
        self.myLayout.addWidget(self.prevButton, 11, 0)

    @QtCore.Slot()
    def magic(self):
        pass

    def handleFinished(self, image):
        self.movie.stop()
        self.text.setPixmap(QPixmap.fromImage(image))
        self.nextButton.setDisabled(False)
        self.prevButton.setDisabled(False)
        if (self.xkcd.getCurrentComicNumber() ==
                self.xkcd.getLatestComicNumber()):
            self.nextButton.setDisabled(True)
        if (self.xkcd.getCurrentComicNumber() ==
                self.xkcd.getOldestComicNumber()):
            self.prevButton.setDisabled(True)

    @QtCore.Slot()
    def getPreviousComic(self):
        self.text.setMovie(self.movie)
        self.movie.start()
        self.generateComicStrip(-1)

    @QtCore.Slot()
    def getNextComic(self):
        self.text.setMovie(self.movie)
        self.movie.start()
        self.generateComicStrip(1)

    def eventFilter(self, obj, ev):
        if (ev.type() == QtCore.QEvent.ToolTipChange):
            print(ev.type())
            if not isinstance(obj, QtWidgets.QWidget):
                raise ValueError('QObject "{}" not a widget.'.format(obj))
            tooltip = obj.toolTip()
            if tooltip and not Qt.mightBeRichText(tooltip):
                # HACK to make it rich text
                # refer https://stackoverflow.com/a/46212292
                tooltip = '<qt>{}</qt>'.format(html.escape(tooltip))
                obj.setToolTip(tooltip)
                return True
            return True
        return False


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.setFixedSize(800, 600)
    widget.show()

    sys.exit(app.exec())
