import csv
import os

from model.result import Result


class CSV:

    def __init__(self, dir_name=None):
        if dir_name:
            self._path = f'results2/{dir_name}/'
            if not os.path.exists(self._path):
                os.makedirs(self._path)
        else:
            self._path = ''

    def write(self, results: [], file_name: str):
        with open(self._path + file_name, 'w') as file:
            writer = csv.writer(file)
            keys = [key for key, value in vars(Result('', '', '', '', '')).items()]
            writer.writerow(keys)

            for result in results:
                values = [str(value).replace(';', '') for key, value in vars(result).items()]
                writer.writerow(values)
