from model.result import Result
from model.result_constants import ResultConstants


def count_similar_results(results: [Result]) -> [Result]:
    c = 0
    found_results = []

    for result in results:
        found = False

        for found_result in found_results:
            if result == found_result:
                _update_found_result(result, found_result)
                found = True
                break
        if not found:
            found_results.append(result)

        c += 1
        print(f'Result number {c} done')
    return found_results


def _update_found_result(result: Result, found_result: Result):
    found_result.nr_found += 1

    not_empty = (result.cite_count != ResultConstants.NO_CITE_COUNT and
                 found_result.cite_count != ResultConstants.NO_CITE_COUNT)
    if not_empty:
        max_cite_count = max(_to_number(result.cite_count), _to_number(found_result.cite_count))
        found_result.cite_count = str(max_cite_count)


def _to_number(cite_count: str) -> int:
    if 'k' not in cite_count:
        return int(cite_count)

    cite_count = cite_count.replace('k', '')
    return int(float(cite_count) * 1000)
