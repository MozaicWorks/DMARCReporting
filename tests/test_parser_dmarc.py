import os
import io
import time

import pytest

from .context import DMARCReporting  # noqa F401
from DMARCReporting.parser import DMARCRuaParser


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


def rua_report(disposition="none", spf_aligned="pass", dkim_aligned="pass"):
    return io.StringIO(
        """
        <feedback>
            <report_metadata>
                <date_range>
                    <begin>1703237232</begin>
                    <end>1703280196</end>
                </date_range>
            </report_metadata>
            <record>
                <row>
                <source_ip>101.0.122.38</source_ip>
                <count>1</count>
                <policy_evaluated>
                    <disposition>{disposition}</disposition>
                    <dkim>{dkim_aligned}</dkim>
                    <spf>{spf_aligned}</spf>
                </policy_evaluated>
                </row>
                <identifiers>
                <envelope_to>recipient.org</envelope_to>
                <envelope_from>sender.org</envelope_from>
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
        """.format(
            disposition=disposition, spf_aligned=spf_aligned, dkim_aligned=dkim_aligned
        )
    )


@pytest.fixture
def rua_report_quarantine():
    return rua_report(disposition="quarantine", spf_aligned="fail", dkim_aligned="fail")


@pytest.fixture
def rua_report_none():
    return rua_report()


@pytest.fixture
def rua_report_reject():
    return rua_report(disposition="reject", spf_aligned="fail", dkim_aligned="fail")


@pytest.fixture
def rua_report_spf_and_dkim_aligned():
    return rua_report()


@pytest.fixture
def rua_report_spf_not_aligned():
    return rua_report(spf_aligned="fail")


@pytest.fixture
def rua_report_dkim_not_aligned():
    return rua_report(dkim_aligned="fail")


class DNSStub:
    def reverse_name(self, ipv4):
        return "mail.email.com"


def test_when_dmarc_disposition_quarantine(rua_report_quarantine, setup_timezone):
    sut = DMARCRuaParser(DNSStub())
    actual = sut.parse(rua_report_quarantine)
    expected = [
        [
            "2023-12-22T10:27:12",
            "2023-12-22T22:23:16",
            "101.0.122.38",
            "mail.email.com",
            "email.com",
            "example.com",
            "quarantine",
            "fail",
            "pass",
            "fail",
            "pass",
            1,
        ]
    ]
    assert expected == actual


def test_when_dmarc_disposition_none(rua_report_none, setup_timezone):
    sut = DMARCRuaParser(DNSStub())
    actual = sut.parse(rua_report_none)
    assert [] == actual


def test_when_dmarc_disposition_reject(rua_report_reject, setup_timezone):
    sut = DMARCRuaParser(DNSStub())
    actual = sut.parse(rua_report_reject)
    expected = [
        [
            "2023-12-22T10:27:12",
            "2023-12-22T22:23:16",
            "101.0.122.38",
            "mail.email.com",
            "email.com",
            "example.com",
            "reject",
            "fail",
            "pass",
            "fail",
            "pass",
            1,
        ]
    ]
    assert expected == actual


def test_when_spf_and_dkim_aligned(rua_report_spf_and_dkim_aligned, setup_timezone):
    sut = DMARCRuaParser(DNSStub())
    actual = sut.parse(rua_report_spf_and_dkim_aligned)
    assert [] == actual


def test_when_spf_not_aligned(rua_report_spf_not_aligned, setup_timezone):
    sut = DMARCRuaParser(DNSStub())
    actual = sut.parse(rua_report_spf_not_aligned)
    expected = [
        [
            "2023-12-22T10:27:12",
            "2023-12-22T22:23:16",
            "101.0.122.38",
            "mail.email.com",
            "email.com",
            "example.com",
            "none",
            "pass",
            "pass",
            "fail",
            "pass",
            1,
        ]
    ]
    assert expected == actual


def test_when_dkim_not_aligned(rua_report_dkim_not_aligned, setup_timezone):
    sut = DMARCRuaParser(DNSStub())
    actual = sut.parse(rua_report_dkim_not_aligned)
    expected = [
        [
            "2023-12-22T10:27:12",
            "2023-12-22T22:23:16",
            "101.0.122.38",
            "mail.email.com",
            "email.com",
            "example.com",
            "none",
            "fail",
            "pass",
            "pass",
            "pass",
            1,
        ]
    ]
    assert expected == actual
