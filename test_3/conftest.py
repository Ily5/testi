import pytest
import requests
import string
import random
import json
from test_3.fixture.api import APIClientV3
from random import randint


@pytest.fixture(scope='session')
def api_v3(request):
    fixture = None
    if fixture is None:
        with open(request.config.getoption("--config")) as cfg:
            config = json.load(cfg)
            fixture = APIClientV3(base_url=config['v3']['api']['api_base_url'],
                                  test_data=config['v3']['test_data'],
                                  path_end_point=config['v3']['api']['methods_end_point'])
            token, refresh_token = fixture.get_api_token(password=config['v3']['auth']['pass'],
                                                         login=config['v3']['auth']['login'])
        fixture.token, fixture.refresh_token = token, refresh_token

    return fixture


@pytest.fixture(scope='session')
def pool_api_v3(request):
    fixture = None
    if fixture is None:
        with open(request.config.getoption("--config")) as cfg:
            config = json.load(cfg)
            fixture = APIClientV3(base_url=config['v3']['api']['poll_api_v3_url'],
                                  test_data=config['v3']['test_data'],
                                  path_end_point=config['v3']['api']['methods_end_point']["poll_api"])
    return fixture


@pytest.fixture
def params_agent_uuid(api_v3):
    agent_uuid = api_v3.test_data['agent_uuid']
    params = {"agent_uuid": "{}".format(agent_uuid)}
    return params


@pytest.fixture
def params_agent_id(pool_api_v3):
    agent_id = pool_api_v3.test_data['agent_id']
    params = {"agent_id": "{}".format(agent_id)}
    return params


@pytest.fixture
def default_settings_agent(api_v3, params_agent_uuid):
    yield
    test_data = api_v3.test_data
    data = {"flag": "{}".format(test_data['agent_flag']),
            "name": "{}".format(test_data['agent_name']),
            "recall_count": "{}".format(test_data['recall_count']),
            "routing_channel_limit": None,
            "asr": "{}".format(test_data['asr']),
            "tts": "{}".format(test_data['tts']),
            "language": "{}".format(test_data['language'])}

    path = api_v3.path_end_point['put_change_agent_settings']
    api_v3.request_send(method="PUT", path=path, json=data, params=params_agent_uuid)


@pytest.fixture()
def create_new_rule_agent(request, api_v3, params_agent_uuid):
    path = api_v3.path_end_point['agent_call_rules']
    data = {"day": 1, "not_before": "09:00", "not_after": "10:30"}
    response = api_v3.request_send(method='POST', path=path, json=data, params=params_agent_uuid)
    time_slot_uuid = response.json()['time_slot_uuid']

    def fin():
        api_v3.request_send(method='DELETE', path=path, json={"time_slot_uuid": response.json()['time_slot_uuid']})

    request.addfinalizer(fin)
    return time_slot_uuid


@pytest.fixture()
def create_new_initial_entity_agent(request, api_v3, random_str_generator, params_agent_uuid):
    path = api_v3.path_end_point['agent_initial_entities']
    data = {"name": random_str_generator,
            "synthesis": True}
    response = api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json=data)
    initial_entity_uuid = response.json()['initial_entity_uuid']

    def fin():
        api_v3.request_send(method='DELETE', path=path,
                            json={'initial_entity_uuid': response.json()['initial_entity_uuid']})

    request.addfinalizer(fin)
    return initial_entity_uuid


@pytest.fixture()
def create_new_output_entity_agent(request, api_v3, random_str_generator, params_agent_uuid):
    path = api_v3.path_end_point['agent_output_entities']
    data = {"name": random_str_generator, "number_cell": randint(2, 9), "entity_type": 'string'}
    response = api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json=data)
    output_entity_uuid = response.json()['output_entity_uuid']

    def fin():
        api_v3.request_send(method='DELETE', path=path,
                            json={'output_entity_uuid': output_entity_uuid})

    request.addfinalizer(fin)
    return output_entity_uuid


@pytest.fixture()
def remove_queue_dialogs(request, api_v3, params_agent_uuid):
    def fin():
        path = api_v3.path_end_point['remove_queue_dialogs']
        api_v3.request_send(method='POST', path=path, params=params_agent_uuid)

    request.addfinalizer(fin)
    # todo интегрироваться с базой cms, удалять диалоги от туда


@pytest.fixture()
def upload_group_dialogs(api_v3, params_agent_uuid, remove_queue_dialogs):
    path = api_v3.path_end_point['upload_group_dialogs']
    data = [{'msisdn': str(randint(00000000000, 99999999999)), "script_entry_point": "main"},
            {'msisdn': str(randint(00000000000, 99999999999)), "script_entry_point": "main"}]
    return (api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json=data)).json()


@pytest.fixture
def upload_dialog(api_v3, params_agent_uuid, remove_queue_dialogs):
    path = api_v3.path_end_point['upload_dialog']
    data = {'msisdn': str(randint(00000000000, 99999999999))}
    return (api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json=data)).json()


@pytest.fixture
def random_str_generator(size=random.randint(3, 129),
                         chars=string.ascii_uppercase + string.digits + string.ascii_lowercase + '\t'):
    return ''.join(random.choice(chars) for _ in range(size))
