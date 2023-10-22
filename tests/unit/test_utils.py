import pytest
from unittest.mock import patch
import socket

from utils import get_ip_from_host, get_host_from_ip


@pytest.mark.parametrize('return_value', ['8.8.8.8'])
@pytest.mark.parametrize('host', ['google.com'])
def test_get_ip_from_host(return_value, host):
    with patch.object(socket, 'gethostbyname', return_value=return_value) as mock:
        result = get_ip_from_host(host)
        assert result == return_value


@pytest.mark.parametrize('return_value', [None])
@pytest.mark.parametrize('host', ['google.com'])
def test_get_ip_from_host_error(return_value, host):
    with (patch.object(socket, 'gethostbyname', side_effect=socket.gaierror) as mock):
        result = get_ip_from_host(host)
        assert result == return_value


@pytest.mark.parametrize('return_value', [['google.com']])
@pytest.mark.parametrize('host', ['8.8.8.8'])
def test_get_host_from_ip_host(return_value, host):
    with patch.object(socket, 'gethostbyaddr', return_value=return_value) as mock:
        result = get_host_from_ip(host)
        assert result == return_value[0]


@pytest.mark.parametrize('return_value', [None])
@pytest.mark.parametrize('host', ['8.8.8.8'])
def test_get_host_from_ip_error(return_value, host):
    with patch.object(socket, 'gethostbyaddr', side_effect=socket.herror) as mock:
        result = get_host_from_ip(host)
        assert result == return_value
