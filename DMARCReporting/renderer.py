
from tabulate import tabulate


class ConsoleRenderer():
    def render(self, data):
        print(tabulate(data, headers=[
            "Source IP",
            "DMARC",
            "DKIM Aligned",
            "SPF Aligned"
        ]))
