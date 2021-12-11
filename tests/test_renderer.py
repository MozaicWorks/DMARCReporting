import io
import sys

from .context import DMARCReporting  # noqa F401
from DMARCReporting.renderer import ConsoleRenderer


def test_render_when_no_data():
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


def test_render_when_data():
    try:
        output = io.StringIO()
        sys.stdout = output

        data = [
            ["source_ip", "dmarc_disposition", "dkim_aligned", "dkim_auth", "spf_aligned", "spf_auth"]
        ]

        sut = ConsoleRenderer()
        sut.render("ruareport_file", data)

        expected = (
            "\n"
            "ruareport_file\n"
            "Source IP    DMARC              DKIM Aligned    DKIM Authenticated    SPF Aligned    SPF Authenticated\n"
            "-----------  -----------------  --------------  --------------------  -------------  -------------------\n"
            "source_ip    dmarc_disposition  dkim_aligned    dkim_auth             spf_aligned    spf_auth\n"
        )
        actual = output.getvalue()

        assert expected == actual

    finally:
        sys.stdout = sys.__stdout__
