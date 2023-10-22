import sys

import pytest


@pytest.mark.parametrize('url', ['ya.ru'])
@pytest.mark.parametrize('max_ttl', [30])
@pytest.mark.parametrize('_timeout', [3.0, 5.0])
@pytest.mark.parametrize('_request_timeout', [0.1, 0.2])
@pytest.mark.parametrize('_n', [3, 5])
@pytest.mark.parametrize('_ipv', [4, 6])
def test_traceroute(main_app, logger, url, max_ttl, _timeout, _request_timeout, _n, _ipv):
    sys.stdout = logger

    class Args:
        host = url
        ttl = max_ttl
        timeout = _timeout
        request_timeout = _request_timeout
        seq = None
        size = 60
        n = _n
        ipv = _ipv

    main_app(Args)

    result = logger.log
    assert len(result) > 4  # присутствует минимум первая информационная строка, 2 узла (gateway, целевой узел) и сообщение о том что мы узел
    assert f'Traceroute to {Args.host}' in result[0]
    assert f'Send {Args.n} packets for {Args.size} bytes each' in result[0]
    assert 'Достигнут конечный узел.' in result


def test_not_valid_ipv(main_app):
    class Args:
        host = 'google.com'
        ttl = 123
        timeout = 123
        request_timeout = 123
        seq = None
        size = 123
        n = 123
        ipv = 123

    try:
        main_app(Args)
        assert False
    except ValueError as ex:
        assert True

