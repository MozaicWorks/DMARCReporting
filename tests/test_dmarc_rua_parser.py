import io
import pytest

from .context import DMARCReporting  # noqa F401
from DMARCReporting.dmarc_rua_parser import DMARCRuaParser


def rua_report(disposition):
    return io.StringIO(
        """
        <feedback>
            <record>
                <row>
                <source_ip>101.0.122.38</source_ip>
                <count>1</count>
                <policy_evaluated>
                    <disposition>{disposition}</disposition>
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
        """.format(disposition=disposition))


@pytest.fixture
def rua_report_quarantine():
    return rua_report("quarantine")


@pytest.fixture
def rua_report_none():
    return rua_report("none")


def test_when_dmarc_disposition_quarantine(rua_report_quarantine):
    sut = DMARCRuaParser()
    actual = sut.execute(rua_report_quarantine)
    assert [["101.0.122.38", "quarantine"]] == actual


def test_when_dmarc_disposition_none(rua_report_none):
    sut = DMARCRuaParser()
    actual = sut.execute(rua_report_none)
    assert [] == actual
