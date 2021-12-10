
from tabulate import tabulate


class ConsoleRenderer():
    def render(self, data):
        if len(data) == 0:
            return

        print(tabulate(data, headers=[
            "Source IP",
            "DMARC",
            "DKIM Aligned",
            "SPF Aligned"
        ]))
