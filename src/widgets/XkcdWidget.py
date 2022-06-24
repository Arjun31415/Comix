from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QDesktopServices, QPixmap, QMovie, Qt
from ImageDownloader import ImageDownloader
from models.xkcd import Xkcd
import html
import sys


class XkcdWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.xkcd = Xkcd()
        self.gotLatest = False
        self.initializedUi = False

    def getLatest(self):
        if self.gotLatest is False:
            self.xkcd.getLatest()
        self.gotLatest = True

    def forceGetLatest(self):
        self.gotLatest = False
        self.getLatest()

    def forceInitUI(self):
        self.initializedUi = False
        self.initUI()

    def __setlayout(self):
        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
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
        if self.initializedUi is True:
            return
        self.__setlayout()
        # Buttons
        self.nextButton = QtWidgets.QPushButton("Next")
        self.prevButton = QtWidgets.QPushButton("Prev")

        self.prevButton.clicked.connect(self.getPreviousComic)
        self.nextButton.clicked.connect(self.getNextComic)

        # Main Comic Label
        self.text = QtWidgets.QLabel("")
        # Event Filter
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
        self.initializedUi = True

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
        elif ev.type() == QtCore.QEvent.Type.MouseButtonDblClick:
            QDesktopServices.openUrl(
                QtCore.QUrl(self.xkcd.getCurrentComicUrl()))
            # quit and focus the webbrowser
            sys.exit(0)

        return False
