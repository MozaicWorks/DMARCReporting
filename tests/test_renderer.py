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
        sut.render(data)

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
            ["source_ip", "dmarc_disposition", "dkim_aligned", "spf_aligned"]
        ]

        sut = ConsoleRenderer()
        sut.render(data)

        expected = (
            "Source IP    DMARC              DKIM Aligned    SPF Aligned\n"
            "-----------  -----------------  --------------  -------------\n"
            "source_ip    dmarc_disposition  dkim_aligned    spf_aligned\n"
        )
        actual = output.getvalue()

        assert expected == actual

    finally:
        sys.stdout = sys.__stdout__