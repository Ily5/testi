import pytest
from fixture.api import ApiHelper


@pytest.fixture
def app():
    fixture = ApiHelper()
    return fixture


def test_agents(app):
    resp = app.get_agents()
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert json["id"] == "test"
    assert json["result"][0]["2GIS"] == 37

    resp = app.set_agent_param(63, "name", "test_run")
    assert resp.status_code == 200
    json = app.get_json(resp.json())
    assert json["result"] == "successful"

    resp = app.get_agent_param(63, "name")
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"]["name"] == "test_run"

    resp = app.get_agent_params(63)
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"]["name"] == "test_run"


def test_initial_entity(app):
    resp = app.set_initial_entity(63, "name", "str", 0)
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"] == "successful"

    resp = app.get_initial_entities(63)
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    i = 0
    for x in json["result"]:
        if json["result"][i]["initial_entity_number_cell"] == 0:
            assert json["result"][i]["initial_entity_name"] == "name"
            i += 1

    resp = app.get_initial_entity(63, "name")
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"]["initial_entity_name"] == "name"

    resp = app.delete_initial_entity(63, "name")
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"] == "successful"


def test_output_entity(app):
    resp = app.set_output_entity(63, "name", "str", 0)
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"] == "successful"

    resp = app.get_output_entities(63)
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    i = 0
    for x in json["result"]:
        if json["result"][i]["output_entity_number_cell"] == 0:
            assert json["result"][i]["initial_entity_name"] == "name"
            i += 1

    resp = app.get_output_entity(63, "name")
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"]["output_entity_name"] == "name"

    resp = app.delete_output_entity(63, "name")
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"] == "successful"


def test_data_and_calls(app):
    resp = app.initiate_call(63, "89535750158")
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert type(json["result"]["call_group_id"]) == int

    resp = app.initiate_bulk_calls(63, "9535750158")
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert type(json["result"]["bulk_id"]) == int
    assert json["result"]["calls"][0]["status"] == "successful"

    resp = app.get_data_by_bulk_id(24, 28)
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert type(json["result"][0]["call_id"]) == str

    resp = app.get_data_by_call_group_id(63, 261477)
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert type(json["result"][0]["call_id"]) == str

    resp = app.get_data_by_timeslot(63, "02-10", "05-25")
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert type(json["result"][0]["call_id"]) == str

    resp = app.get_call_records(63, "2eb32a82-955e-11ea-b957-cb87ec06544a.wav")
    json = app.get_json(resp.json())
    assert resp.status_code == 200
    assert type(json["result"]["data"]) == str
