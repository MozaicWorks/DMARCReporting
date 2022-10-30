import io
import sys

from .context import DMARCReporting  # noqa F401
from DMARCReporting.renderer import ConsoleRenderer


def test_render_without_data():
    try:
        output = io.StringIO()
        sys.stdout = output

        data = []

        sut = ConsoleRenderer()
        sut.render("ruareport_file", data)

        expected = ""
        actual = output.getvalue()

        assert expected == actual

    finally:
        sys.stdout = sys.__stdout__


def test_render_with_data():
    try:
        output = io.StringIO()
        sys.stdout = output

        data = [
            [
                "source_ip",
                "source_host",
                "payload_from",
                "envelop_from",
                "dmarc_disposition",
                "dkim_aligned",
                "dkim_auth",
                "spf_aligned",
                "spf_auth",
                42,
                "ruareport_file",
            ]
        ]

        sut = ConsoleRenderer()
        sut.render("ruareport_file", data)

        expected = (
            "Source IP    Source Host    Payload From (From:)    Envelop From (MAIL FROM)    DMARC              DKIM Align    DKIM Auth    SPF Align    SPF Auth      Count  File\n"  # noqa E501
            "-----------  -------------  ----------------------  --------------------------  -----------------  ------------  -----------  -----------  ----------  -------  --------------\n"  # noqa E501
            "source_ip    source_host    payload_from            envelop_from                dmarc_disposition  dkim_aligned  dkim_auth    spf_aligned  spf_auth         42  ruareport_file\n"  # noqa E501
        )
        actual = output.getvalue()

        assert expected == actual

    finally:
        sys.stdout = sys.__stdout__
