import pytest
from fixture.api import PoolApiHelper


# @pytest.fixture
# def api_app():
#     fixture = PoolApiHelper()
#     return fixture


def test_queue(app):
    resp = app.p_api.get_calls()
    assert resp.status_code == 200

    resp = app.p_api.get_pending_calls(app.project)
    assert resp.status_code == 200

    resp = app.p_api.get_queued_calls(app.project, 1, 3)
    assert resp.status_code == 200

    resp = app.p_api.queue_defer(app.project)
    assert resp.status_code == 200

    resp = app.p_api.queue_return(app.project)
    assert resp.status_code == 200

    resp = app.p_api.queue_clean(app.project)
    assert  resp.status_code == 200

    resp = app.p_api.queue_clean_call(app.project, 200)
    assert resp.status_code == 200

    resp = app.p_api.refresh_queue(app.project)
    assert resp.status_code == 200

    resp = app.p_api.pending_count()
    assert  resp.status_code == 200