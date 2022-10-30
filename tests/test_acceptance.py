import io
import sys
from unittest.mock import patch

from .context import DMARCReporting  # noqa F401
from DMARCReporting.cli import CLI


@patch('socket.gethostbyaddr')
def test_render(gethostbyaddr_mock):
    gethostbyaddr_mock.side_effect = [
        ("Unknown host", [], []),
        ("208-90-221-45.static.flhsi.com", [], []),
        ("Unknown host", [], []),
        ("208-90-221-45.static.flhsi.com", [], []),
    ]
    try:
        output = io.StringIO()
        sys.stdout = output

        cli = CLI()
        cli.execute("./samples")

        expected = (
            "Source IP      Source Host                     Payload From (From:)    Envelop From (MAIL FROM)    DMARC    DKIM Align    DKIM Auth    SPF Align    SPF Auth      Count  File\n"  # noqa E501
            "-------------  ------------------------------  ----------------------  --------------------------  -------  ------------  -----------  -----------  ----------  -------  --------------\n"  # noqa E501
            "80.96.161.193  Unknown host                    bellous.com             bellous.com                 none     pass          pass         fail         fail              3  report.xml.gz\n"  # noqa E501
            "208.90.221.45  208-90-221-45.static.flhsi.com  bellous.com             calendar.yambo.com          none     pass          pass         fail         pass             32  report.xml.gz\n"  # noqa E501
            "80.96.161.193  Unknown host                    disicious.com           disicious.com               none     pass          pass         fail         fail              3  report.xml.zip\n"  # noqa E501
            "208.90.221.45  208-90-221-45.static.flhsi.com  disicious.com           calendar.trumbee.com        none     pass          pass         fail         pass             32  report.xml.zip\n"  # noqa E501
        )
        actual = output.getvalue()

        assert expected == actual

    finally:
        sys.stdout = sys.__stdout__
