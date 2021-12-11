
from tabulate import tabulate


class ConsoleRenderer():
    def render(self, file, data):
        if len(data) == 0:
            return

        print()
        print(file)
        print(tabulate(data, headers=[
            "Source IP",
            "DMARC",
            "DKIM Aligned",
            "DKIM Authenticated",
            "SPF Aligned",
            "SPF Authenticated"
        ]))
