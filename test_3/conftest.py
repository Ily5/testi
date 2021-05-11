import time
from random import randint
import pytest


@pytest.fixture(scope="session")
def params_agent_uuid(api_v3):
    agent_uuid = api_v3.test_data["agent_uuid"]
    params = {"agent_uuid": "{}".format(agent_uuid)}
    return params


@pytest.fixture
def default_settings_agent(api_v3, params_agent_uuid):
    yield
    set_default_settings_agent(api_v3, params_agent_uuid)


@pytest.fixture()
def create_new_rule_agent(request, api_v3, params_agent_uuid):
    path = api_v3.path_end_point["agent_call_rules"]
    data = {"day": 1, "not_before": "09:00", "not_after": "10:30"}
    response = api_v3.request_send(
        method="POST", path=path, json=data, params=params_agent_uuid
    )
    time_slot_uuid = response.json()["time_slot_uuid"]

    def fin():
        api_v3.request_send(
            method="DELETE",
            path=path,
            json={"time_slot_uuid": response.json()["time_slot_uuid"]},
        )

    request.addfinalizer(fin)
    return time_slot_uuid


@pytest.fixture()
def create_new_initial_entity_agent(
        request, api_v3, random_str_generator, params_agent_uuid
):
    path = api_v3.path_end_point["agent_initial_entities"]
    data = {"name": random_str_generator, "synthesis": True}
    response = api_v3.request_send(
        method="POST", path=path, params=params_agent_uuid, json=data
    )
    initial_entity_uuid = response.json()["initial_entity_uuid"]

    def fin():
        api_v3.request_send(
            method="DELETE",
            path=path,
            json={"initial_entity_uuid": response.json()["initial_entity_uuid"]},
        )

    request.addfinalizer(fin)
    return initial_entity_uuid


@pytest.fixture()
def create_new_output_entity_agent(
        request, api_v3, random_str_generator, params_agent_uuid
):
    path = api_v3.path_end_point["agent_output_entities"]
    data = {
        "name": random_str_generator,
        "number_cell": randint(2, 9),
        "entity_type": "string",
    }
    response = api_v3.request_send(
        method="POST", path=path, params=params_agent_uuid, json=data
    )
    output_entity_uuid = response.json()["output_entity_uuid"]

    def fin():
        api_v3.request_send(
            method="DELETE", path=path, json={"output_entity_uuid": output_entity_uuid}
        )

    request.addfinalizer(fin)
    return output_entity_uuid


@pytest.fixture(scope="class")
def remove_queue_dialogs_and_calls(request, api_v3, pool_api_v3, params_agent_uuid):
    def fin():
        clear_queue(api_v3, params_agent_uuid, pool_api_v3)

    try:
        pass
    except:
        pass
    finally:
        request.addfinalizer(fin)


@pytest.fixture(scope="class")
def upload_group_dialogs(api_v3, params_agent_uuid, remove_queue_dialogs_and_calls):
    path = api_v3.path_end_point["upload_group_dialogs"]
    data = [
        {
            "msisdn": str(randint(00000000000, 99999999999)),
            "script_entry_point": "main",
            "script_name": "test_api",
        },
        {
            "msisdn": str(randint(00000000000, 99999999999)),
            "script_entry_point": "main",
            "script_name": "test_api",
        },
    ]
    res = api_v3.request_send(
        method="POST", path=path, params=params_agent_uuid, json=data
    )
    if res.status_code not in [200, 201, 202]:
        print(res.status_code)
        print(res.text)
        raise Exception("Uploading group dialog error")
    return res.json()


@pytest.fixture(scope="class")
def upload_dialog(api_v3, params_agent_uuid, remove_queue_dialogs_and_calls):
    path = api_v3.path_end_point["upload_dialog"]
    data = {"msisdn": str(randint(00000000000, 99999999999))}
    return (
            api_v3.request_send(
                method="POST",
                path=path,
                params=params_agent_uuid,
                json=data
            ).json())


@ pytest.fixture(scope="class")
def creation_queue_dialog(
        request,
        pool_api_v3,
        api_v3,
        params_agent_uuid,
        remove_queue_dialogs_and_calls,
        count_dialogs=15,
):
    clear_queue(api_v3, params_agent_uuid, pool_api_v3)

    change_total_channel_limit(api_v3, 0, params_agent_uuid)

    path = api_v3.path_end_point["upload_group_dialogs"]
    data = [
        {
            "msisdn": str(randint(00000000000, 99999999999)),
            "script_entry_point": "main",
            "script_name": "test_api",
        }
    ]
    response = api_v3.request_send(
        method="POST", path=path, params=params_agent_uuid, json=data
    )
    for i in range(count_dialogs):
        data.append(
            {
                "msisdn": str(randint(00000000000, 99999999999)),
                "script_entry_point": "main",
                "script_name": "test_api",
            }
        )
    res = api_v3.request_send(
        method="POST", path=path, params=params_agent_uuid, json=data)
    if res.status_code not in [200, 201, 202]:
        print(res.status_code)
        print(res.text)
        raise Exception("Uploading group dialog error")

    print("\n", "LEN data - ", len(data))

    check_queue(
        params_agent_uuid,
        pool_api_v3,
        path_name="get_all_dialog_queue",
        queue_name="dialogs",
        queue_len=(len(data) + 1),
    )

    def default_setting():
        set_default_settings_agent(api_v3, params_agent_uuid)

    request.addfinalizer(default_setting)
    return response.json(), data


