from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests
from typing import ClassVar, Tuple


@dataclass
class Xkcd:
    """
    Class to get xkcd comics
    """
    latest: int = -1
    URL: ClassVar[str] = "https://xkcd.com/"
    HEADERS: ClassVar[dict] = {
        'User-Agent':
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36",
        "Accept-Language": "en-GB;q=0.5"
    }
    cur = -1

    def getLatest(self):
        webpage = requests.get(Xkcd.URL, headers=Xkcd.HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        link = soup.select_one("#middleContainer > a:nth-child(6)").text
        link = "".join(link.split())
        self.latest = int(link.split("/")[-2])
        self.cur = self.latest
        print(f"Latest comic: {self.latest}")

    def getComic(self, no: None | int = None) -> Tuple[int, str, str]:
        """
        Get the comic given by `self`
        returns the Comic number ,imageURL and the caption as a tuple
        """
        if no is None:
            no = self.latest
        if (no < 0):
            no = 1
        if (no > self.latest):
            no = self.latest
        self.cur = no
        comicPage = requests.get(Xkcd.URL + str(self.cur),
                                 headers=Xkcd.HEADERS)
        print(Xkcd.URL + f"{self.cur}")
        soup = BeautifulSoup(comicPage.content, "html.parser")
        imageTag = soup.select("#comic img")[0]
        print(imageTag)
        if imageTag is None:
            raise ValueError("Image Tag not found")
        if type(imageTag) is list[str]:
            raise ValueError(
                "String expected, list found for variable imageTag")
        img = "https:" + imageTag['src']
        title: str = imageTag['title']
        print(title)
        return (no, img, title)

    def getPreviousComic(self):
        return self.getComic(self.cur - 1)

    def getNextComic(self):
        return self.getComic(self.cur + 1)

    def getCurrentComicNumber(self):
        return self.cur

    def getLatestComicNumber(self):
        return self.latest

    def getOldestComicNumber(self):
        return 1

    def getCurrentComicUrl(self):
        return Xkcd.URL + str(self.cur)
