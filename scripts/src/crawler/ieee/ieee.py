import gin

from crawler.crawler import Crawler
from crawler.ieee.xploreapi import XPLORE
from model.result import Result
from model.result_constants import ResultConstants


@gin.configurable
class IEEEXplore(Crawler):

    def crawl(self, query: str) -> [Result]:
        xplore = self._build_xplore_query(query)
        results = xplore.callAPI()
        return self._parse(results)

    def _parse(self, results) -> [Result]:
        parsed = []
        if not 'articles' in results:
            return parsed

        for result in results['articles']:
            parsed.append(Result(
                title=result['title'],
                author=self._get_authors(result['authors']['authors']),
                date=self._get_year(result),
                link=self._get_link(result),
                pdf_link=result['pdf_url'],
                cite_count=self._get_cite_count(result),
                doi=self._get_doi(result)
            ))
        return parsed

    def _build_xplore_query(self, query) -> XPLORE:
        query = query.replace('+', ' ').replace('*', '')
        xplore = XPLORE('hebd5ry7yhmx8hxw9nr3me4w')
        xplore.outputDataFormat = 'object'
        xplore.maximumResults(35)

        xplore.articleTitle(query)
        xplore.abstractText(query)
        xplore.indexTerms(query)
        return xplore

    def _get_authors(self, authors) -> str:
        return ', '.join([author['full_name'] for author in authors])

    def _get_year(self, result) -> str:
        return result['publication_date'] if 'publication_date' in result else result['publication_year']

    def _get_link(self, result) -> str:
        return result['html_url'] if 'html_url' in result else result['abstract_url']

    def _get_cite_count(self, result) -> str:
        cite_count = int(result['citing_paper_count']) + \
                     int(result['citing_patent_count'])
        return str(cite_count)

    def _get_doi(self, result) -> str:
        return result['doi'] if 'doi' in result else ResultConstants.NO_DOI
