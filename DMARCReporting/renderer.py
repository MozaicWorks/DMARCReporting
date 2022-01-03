
from tabulate import tabulate


class ConsoleRenderer:
    def render(self, file, data):
        if len(data) == 0:
            return

        print()
        print(file)
        print(tabulate(data, headers=[
            "Source IP",
            "Source Host",
            "Payload From (From:)",
            "Envelop From (MAIL FROM)",
            "DMARC",
            "DKIM Align",
            "DKIM Auth",
            "SPF Align",
            "SPF Auth"
        ]))
