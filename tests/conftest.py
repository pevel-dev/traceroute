import sys
from typing import Callable

import pytest

import main
from traceroute import TracerouteIPv4, TracerouteIPv6


@pytest.fixture()
def traceroute_ipv4():
    return TracerouteIPv4()


@pytest.fixture()
def traceroute_ipv6():
    return TracerouteIPv6()


@pytest.fixture()
def main_app():
    return main.main


class Logger:

    def __init__(self):
        self.console = sys.stdout
        self.log = []

    def write(self, message):
        self.console.write(message)
        self.log.append(message)

    def flush(self):
        self.console.flush()


@pytest.fixture()
def logger():
    return Logger()
