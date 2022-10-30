import os

from .context import DMARCReporting  # noqa F401
from DMARCReporting.renderer import CSVRenderer


def test_render_without_data():
    try:
        csv_file = "tmp/render_without_data.csv"
        if not os.path.exists("tmp"):
            os.makedirs("tmp")

        data = []

        sut = CSVRenderer()
        sut.render(csv_file, data)

        expected = "Source IP,Source Host,Payload From (From:),Envelop From (MAIL FROM),DMARC,DKIM Align,DKIM Auth,SPF Align,SPF Auth,Count,File\n"  # noqa E501
        actual = open(csv_file, "r").read()

        assert expected == actual
    finally:
        os.remove(csv_file)


def test_render_with_data():
    try:
        csv_file = "tmp/render_with_data.csv"
        if not os.path.exists("tmp"):
            os.makedirs("tmp")

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

        sut = CSVRenderer()
        sut.render(csv_file, data)

        expected = (
            "Source IP,Source Host,Payload From (From:),Envelop From (MAIL FROM),DMARC,DKIM Align,DKIM Auth,SPF Align,SPF Auth,Count,File\n"  # noqa E501
            "source_ip,source_host,payload_from,envelop_from,dmarc_disposition,dkim_aligned,dkim_auth,spf_aligned,spf_auth,42,ruareport_file\n"  # noqa E501
        )
        actual = actual = open(csv_file, "r").read()

        assert expected == actual

    finally:
        os.remove(csv_file)
