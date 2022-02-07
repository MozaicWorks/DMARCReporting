import io
import sys

from .context import DMARCReporting  # noqa F401
from DMARCReporting.cli import CLI


def test_render():
    try:
        output = io.StringIO()
        sys.stdout = output

        cli = CLI()
        cli.execute("./samples")

        expected = (
            "\n"
            "report.xml.gz\n"
            "Source IP      Source Host                     Payload From (From:)    Envelop From (MAIL FROM)    DMARC    DKIM Align    DKIM Auth    SPF Align    SPF Auth\n"  # noqa E501
            "-------------  ------------------------------  ----------------------  --------------------------  -------  ------------  -----------  -----------  ----------\n"  # noqa E501
            "80.96.161.193  Unknown host                    bellous.com             bellous.com                 none     pass          pass         fail         fail\n"  # noqa E501
            "208.90.221.45  208-90-221-45.static.flhsi.com  bellous.com             calendar.yambo.com          none     pass          pass         fail         pass\n"  # noqa E501
        )
        actual = output.getvalue()

        assert expected == actual

    finally:
        sys.stdout = sys.__stdout__
