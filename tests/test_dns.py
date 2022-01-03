
import socket
from unittest.mock import patch

from .context import DMARCReporting  # noqa F401
from DMARCReporting.dns import DNS


@patch('socket.gethostbyaddr')
def test_reversename(gethostbyaddr_mock):
    gethostbyaddr_mock.return_value = ('ns.tridel.com', [], [])

    dns = DNS()
    assert 'ns.tridel.com' == dns.reverse_name('1.2.3.4')


@patch('socket.gethostbyaddr')
def test_reversename_raise_exception(gethostbyaddr_mock):
    error_msg = 'Unknown host'
    gethostbyaddr_mock.side_effect = socket.herror(1, error_msg)

    dns = DNS()
    assert error_msg == dns.reverse_name('1.2.3.4')
