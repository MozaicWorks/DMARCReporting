import io

import pytest

from .context import DMARCReporting  # noqa F401
from DMARCReporting.parser import DMARCRuaParser


@pytest.fixture
def not_authenticated():
    return io.StringIO(
        """
        <feedback>
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
        """)


def test_when_not_authenticated(not_authenticated):
    sut = DMARCRuaParser()
    actual = sut.parse(not_authenticated)
    assert [["201.81.220.40", "none", "pass", "fail", "pass", "pass"]] == actual


@pytest.fixture
def authenticated_two_records():
    return io.StringIO(
        """
        <feedback>
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
        """)


def test_when_not_authenticated_having_two_records(authenticated_two_records):
    sut = DMARCRuaParser()
    actual = sut.parse(authenticated_two_records)
    assert [["201.81.220.40", "none", "pass", "fail", "pass", "pass"]] == actual
