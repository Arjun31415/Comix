import sys
import random
from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QPixmap, QMovie
from ImageDownloader import ImageDownloader
from xkcd import Xkcd


class MyWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.xkcd = Xkcd()
        self.nextButton = QtWidgets.QPushButton("Next")
        self.prevButton = QtWidgets.QPushButton("Prev")
        self.prevButton.clicked.connect(self.getPreviousComic)
        self.nextButton.clicked.connect(self.getNextComic)
        self.text = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.movie = QMovie("assets/pics/loading.gif")
        self.text.setMovie(self.movie)
        self.movie.start()
        self.layout = QtWidgets.QGridLayout(self)
        self.downloader = ImageDownloader()
        self.downloader.finished.connect(self.handleFinished)

        self.downloader.start_download(self.xkcd.getComic()[1])

        self.layout.addWidget(self.text, 0, 0, 10, 10)
        self.layout.addWidget(self.nextButton, 11, 1)
        self.layout.addWidget(self.prevButton, 11, 0)
        # self.layout.addWidget(self.movie, 0, 0, 5, 5)
        # self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        pass

    def handleFinished(self, image):
        self.movie.stop()
        pixmap = QPixmap.fromImage(image)
        self.text.setPixmap(pixmap)
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
        self.downloader.start_download(self.xkcd.getPreviousComic()[1])

    @QtCore.Slot()
    def getNextComic(self):
        self.text.setMovie(self.movie)
        self.movie.start()
        self.downloader.start_download(self.xkcd.getNextComic()[1])


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
