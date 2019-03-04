from dataclasses import dataclass
from fuzzywuzzy import fuzz

from model.result_constants import ResultConstants


@dataclass
class Result:
    title: str
    author: str
    date: str
    link: str
    pdf_link: str

    query: str = ''
    search_engine: str = ''

    nr_found: int = 1

    cite_count: str = ResultConstants.NO_CITE_COUNT
    doi: str = ResultConstants.NO_DOI

    def __str__(self) -> str:
        return str(vars(self))

    def __eq__(self, other):
        if type(other) is not Result:
            return False

        link_equal = self.link == other.link
        return (link_equal or
                self.is_doi_equal(other) or
                self.is_title_fuzzy_equal(other))

    def __hash__(self):
        return hash(self.link + self.title)

    def is_doi_equal(self, other) -> bool:
        return (self.doi != ResultConstants.NO_DOI and
                other.doi != ResultConstants.NO_DOI and
                self.doi == other.doi)

    def is_title_fuzzy_equal(self, other) -> bool:
        return fuzz.ratio(self.title, other.title) >= 75
