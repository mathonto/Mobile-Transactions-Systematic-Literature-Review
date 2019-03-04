import time

import gin
import re
import urllib.request
from bs4 import BeautifulSoup

from crawler.crawler import Crawler
from model.result import Result
from model.result_constants import ResultConstants


@gin.configurable
class GoogleScholar(Crawler):

    def __init__(self, crawl_until_page=2, timeout=1):
        super().__init__(crawl_until_page, timeout)
        self.SCHOLAR_URL = 'https://scholar.google.de/scholar?'

    def build_gs_url(self, search_query: str, page_number: int) -> str:
        return self.SCHOLAR_URL + f"start={page_number * 10}&q={search_query}"

    def crawl(self, query: str) -> [Result]:
        results = []
        for current_page in range(0, self._CRAWL_UNTIL_PAGE):
            request = urllib.request.Request(self.build_gs_url(query, current_page), None,
                                             self._HEADER)
            response = urllib.request.urlopen(request).read()
            results += self.html_to_result(response)
            time.sleep(self._TIMEOUT)
        return results

    def html_to_result(self, html) -> [Result]:
        results = []
        soup = BeautifulSoup(html, "html.parser")
        meta_articles = soup.findAll("div", {"class": "gs_r gs_or gs_scl"})
        for meta_article in meta_articles:
            article_info = meta_article.find("div", {"class": "gs_ri"})
            link_title = article_info.find("a")
            title = link_title.get_text()
            author = article_info.find("div", {"class": "gs_a"}).get_text()
            year = re.search(r'\d{4}', author).group() if re.search(r'\d{4}', author) else ResultConstants.NO_YEAR
            link = link_title["href"]
            additional_info = meta_article.find("div", {"class": "gs_or_ggsm"})
            pdf_link = additional_info.find("a")["href"] if additional_info else ResultConstants.NO_PDF
            result = Result(
                title=title,
                author=author,
                date=year, link=link,
                pdf_link=pdf_link,
                cite_count=self._get_cite_count(meta_article)
            )
            results.append(result)
        return results

    def _get_cite_count(self, meta_article) -> str:
        cite_string = 'Zitiert von: '
        cite_count = meta_article.find(text=re.compile(rf'{cite_string}*'))

        return cite_count.replace(cite_string, '') if cite_count else ResultConstants.NO_CITE_COUNT
