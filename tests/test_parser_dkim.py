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


@pytest.fixture
def not_authenticated():
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
                <source_ip>201.81.220.40</source_ip>
                <count>1</count>
                <policy_evaluated>
                    <disposition>none</disposition>
                    <dkim>pass</dkim>
                    <spf>pass</spf>
                </policy_evaluated>
                </row>
                <identifiers>
                <header_from>email.com</header_from>
                <envelope_to>recipient.org</envelope_to>
                <envelope_from>sender.org</envelope_from>
                </identifiers>
                <auth_results>
                    <dkim>
                        <domain>example.com</domain>
                        <result>fail</result>
                        <selector>default</selector>
                    </dkim>
                </auth_results>
            </record>
        </feedback>
        """
    )


class DNSStub:
    def reverse_name(self, ipv4):
        return "mail.email.com"


def test_when_not_authenticated(not_authenticated, setup_timezone):
    sut = DMARCRuaParser(DNSStub())
    actual = sut.parse(not_authenticated)
    expected = [
        [
            "2023-12-22T10:27:12",
            "2023-12-22T22:23:16",
            "201.81.220.40",
            "mail.email.com",
            "email.com",
            "",
            "none",
            "pass",
            "fail",
            "pass",
            "pass",
            1,
        ]
    ]
    assert expected == actual


@pytest.fixture
def authenticated_two_records():
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
                <source_ip>201.81.220.40</source_ip>
                <count>1</count>
                <policy_evaluated>
                    <disposition>none</disposition>
                    <dkim>pass</dkim>
                    <spf>pass</spf>
                </policy_evaluated>
                </row>
                <identifiers>
                <header_from>email.com</header_from>
                <envelope_to>recipient.org</envelope_to>
                <envelope_from>sender.org</envelope_from>
                </identifiers>
                <auth_results>
                    <dkim>
                        <domain>example.com</domain>
                        <result>pass</result>
                        <selector>default</selector>
                    </dkim>
                    <dkim>
                        <domain>foo.com</domain>
                        <result>fail</result>
                        <selector>foo</selector>
                    </dkim>
                </auth_results>
            </record>
        </feedback>
        """
    )


def test_when_not_authenticated_having_two_records(authenticated_two_records, setup_timezone):
    sut = DMARCRuaParser(DNSStub())
    actual = sut.parse(authenticated_two_records)
    expected = [
        [
            "2023-12-22T10:27:12",
            "2023-12-22T22:23:16",
            "201.81.220.40",
            "mail.email.com",
            "email.com",
            "",
            "none",
            "pass",
            "fail",
            "pass",
            "pass",
            1,
        ]
    ]
    assert expected == actual