@pytest.fixture(scope="class")
def creation_queue_calls(
        request, api_v3, pool_api_v3, params_agent_uuid, remove_queue_dialogs_and_calls
):
    clear_queue(api_v3, params_agent_uuid, pool_api_v3)
    change_total_channel_limit(api_v3, 2, params_agent_uuid)

    path = api_v3.path_end_point["upload_group_dialogs"]
    data = []
    for i in range(randint(12, 15)):
        data.append(
            {
                "msisdn": str(randint(00000000000, 99999999999)),
                "script_entry_point": "main",
                "script_name": "test_api",
            }
        )
    res = api_v3.request_send(
        method="POST", path=path, params=params_agent_uuid, json=data
    )
    if res.status_code not in [200, 201, 202]:
        print(res.status_code)
        print(res.text)
        raise Exception("Uploading group dialog error")

    check_queue(
        params_agent_uuid,
        pool_api_v3,
        path_name="get_list_queue_calls",
        queue_name="calls",
        queue_len=len(data),
    )
    change_total_channel_limit(api_v3, 0, params_agent_uuid)

    def default_setting():
        set_default_settings_agent(api_v3, params_agent_uuid)

    request.addfinalizer(default_setting)
    return data


@pytest.fixture(scope="module", autouse=True)
def default_settings(api_v3, params_agent_uuid):
    set_default_settings_agent(api_v3, params_agent_uuid)


def clear_queue(api_v3, params_agent_uuid, pool_api_v3):
    api_v3.request_send(
        method="POST",
        path=api_v3.path_end_point["return_queue_dialogs"],
        params=params_agent_uuid,
        json={}
    )
    api_v3.request_send(
        method="POST",
        path=api_v3.path_end_point["remove_queue_dialogs"],
        params=params_agent_uuid
    )

    pool_api_v3.request_send(
        method="POST",
        path=pool_api_v3.path_end_point["return_calls"],
        params=params_agent_uuid,
        json={},
    )
    pool_api_v3.request_send(
        method="DELETE",
        path=pool_api_v3.path_end_point["get_list_queue_calls"],
        params=params_agent_uuid,
        json={},
    )


def set_default_settings_agent(api_v3, params_agent_uuid):
    test_data = api_v3.test_data
    data = {
        "flag": "{}".format(test_data["agent_flag"]),
        "name": "{}".format(test_data["agent_name"]),
        "recall_count": "{}".format(test_data["recall_count"]),
        "routing_channel_limit": None,
        "asr": "{}".format(test_data["asr"]),
        "tts": "{}".format(test_data["tts"]),
        "language": "{}".format(test_data["language"]),
        "total_channel_limit": "{}".format(test_data["total_channel_limit"]),
    }

    path = api_v3.path_end_point["put_change_agent_settings"]
    api_v3.request_send(method="PUT", path=path, json=data, params=params_agent_uuid)

    data = {
        "name": f"{test_data['agent_name']}",
        "default_priority": 3,
        "pool_uuid": f"{test_data['pool_uuid']}",
        "trunk_uuid": f"{test_data['trunk_uuid']}",
    }
    api_v3.request_send(
        method="PUT", path=f"/api/v2/rbac/agent/{test_data['agent_uuid']}", json=data
    )
    api_v3.request_send(
        method="POST",
        path="/api/v2/logic/logic_unit/default",
        params=params_agent_uuid,
        json={**{"uuid": test_data["logic_uuid"]}, **params_agent_uuid},
    )


def check_queue(params_agent_uuid, pool_api_v3, path_name, queue_name, queue_len=0):
    time_out = time.time() + 240
    params = {**{"page": "1", "by_count": "100000"}, **params_agent_uuid}
    path = pool_api_v3.path_end_point[path_name]
    # TODO переделать проверку очереди через методы ext api

    while True:
        if time.time() > time_out:
            raise TimeoutError

        if queue_name == "calls":
            queue_name_2 = "dialogs"
            path_2 = pool_api_v3.path_end_point["get_all_dialog_queue"]
            response_1 = pool_api_v3.request_send(path=path, params=params)
            response_2 = pool_api_v3.request_send(path=path_2, params=params)

            # print('\n', time.time(), ' len calls = ', len(response_1.json()['calls']))
            # print('\n', time.time(), 'len dialogs = ', len(response_2.json()['dialogs']))

            if (
                    len(response_1.json()[queue_name]) == queue_len
                    and len(response_2.json()[queue_name_2]) == 0
            ):
                print("Вышли из цикла")
                # print('\n', time.time(), 'Выход из цикла. len calls = ', len(response_1.json()['calls']))
                break
        else:
            response = pool_api_v3.request_send(path=path, params=params)
            # print('\n', time.time(), 'len DIALOGS = ', len(response.json()[queue_name]))
            if response.json()["total"] >= queue_len:
                print("Вышли из цикла")
                break


def change_total_channel_limit(api_v3, limit, params_agent_uuid):
    path_agent_setting = api_v3.path_end_point["put_change_agent_settings"]
    api_v3.request_send(
        method="PUT",
        path=path_agent_setting,
        json={"total_channel_limit": limit},
        params=params_agent_uuid,
    )
