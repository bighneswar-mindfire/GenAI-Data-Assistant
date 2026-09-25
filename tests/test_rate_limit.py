from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.rate_limit import MAX_REQUESTS_PER_WINDOW, _requests, rate_limit


def _make_request(ip: str):
    request = MagicMock()
    request.client.host = ip
    return request


@pytest.fixture(autouse=True)
def clear_rate_limit_state():
    _requests.clear()
    yield
    _requests.clear()


def test_allows_requests_up_to_limit():
    request = _make_request("10.0.0.1")
    for _ in range(MAX_REQUESTS_PER_WINDOW):
        rate_limit(request)


def test_blocks_requests_over_limit():
    request = _make_request("10.0.0.2")
    for _ in range(MAX_REQUESTS_PER_WINDOW):
        rate_limit(request)

    with pytest.raises(HTTPException) as exc_info:
        rate_limit(request)
    assert exc_info.value.status_code == 429


def test_different_clients_are_independent():
    request_a = _make_request("10.0.0.3")
    request_b = _make_request("10.0.0.4")

    for _ in range(MAX_REQUESTS_PER_WINDOW):
        rate_limit(request_a)

    rate_limit(request_b)
