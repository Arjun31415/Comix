from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests
from typing import ClassVar, Tuple
from datetime import date, timedelta
import re


@dataclass
class Dilbert:
    """
    Class to get dilbert comics
    """
    latest: date = date.today()
    URL: ClassVar[str] = "https://dilbert.com/strip/"
    HEADERS: ClassVar[dict] = {
        'User-Agent':
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36",
        "Accept-Language": "en-GB;q=0.5"
    }
    cur = date.today()

    def getLatest(self) -> None:
        today = date.today()
        webpage = requests.get(Dilbert.URL + today.strftime("%Y-%m-%d"),
                               headers=Dilbert.HEADERS)

        # if the current day's comic is not yet uploaded then the url will be
        # https://dilbert.com/
        if webpage.url != Dilbert.URL:
            self.latest = date.today() - timedelta(days=1)
        return

    def getComic(self, no: None | date = None) -> Tuple[date, str, str]:
        """
        Get the comic given by `no`
        returns the Comic number ,imageURL and the caption as a tuple
        """
        if no is None:
            no = self.latest
        self.cur = no
        comicPage = requests.get(Dilbert.URL + str(self.cur),
                                 headers=Dilbert.HEADERS)
        print(Dilbert.URL + f"{self.cur}")
        soup = BeautifulSoup(comicPage.content, "html.parser")
        imageTag = soup.select(".img-comic")[0]
        print(imageTag)
        if imageTag is None:
            raise ValueError("Image Tag not found")
        if type(imageTag) is list[str]:
            raise ValueError(
                "String expected, list found for variable imageTag")
        img: str = "".join(imageTag['src'])
        title: str = "".join(imageTag['alt'])
        # Use the pattern '((?!regex).)*' to match all lines
        # that do not contain regex pattern regex.
        # The expression '(?! ...)' is a negative lookahead
        # that ensures that the enclosed pattern ...
        # does not follow from the current position.
        match = re.match("((?!- Dilbert by Scott Adams).)*", title)
        if match is not None:
            title = match.group().strip()
        print(title)
        return (no, img, title)

    def getPreviousComic(self):
        return self.getComic(self.cur - timedelta(days=1))

    def getNextComic(self):
        return self.getComic(self.cur + timedelta(days=1))

    def getCurrentComicNumber(self) -> date:
        return self.cur

    def getLatestComicNumber(self) -> date:
        return self.latest

    def getOldestComicNumber(self) -> date:
        # lets go with the first time the pointy hair boss appears.
        return date(year=1989, month=7, day=31)

    def getCurrentComicUrl(self):
        return Dilbert.URL + str(self.cur)
