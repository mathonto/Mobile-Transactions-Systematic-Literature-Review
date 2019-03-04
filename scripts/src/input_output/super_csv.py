import csv
import os

from model.result import Result


class SuperCsv:

    def __init__(self):
        self.path = os.path.join('results2')

    def get_super_csv(self) -> [Result]:
        results = []

        for directory in os.listdir(self.path):
            csv_results = os.listdir(os.path.join(self.path, directory))

            for csv_result in csv_results:
                with open(os.path.join(self.path, directory, csv_result)) as file:
                    reader = csv.reader(file)

                    for row in reader:
                        if row[0] == 'title':
                            continue
                        results.append(Result(
                            title=row[0],
                            author=row[1],
                            date=row[2],
                            link=row[3],
                            pdf_link=row[4],
                            query=csv_result,
                            search_engine=directory,
                            cite_count=row[8],
                            doi=row[9]
                        ))
        return results
