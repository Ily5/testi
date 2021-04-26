from typing import Tuple
import pytest


def pytest_addoption(parser):
    parser.addoption("--max_channels", action="store", default=4)
    parser.addoption("--min_channels", action="store", default=2)
    parser.addoption("--step", action="store", default=2)


@pytest.fixture()
def get_step_max_min(request) -> Tuple[int, int, int]:
    return (
        int(request.config.getoption("--step")),
        int(request.config.getoption("--max_channels")),
        int(request.config.getoption("--min_channels")),
    )
