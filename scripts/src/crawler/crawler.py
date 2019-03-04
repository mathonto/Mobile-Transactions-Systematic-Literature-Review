from abc import abstractmethod, ABC

from model.result import Result


class Crawler(ABC):

    def __init__(self, crawl_until_page=2, timeout=1):
        self._CRAWL_UNTIL_PAGE = crawl_until_page
        self._TIMEOUT = timeout

        agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'
        self._HEADER = {'User-Agent': agent}

    @abstractmethod
    def crawl(self, query: str) -> [Result]:
        pass
