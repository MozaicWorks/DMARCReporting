import io
import sys

from .context import DMARCReporting  # noqa F401
from DMARCReporting.renderer import ConsoleRenderer


def test_render():
    try:
        output = io.StringIO()
        sys.stdout = output

        sut = ConsoleRenderer()
        sut.render([["source_ip", "dmarc_disposition", "dkim_aligned", "spf_aligned"]])

        expected = (
            "Source IP    DMARC              DKIM Aligned    SPF Aligned\n"
            "-----------  -----------------  --------------  -------------\n"
            "source_ip    dmarc_disposition  dkim_aligned    spf_aligned\n"
        )
        actual = output.getvalue()

        assert expected == actual

    finally:
        sys.stdout = sys.__stdout__
