

def test_agents(app):
    resp = app.api.get_agents()
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert json["id"] == "test"
    assert json["result"][0]["2GIS"] == 37

    resp = app.api.set_agent_param(63, "name", "test_run")
    assert resp.status_code == 200
    json = app.api.get_json(resp.json())
    assert json["result"] == "successful"

    resp = app.api.get_agent_param(63, "name")
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"]["name"] == "test_run"

    resp = app.api.get_agent_params(63)
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"]["name"] == "test_run"


def test_initial_entity(app):
    resp = app.api.set_initial_entity(63, "name", "str", 0)
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"] == "successful"

    resp = app.api.get_initial_entities(63)
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    i = 0
    for x in json["result"]:
        if json["result"][i]["initial_entity_number_cell"] == 0:
            assert json["result"][i]["initial_entity_name"] == "name"
            i += 1

    resp = app.api.get_initial_entity(63, "name")
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"]["initial_entity_name"] == "name"

    resp = app.api.delete_initial_entity(63, "name")
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"] == "successful"


def test_output_entity(app):
    resp = app.api.set_output_entity(63, "name", "str", 0)
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"] == "successful"

    resp = app.api.get_output_entities(63)
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    i = 0
    for x in json["result"]:
        if json["result"][i]["output_entity_number_cell"] == 0:
            assert json["result"][i]["initial_entity_name"] == "name"
            i += 1

    resp = app.api.get_output_entity(63, "name")
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"]["output_entity_name"] == "name"

    resp = app.api.delete_output_entity(63, "name")
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert json["result"] == "successful"


def test_data_and_calls(app):
    resp = app.api.initiate_call(63, "9535750158")
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert type(json["result"]["call_group_id"]) == int

    resp = app.api.initiate_bulk_calls(63, "9535750158")
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert type(json["result"]["bulk_id"]) == int
    assert json["result"]["calls"][0]["status"] == "successful"

    resp = app.api.get_data_by_bulk_id(24, 28)
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert type(json["result"][0]["call_id"]) == str

    resp = app.api.get_data_by_call_group_id(63, 261477)
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert type(json["result"][0]["call_id"]) == str

    resp = app.api.get_data_by_timeslot(63, "02-10", "05-25")
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert type(json["result"][0]["call_id"]) == str

    resp = app.api.get_call_records(63, "2eb32a82-955e-11ea-b957-cb87ec06544a.wav")
    json = app.api.get_json(resp.json())
    assert resp.status_code == 200
    assert type(json["result"]["data"]) == str
