"""
    File name: main.py
    Author: Adrian Wersching (https://www.github.com/awersching),
            Simon Matejetz (https://www.github.com/matejetz),
            Tobias Mathony (https://www.github.com/mathonto)
    
    This script crawls results on search engines IEEE, Google Scholar or Springer
    for queries stored in queries.txt and writes it into a csv.
"""
import gin

from analysis.count_duplicates import count_similar_results
from crawler.springer import SpringerLink
from input_output.csv import CSV
from input_output.queries import Queries
from input_output.super_csv import SuperCsv


def execute_queries():
    gin.parse_config_file('config.gin', True)

    crawler = SpringerLink()
    queries = Queries().get_queries()

    crawler_name = type(crawler).__name__
    csv = CSV(crawler_name)

    for query in queries:
        print(f'Querying {crawler_name} for {query}...')

        results = crawler.crawl(query)
        csv.write(results, query + '_' + crawler_name + '.csv')


def count_duplicates():
    print('Starting to count similar results')

    results = SuperCsv().get_super_csv()
    print('Done reading files')
    similarities = count_similar_results(results)
    csv = CSV()
    csv.write(similarities, 'results.csv')
    print('Finished counting similar results')


if __name__ == '__main__':
    count_duplicates()
