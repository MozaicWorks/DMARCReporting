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
                    <spf>
                        <domain>example.com</domain>
                        <result>fail</result>
                    </spf>
                </auth_results>
            </record>
        </feedback>
        """)


def test_when_spf_not_authenticated(not_authenticated):
    sut = DMARCRuaParser()
    actual = sut.parse(not_authenticated)
    assert [["201.81.220.40", "email.com", "example.com", "none", "pass", "pass", "pass", "fail"]] == actual
