import io
import pytest

from .context import DMARCReporting  # noqa F401
from DMARCReporting.dmarc_rua_parser import DMARCRuaParser


def rua_report(disposition="none", spf_aligned="pass"):
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
                    <spf>{spf_aligned}</spf>
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
        """.format(disposition=disposition, spf_aligned=spf_aligned))


@pytest.fixture
def rua_report_quarantine():
    return rua_report(disposition="quarantine", spf_aligned="fail")


@pytest.fixture
def rua_report_none():
    return rua_report()


@pytest.fixture
def rua_report_reject():
    return rua_report(disposition="reject", spf_aligned="fail")


@pytest.fixture
def rua_report_spf_aligned():
    return rua_report()


@pytest.fixture
def rua_report_spf_not_aligned():
    return rua_report(spf_aligned="fail")


def test_when_dmarc_disposition_quarantine(rua_report_quarantine):
    sut = DMARCRuaParser()
    actual = sut.execute(rua_report_quarantine)
    assert [["101.0.122.38", "quarantine", "fail"]] == actual


def test_when_dmarc_disposition_none(rua_report_none):
    sut = DMARCRuaParser()
    actual = sut.execute(rua_report_none)
    assert [] == actual


def test_when_dmarc_disposition_reject(rua_report_reject):
    sut = DMARCRuaParser()
    actual = sut.execute(rua_report_reject)
    assert [["101.0.122.38", "reject", "fail"]] == actual


def test_when_spf_aligned(rua_report_spf_aligned):
    sut = DMARCRuaParser()
    actual = sut.execute(rua_report_spf_aligned)
    assert [] == actual


def test_when_spf_not_aligned(rua_report_spf_not_aligned):
    sut = DMARCRuaParser()
    actual = sut.execute(rua_report_spf_not_aligned)
    assert [["101.0.122.38", "none", "fail"]] == actual
