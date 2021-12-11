import io
import sys

from .context import DMARCReporting  # noqa F401
from DMARCReporting.cli import CLI


def test_render_when_data():
    try:
        output = io.StringIO()
        sys.stdout = output

        cli = CLI()
        cli.execute("./data")

        expected = (
            "\n"
            "report.xml\n"
            "Source IP      DMARC    DKIM Align    DKIM Auth    SPF Align    SPF Auth\n"
            "-------------  -------  ------------  -----------  -----------  ----------\n"
            "80.96.161.193  none     pass          pass         fail         fail\n"
            "207.90.221.45  none     pass          pass         fail         pass\n"
        )
        actual = output.getvalue()

        assert expected == actual

    finally:
        sys.stdout = sys.__stdout__
