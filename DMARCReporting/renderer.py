import csv

from tabulate import tabulate
from .constants import headers


class ConsoleRenderer:
    def render(self, file, data):
        if len(data) == 0:
            return

        print(tabulate(data, headers=headers))


class CSVRenderer:
    def render(self, file, data):
        with open(file, 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(headers)
            writer.writerows(data)
