import time

import gin
import re
import urllib.request
from bs4 import BeautifulSoup
from urllib.error import HTTPError

from crawler.crawler import Crawler
from model.result import Result
from model.result_constants import ResultConstants


@gin.configurable
class SpringerLink(Crawler):

    def __init__(self, crawl_until_page=2, timeout=1):
        super().__init__(crawl_until_page, timeout)
        self._SPRINGER_URL = 'https://link.springer.com'

    def crawl(self, query: str) -> [Result]:
        results = []

        soup = self._query_page(1, query)
        pages = int(soup.find('span', {'class': 'number-of-pages'}).get_text().replace(',', ''))
        results += self._parse_results(soup)

        try:
            for current_page in range(2, pages + 1):
                print(f'Page {current_page} of {pages}...')

                soup = self._query_page(current_page, query)
                results += self._parse_results(soup)
                time.sleep(self._TIMEOUT)
        except HTTPError:
            print('Pages in Spring Link >= 1000 are not working')
        return results

    def _query_page(self, page, query) -> BeautifulSoup:
        url = self._SPRINGER_URL + f'/search/page/{page}?query={query}'
        request = urllib.request.Request(url, None, self._HEADER)
        html = urllib.request.urlopen(request).read()
        return BeautifulSoup(html, 'html.parser')

    def _parse_results(self, soup) -> [Result]:
        html_list = soup.find('ol', {'id': 'results-list'}).findAll('li')
        results = []

        for list_item in html_list:
            if not self._is_result(list_item):
                continue

            link = self._get_link(list_item)
            link_soup = self._open_result_link(link)

            results.append(Result(
                title=self._get_title(list_item),
                author=self._get_authors(list_item),
                date=self._get_year(list_item),
                link=link,
                pdf_link=self._get_pdf_link(list_item),
                cite_count=self._get_cite_count(link_soup),
                doi=self._get_doi(link_soup)
            ))
        return results

    def _get_title(self, list_item) -> str:
        return list_item.find('a', {'class': 'title'}).get_text()

    def _get_authors(self, list_item) -> str:
        if list_item.findAll('span', {'class': 'authors'}):
            return ','.join([author.get_text() for author in list_item.findAll('span', {'class': 'authors'})]) \
                .replace('\n', '')
        else:
            return ResultConstants.NO_AUTHOR

    def _get_year(self, list_item) -> str:
        if list_item.find('span', {'class': 'year'}):
            return list_item.find('span', {'class': 'year'}).get_text() \
                .replace('(', '') \
                .replace(')', '')
        else:
            return ResultConstants.NO_YEAR

    def _get_link(self, list_item) -> str:
        return self._SPRINGER_URL + list_item.find('a', {'class': 'title'})['href']

    def _get_pdf_link(self, list_item) -> str:
        if list_item.find('a', {'class': 'webtrekk-track pdf-link'}):
            return self._SPRINGER_URL + list_item.find('a', {'class': 'webtrekk-track pdf-link'})['href']
        else:
            return ResultConstants.NO_PDF

    def _is_result(self, list_item) -> bool:
        return list_item.find('a', {'class': 'title'})

    def _get_cite_count(self, soup: BeautifulSoup) -> str:
        if not soup:
            return ResultConstants.NO_CITE_COUNT

        cite_count = soup.find('span', id=re.compile('citations-count-number'))
        return str(cite_count.get_text()) if cite_count else ResultConstants.NO_CITE_COUNT

    def _get_doi(self, soup: BeautifulSoup) -> str:
        if not soup:
            return ResultConstants.NO_DOI

        doi = soup.find(id='doi-url')
        return doi.get_text() if doi else ResultConstants.NO_DOI

    def _open_result_link(self, link: str) -> BeautifulSoup:
        try:
            request = urllib.request.Request(link, None, self._HEADER)
            html = urllib.request.urlopen(request).read()
            return BeautifulSoup(html, 'html.parser')
        except HTTPError as http_error:
            if http_error.code == 500:
                print(f'The link {link} seems to be invalid')
            else:
                print(f'Something went wrong getting the cite count for {link}')
