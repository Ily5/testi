import pytest
from fixture.api import PoolApiHelper


@pytest.fixture
def api_app():
    fixture = PoolApiHelper()
    return fixture


def test_queue(api_app):
    resp = api_app.get_calls()
    assert resp.status_code == 200

    resp = api_app.get_pending_calls(63)
    assert resp.status_code == 200

    resp = api_app.get_queued_calls(63,1,3)
    assert resp.status_code == 200

    resp = api_app.queue_defer(63)
    assert resp.status_code == 200

    resp = api_app.queue_return(63)
    assert resp.status_code == 200

    resp = api_app.queue_clean(63)
    assert  resp.status_code == 200

    resp = api_app.queue_clean_call(63,200)
    assert resp.status_code == 200

    resp = api_app.refresh_queue(63)
    assert resp.status_code == 200

    resp = api_app.pending_count()
    assert  resp.status_code == 200