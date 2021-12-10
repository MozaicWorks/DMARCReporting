import io
import pytest

from .context import DMARCReporting  # noqa F401
from DMARCReporting.dmarc_rua_parser import DMARCRuaParser


@pytest.fixture
def rua_report_quarantine():
    return io.BytesIO(
        b"""
        <feedback>
            <record>
                <row>
                <source_ip>101.0.122.38</source_ip>
                <count>1</count>
                <policy_evaluated>
                    <disposition>quarantine</disposition>
                    <dkim>fail</dkim>
                    <spf>fail</spf>
                </policy_evaluated>
                </row>
                <identifiers>
                <header_from>email.com</header_from>
                </identifiers>
                <auth_results>
                <dkim>
                    <domain>example.com</domain>
                    <result>pass</result>
                    <selector>default</selector>
                </dkim>
                <spf>
                    <domain>example.com</domain>
                    <result>pass</result>
                </spf>
                </auth_results>
            </record>
        </feedback>
        """)


def test_when_dmarc_disposition_quarantine(rua_report_quarantine):
    sut = DMARCRuaParser()
    actual = sut.execute(rua_report_quarantine)
    assert [["101.0.122.38", "quarantine"]] == actual
