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
            "-------------  ------------------------------  ----------------------  --------------------------  -------  ------------  -----------  -----------  ----------  -------  ------------------------\n"  # noqa E501
            "80.96.161.193  Unknown host                    bellous.com             bellous.com                 none     pass          pass         fail         fail              3  ./samples/report.xml.gz\n"  # noqa E501
            "208.90.221.45  208-90-221-45.static.flhsi.com  bellous.com             calendar.yambo.com          none     pass          pass         fail         pass             32  ./samples/report.xml.gz\n"  # noqa E501
            "80.96.161.193  Unknown host                    disicious.com           disicious.com               none     pass          pass         fail         fail              3  ./samples/report.xml.zip\n"  # noqa E501
            "208.90.221.45  208-90-221-45.static.flhsi.com  disicious.com           calendar.trumbee.com        none     pass          pass         fail         pass             32  ./samples/report.xml.zip\n"  # noqa E501
        )
        actual = output.getvalue()

        assert expected == actual

    finally:
        sys.stdout = sys.__stdout__


@patch('socket.gethostbyaddr')
def test_render_all(gethostbyaddr_mock):
    gethostbyaddr_mock.side_effect = [
        ("smtp.bellous.com", [], []),
        ("smtp.bellous.com", [], []),
        ("smtp.bellous.com", [], []),
        ("smtp.bellous.com", [], []),
        ("smtp.bellous.com", [], []),
        ("Unknown host", [], []),
        ("208-90-221-45.static.flhsi.com", [], []),
        ("smtp.disicious.com", [], []),
        ("smtp.disicious.com", [], []),
        ("smtp.disicious.com", [], []),
        ("smtp.disicious.com", [], []),
        ("smtp.disicious.com", [], []),
        ("Unknown host", [], []),
        ("208-90-221-45.static.flhsi.com", [], []),
        ("smtp.abbove.com", [], []),
        ("smtp.abbove.com", [], []),
        ("smtp.abbove.com", [], []),
        ("smtp.abbove.com", [], []),
        ("smtp.abbove.com", [], []),
    ]
    try:
        output = io.StringIO()
        sys.stdout = output

        cli = CLI()
        cli.execute("./samples", csv_output_file=None, show_all=True)

        expected = (
            "Source IP       Source Host                     Payload From (From:)    Envelop From (MAIL FROM)    DMARC    DKIM Align    DKIM Auth    SPF Align    SPF Auth      Count  File\n"  # noqa E501
            "--------------  ------------------------------  ----------------------  --------------------------  -------  ------------  -----------  -----------  ----------  -------  ----------------------------------\n"  # noqa E501
            "207.90.221.45   smtp.bellous.com                bellous.com             bellous.com                 none     pass          pass         pass         pass              8  ./samples/report.xml.gz\n"  # noqa E501
            "207.86.220.40   smtp.bellous.com                bellous.com             bellous.com                 none     pass          pass         pass         pass             22  ./samples/report.xml.gz\n"  # noqa E501
            "198.3.186.1     smtp.bellous.com                bellous.com             mail.bellous.com            none     pass          pass         pass         pass             68  ./samples/report.xml.gz\n"  # noqa E501
            "210.81.222.70   smtp.bellous.com                bellous.com             bellous.com                 none     pass          pass         pass         pass              6  ./samples/report.xml.gz\n"  # noqa E501
            "197.3.177.11    smtp.bellous.com                bellous.com             mail.bellous.com            none     pass          pass         pass         pass             81  ./samples/report.xml.gz\n"  # noqa E501
            "80.96.161.193   Unknown host                    bellous.com             bellous.com                 none     pass          pass         fail         fail              3  ./samples/report.xml.gz\n"  # noqa E501
            "208.90.221.45   208-90-221-45.static.flhsi.com  bellous.com             calendar.yambo.com          none     pass          pass         fail         pass             32  ./samples/report.xml.gz\n"  # noqa E501
            "207.90.221.45   smtp.disicious.com              disicious.com           disicious.com               none     pass          pass         pass         pass              8  ./samples/report.xml.zip\n"  # noqa E501
            "207.86.220.40   smtp.disicious.com              disicious.com           disicious.com               none     pass          pass         pass         pass             22  ./samples/report.xml.zip\n"  # noqa E501
            "198.3.186.1     smtp.disicious.com              disicious.com           mail.disicious.com          none     pass          pass         pass         pass             68  ./samples/report.xml.zip\n"  # noqa E501
            "210.81.222.70   smtp.disicious.com              disicious.com           disicious.com               none     pass          pass         pass         pass              6  ./samples/report.xml.zip\n"  # noqa E501
            "197.3.177.11    smtp.disicious.com              disicious.com           mail.disicious.com          none     pass          pass         pass         pass             81  ./samples/report.xml.zip\n"  # noqa E501
            "80.96.161.193   Unknown host                    disicious.com           disicious.com               none     pass          pass         fail         fail              3  ./samples/report.xml.zip\n"  # noqa E501
            "208.90.221.45   208-90-221-45.static.flhsi.com  disicious.com           calendar.trumbee.com        none     pass          pass         fail         pass             32  ./samples/report.xml.zip\n"  # noqa E501
            "209.85.208.179  smtp.abbove.com                 abbove.com              abbove.com                  none     pass          pass         pass         pass              1  ./samples/trailing_garbage1.xml.gz\n"  # noqa E501
            "209.85.208.170  smtp.abbove.com                 abbove.com              abbove.com                  none     pass          pass         pass         pass              1  ./samples/trailing_garbage1.xml.gz\n"  # noqa E501
            "209.85.208.181  smtp.abbove.com                 abbove.com              abbove.com                  none     pass          pass         pass         pass              1  ./samples/trailing_garbage1.xml.gz\n"  # noqa E501
            "209.85.219.176  smtp.abbove.com                 abbove.com              abbove.com                  none     pass          pass         pass         pass              1  ./samples/trailing_garbage2.xml.gz\n"  # noqa E501
            "209.85.219.178  smtp.abbove.com                 abbove.com              abbove.com                  none     pass          pass         pass         pass              1  ./samples/trailing_garbage2.xml.gz\n"  # noqa E501
        )
        actual = output.getvalue()

        assert expected == actual

    finally:
        sys.stdout = sys.__stdout__
