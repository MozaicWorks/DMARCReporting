import os
import sys
import io
import time
from unittest.mock import patch

import pytest

from .context import DMARCReporting  # noqa F401
from DMARCReporting.cli import CLI

test_tz = 'Europe/Brussels'
env_tz = ''


@pytest.fixture
def setup_timezone():
    env_tz = time.tzname[0]
    print()
    print(f"save current timezone: {env_tz}")
    print(f"set timezone for tests to {test_tz}")
    os.environ['TZ'] = test_tz
    time.tzset()
    print(f"timezone is now {time.tzname[0]}")
    yield
    print()
    print(f"reset timezone back to {env_tz}")
    os.environ['TZ'] = env_tz
    time.tzset()
    print(f"timezone is now {time.tzname[0]}")


@patch('socket.gethostbyaddr')
def test_render(gethostbyaddr_mock, setup_timezone):
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
            "Begin Date           End Date             Source IP      Source Host                     Payload From (From:)    Envelop From (MAIL FROM)    DMARC    DKIM Align    DKIM Auth    SPF Align    SPF Auth      Count  File\n"  # noqa E501
            "-------------------  -------------------  -------------  ------------------------------  ----------------------  --------------------------  -------  ------------  -----------  -----------  ----------  -------  ------------------------\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  80.96.161.193  Unknown host                    bellous.com             bellous.com                 none     pass          pass         fail         fail              3  ./samples/report.xml.gz\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  208.90.221.45  208-90-221-45.static.flhsi.com  bellous.com             calendar.yambo.com          none     pass          pass         fail         pass             32  ./samples/report.xml.gz\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  80.96.161.193  Unknown host                    disicious.com           disicious.com               none     pass          pass         fail         fail              3  ./samples/report.xml.zip\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  208.90.221.45  208-90-221-45.static.flhsi.com  disicious.com           calendar.trumbee.com        none     pass          pass         fail         pass             32  ./samples/report.xml.zip\n"  # noqa E501
        )
        actual = output.getvalue()

        assert expected == actual

    finally:
        sys.stdout = sys.__stdout__


@patch('socket.gethostbyaddr')
def test_render_all(gethostbyaddr_mock, setup_timezone):
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
            "Begin Date           End Date             Source IP       Source Host                     Payload From (From:)    Envelop From (MAIL FROM)    DMARC    DKIM Align    DKIM Auth    SPF Align    SPF Auth      Count  File\n"  # noqa E501
            "-------------------  -------------------  --------------  ------------------------------  ----------------------  --------------------------  -------  ------------  -----------  -----------  ----------  -------  ----------------------------------\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  207.90.221.45   smtp.bellous.com                bellous.com             bellous.com                 none     pass          pass         pass         pass              8  ./samples/report.xml.gz\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  207.86.220.40   smtp.bellous.com                bellous.com             bellous.com                 none     pass          pass         pass         pass             22  ./samples/report.xml.gz\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  198.3.186.1     smtp.bellous.com                bellous.com             mail.bellous.com            none     pass          pass         pass         pass             68  ./samples/report.xml.gz\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  210.81.222.70   smtp.bellous.com                bellous.com             bellous.com                 none     pass          pass         pass         pass              6  ./samples/report.xml.gz\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  197.3.177.11    smtp.bellous.com                bellous.com             mail.bellous.com            none     pass          pass         pass         pass             81  ./samples/report.xml.gz\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  80.96.161.193   Unknown host                    bellous.com             bellous.com                 none     pass          pass         fail         fail              3  ./samples/report.xml.gz\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  208.90.221.45   208-90-221-45.static.flhsi.com  bellous.com             calendar.yambo.com          none     pass          pass         fail         pass             32  ./samples/report.xml.gz\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  207.90.221.45   smtp.disicious.com              disicious.com           disicious.com               none     pass          pass         pass         pass              8  ./samples/report.xml.zip\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  207.86.220.40   smtp.disicious.com              disicious.com           disicious.com               none     pass          pass         pass         pass             22  ./samples/report.xml.zip\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  198.3.186.1     smtp.disicious.com              disicious.com           mail.disicious.com          none     pass          pass         pass         pass             68  ./samples/report.xml.zip\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  210.81.222.70   smtp.disicious.com              disicious.com           disicious.com               none     pass          pass         pass         pass              6  ./samples/report.xml.zip\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  197.3.177.11    smtp.disicious.com              disicious.com           mail.disicious.com          none     pass          pass         pass         pass             81  ./samples/report.xml.zip\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  80.96.161.193   Unknown host                    disicious.com           disicious.com               none     pass          pass         fail         fail              3  ./samples/report.xml.zip\n"  # noqa E501
            "2021-11-25T01:00:00  2021-11-26T00:59:59  208.90.221.45   208-90-221-45.static.flhsi.com  disicious.com           calendar.trumbee.com        none     pass          pass         fail         pass             32  ./samples/report.xml.zip\n"  # noqa E501
            "2023-08-30T02:00:00  2023-08-31T01:59:59  209.85.208.179  smtp.abbove.com                 abbove.com              abbove.com                  none     pass          pass         pass         pass              1  ./samples/trailing_garbage1.xml.gz\n"  # noqa E501
            "2023-08-30T02:00:00  2023-08-31T01:59:59  209.85.208.170  smtp.abbove.com                 abbove.com              abbove.com                  none     pass          pass         pass         pass              1  ./samples/trailing_garbage1.xml.gz\n"  # noqa E501
            "2023-08-30T02:00:00  2023-08-31T01:59:59  209.85.208.181  smtp.abbove.com                 abbove.com              abbove.com                  none     pass          pass         pass         pass              1  ./samples/trailing_garbage1.xml.gz\n"  # noqa E501
            "2023-08-31T02:00:00  2023-09-01T01:59:59  209.85.219.176  smtp.abbove.com                 abbove.com              abbove.com                  none     pass          pass         pass         pass              1  ./samples/trailing_garbage2.xml.gz\n"  # noqa E501
            "2023-08-31T02:00:00  2023-09-01T01:59:59  209.85.219.178  smtp.abbove.com                 abbove.com              abbove.com                  none     pass          pass         pass         pass              1  ./samples/trailing_garbage2.xml.gz\n"  # noqa E501
        )
        actual = output.getvalue()

        assert expected == actual

    finally:
        sys.stdout = sys.__stdout__
