import pytest
import allure
import requests
from random import randint
import time
import uuid


@pytest.mark.parametrize('login', ['rdevetiarov@neuro.net', 'sddsf@neuro.net'])
@allure.feature('Получение токена невалидный данные')
def test_get_token_no_valid(api_v3, login):
    password = str([randint(21341231, 312423234234)])
    request_url = api_v3.base_url + api_v3.path_end_point['post_auth']
    response = requests.request(method='POST', url=request_url, auth=(login, str(password)))

    assert response.status_code == 401, 'Проверка кода ответа от сервера'


@allure.feature('Обновление токена, валидный')
def test_get_refresh_token(api_v3):
    refresh_token = api_v3.refresh_token
    request_url = api_v3.base_url + api_v3.path_end_point['post_update_token']
    data = {"refresh_token": "%s" % refresh_token}
    response = requests.post(url=request_url, json=data)

    assert response.status_code == 200
    assert 'token' in response.json()
    assert 'refresh_token' in response.json()


@pytest.mark.parametrize('no_valid_token', ['12345354346436', '23fdw234fw34', 'ывфавывапывп', 'sdfgagsdfgaa', '   '])
@allure.feature('Обновление токена, невалидный токен')
def test_get_refresh_token_again(api_v3, no_valid_token):
    request_url = api_v3.base_url + api_v3.path_end_point['post_update_token']
    data = {"refresh_token": "%s" % no_valid_token}
    response = requests.post(url=request_url, json=data)

    assert response.status_code == 401, 'Проверка кода ответа от сервера'


@allure.feature('Получение списка всех агентов организации, валидое company_uuid')
def test_get_all_agents_company_valid(api_v3):
    path = api_v3.path_end_point['get_all_agents_company']
    company_uuid = api_v3.test_data['company_uuid']
    params = {"company_uuid": "{}".format(company_uuid)}
    response = api_v3.request_send(path=path, params=params)

    assert response.status_code == 200
    assert len(response.json()) > 0
    assert 'agent_uuid' in response.json()[0]
    assert 'name' in response.json()[0]

    name_agent_list = []
    for item in response.json():
        name_agent_list.append(item['name'])
    assert api_v3.test_data['agent_name'] in name_agent_list


@allure.feature('Получение настроек проекта, валидноу agent_uuid')
def test_get_agent_settings_valid(api_v3, params_agent_uuid):
    path = api_v3.path_end_point['get_agent_settings']
    response = api_v3.request_send(path=path, params=params_agent_uuid)

    assert response.status_code == 200
    assert response.json()['agent_uuid'] == api_v3.test_data['agent_uuid']

    agent_setting_list = ["agent_uuid", "name", "description", "delay", "recall_count", "trunk_name", "flag",
                          "record_path",
                          "routing_channel_limit", "total_channel_limit", "pool_name", "language", "asr", "tts",
                          "speed", "pitch", "emotion", "record_storage_time", "timezone"]
    for item in response.json():
        assert item in agent_setting_list


@allure.feature('Изменение настроек проекта, валидные данные, agent_uuid')
def test_change_agent_settings_valid(api_v3, params_agent_uuid, default_settings_agent, random_str_generator):
    path = api_v3.path_end_point['put_change_agent_settings']
    data = {"recall_count": 22,
            "flag": random_str_generator,
            "routing_channel_limit": 55,
            "asr": "google",
            "tts": "oksana@yandex",
            "language": "en-US"}
    response = api_v3.request_send(method='PUT', path=path, params=params_agent_uuid, json=data)
    assert response.status_code == 200
    # assert response.json()['name'] == data['name']
    assert response.json()['recall_count'] == data['recall_count']
    assert response.json()['flag'] == data['flag']
    assert response.json()['routing_channel_limit'] == data['routing_channel_limit']
    assert response.json()['asr'] == data['asr']
    assert response.json()['tts'] == data['tts']
    assert response.json()['language'] == data['language']
    # assert response.json()['delay'] == data['delay'] #todo узнать про этот параметр


@allure.feature('Получение всех правил для звонков, валидный agent_uuid')
def test_get_rules_for_agent_valid(api_v3, params_agent_uuid):
    path = api_v3.path_end_point['agent_call_rules']
    response = api_v3.request_send(path=path, params=params_agent_uuid)
    assert response.status_code == 200


@allure.feature('Добавление и удаление правила в проекте , валидные данные')
def test_add_new_rule_in_agent_valid(api_v3, params_agent_uuid):
    path = api_v3.path_end_point['agent_call_rules']
    data = {"day": 1, "not_before": "09:00", "not_after": "10:30"}
    response = api_v3.request_send(method='POST', path=path, json=data, params=params_agent_uuid)
    assert response.status_code == 201
    # удаляем добавленное ранее правило
    resp_del = api_v3.request_send(method='DELETE', path=path,
                                   json={"time_slot_uuid": response.json()['time_slot_uuid']})
    assert resp_del.status_code == 204
    assert "time_slot_uuid" in response.json()
    assert "day" in response.json()
    assert "not_before" in response.json()
    assert "not_after" in response.json()
    assert response.json()['day'] == data['day']
    assert data['not_before'] in response.json()['not_before']
    assert data['not_after'] in response.json()['not_after']


@pytest.mark.parametrize('day', [i for i in range(7)])
@allure.feature('Изменение правила в агенте, валидные данные')
def test_edit_rule_in_agent_valid(api_v3, create_new_rule_agent, day):
    path = api_v3.path_end_point['agent_call_rules']
    data = {"time_slot_uuid": create_new_rule_agent,
            "day": day,
            "not_before": "10:01:01",
            "not_after": "21:59:59"}

    response = api_v3.request_send(method='PUT', path=path, json=data)
    assert response.status_code == 200
    assert "time_slot_uuid" in response.json()
    assert "day" in response.json()
    assert "not_before" in response.json()
    assert "not_after" in response.json()
    assert response.json()['day'] == data['day']
    assert data['not_before'] == response.json()['not_before']
    assert data['not_after'] == response.json()['not_after']


@allure.feature('Получение всех входных сущностей агента, валидный agent_uuid')
def test_get_all_initial_entities_agent_valid(api_v3, params_agent_uuid):
    path = api_v3.path_end_point['agent_initial_entities']
    response = api_v3.request_send(path=path, params=params_agent_uuid)
    assert response.status_code == 200
    assert "data" in response.json()
    assert len(response.json()['data']) > 0
    assert "initial_entity_uuid" in response.json()['data'][0]
    assert "name" in response.json()['data'][0]
    assert "synthesis" in response.json()['data'][0]
    assert "agent_uuid" in response.json()['data'][0]
    assert response.json()['data'][0]['agent_uuid'] == api_v3.test_data['agent_uuid']


@allure.feature('Добавление и удаление входной сущности агента, валидные данные')
def test_add_new_initial_entity_agent_valid(api_v3, params_agent_uuid, random_str_generator):
    path = api_v3.path_end_point['agent_initial_entities']
    data = {"name": random_str_generator,
            "synthesis": True}
    response = api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json=data)
    assert response.status_code == 201
    resp_del = api_v3.request_send(method='DELETE', path=path,
                                   json={'initial_entity_uuid': response.json()['initial_entity_uuid']})
    assert resp_del.status_code == 204
    assert 'initial_entity_uuid' in response.json()
    assert 'name' in response.json()
    assert response.json()['name'] == data['name']


@allure.feature('Изменение валидной сущности агента, валидные данные')
def test_edit_initial_entity_agent_valid(api_v3, create_new_initial_entity_agent, random_str_generator):
    path = api_v3.path_end_point['agent_initial_entities']
    data = {"initial_entity_uuid": create_new_initial_entity_agent,
            "name": random_str_generator,
            "synthesis": False}
    response = api_v3.request_send(method='PUT', path=path, json=data)
    assert response.status_code == 200
    assert 'initial_entity_uuid' in response.json()
    assert 'name' in response.json()
    assert 'synthesis' in response.json()
    assert 'agent_uuid' in response.json()
    assert response.json()['agent_uuid'] == api_v3.test_data['agent_uuid']
    assert response.json()['name'] == data['name']
    assert response.json()['synthesis'] is False


@allure.feature('Получение всех выходных сущностей агента, валидный agent_uuid')
def test_get_all_output_entities_agent_valid(api_v3, params_agent_uuid):
    path = api_v3.path_end_point['agent_output_entities']
    response = api_v3.request_send(path=path, params=params_agent_uuid)
    assert response.status_code == 200
    assert "data" in response.json()
    assert len(response.json()['data']) > 0
    assert "output_entity_uuid" in response.json()['data'][0]
    assert "name" in response.json()['data'][0]
    assert "agent_uuid" in response.json()['data'][0]
    assert response.json()['data'][0]['agent_uuid'] == api_v3.test_data['agent_uuid']


@pytest.mark.parametrize('entity_type', ['string', 'number', 'datetime'])
@allure.feature('Добавление и удаление выходной сущности агента, валидные данные')
def test_add_delete_new_initial_entity_agent_valid(api_v3, params_agent_uuid, random_str_generator, entity_type):
    path = api_v3.path_end_point['agent_output_entities']
    data = {"name": random_str_generator, "number_cell": randint(2, 9), "entity_type": entity_type}
    response = api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json=data)
    assert response.status_code == 201
    resp_del = api_v3.request_send(method='DELETE', path=path,
                                   json={'output_entity_uuid': response.json()['output_entity_uuid']})
    assert resp_del.status_code == 204
    assert 'output_entity_uuid' in response.json()
    assert 'name' in response.json()
    assert response.json()['name'] == data['name']


@pytest.mark.parametrize('entity_type', ['string', 'number', 'datetime'])
@allure.feature('Изменение выходной сущности агента, валидные данные')
def test_edit_output_entity_agent_valid(api_v3, random_str_generator, create_new_output_entity_agent, entity_type):
    path = api_v3.path_end_point['agent_output_entities']
    data = {"name": random_str_generator, "entity_type": entity_type,
            "output_entity_uuid": create_new_output_entity_agent}
    response = api_v3.request_send(method='PUT', path=path, json=data)
    assert response.status_code == 200
    assert "output_entity_uuid" in response.json()
    assert "name" in response.json()
    assert "entity_type" in response.json()
    assert "agent_uuid" in response.json()
    assert response.json()['agent_uuid'] == api_v3.test_data['agent_uuid']
    assert response.json()['name'] == data['name']
    assert response.json()['entity_type'] == data['entity_type']


@allure.feature('Загрузка диалога, валидные данные')
def test_upload_dialog(api_v3, params_agent_uuid, remove_queue_dialogs_and_calls):
    path = api_v3.path_end_point['upload_dialog']
    data = {'msisdn': str(randint(00000000000, 99999999999))}
    response = api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json=data)
    assert response.status_code == 200
    assert 'dialog_uuid' in response.json()


@allure.feature('Множественная загрузка диалога, получение статуса, валидные данные')
def test_upload_group_dialogs(api_v3, params_agent_uuid, remove_queue_dialogs_and_calls):
    path = api_v3.path_end_point['upload_group_dialogs']
    data = [{'msisdn': str(randint(00000000000, 99999999999)), "script_entry_point": "main"}]
    iterations = randint(1, 10)
    for i in range(iterations):
        data.append(data[0])
    response = api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json=data)
    assert response.status_code == 202
    assert 'bulk_uuid' in response.json()
    assert 'task_uuid' in response.json()


@allure.feature('Получение статуса множественной загрузки параметров диалога, валидные данные')
def test_get_status_upload_group_dialogs_valid(api_v3, upload_group_dialogs):
    params = {'task_uuid': upload_group_dialogs['task_uuid']}
    path = api_v3.path_end_point['get_dialogs_group_upload_status']
    response = api_v3.request_send(path=path, params=params)
    assert response.status_code == 200
    assert 'state' in response.json()
    assert 'info' in response.json()
    assert response.json()['state'] in ['SUCCESS', 'PENDING']


@allure.feature('Получение результата множественной загрузки параметров диалога, валидные данные')
def test_get_result_upload_group_dialogs_valid(api_v3, upload_group_dialogs):
    # todo тест переодически падает, т.к. диалог не успевает создаться, как решить без паузы?
    time.sleep(2)
    params = {'task_uuid': upload_group_dialogs['task_uuid']}
    path = api_v3.path_end_point['get_dialogs_group_upload_result']
    response = api_v3.request_send(path=path, params=params)
    result = response.json()
    assert response.status_code == 200
    assert 'status' in result[0]
    assert 'msisdn' in result[0]
    assert 'message' in result[0]
    assert 'dialog_uuid' in result[0]


@allure.feature('Получение статистики по одному диалогу, валидный dialog_uuid')
def test_get_dialog_statistic(api_v3, upload_dialog):
    path = api_v3.path_end_point['get_dialog_statistic']
    params = {"dialog_uuid": upload_dialog['dialog_uuid']}
    response = api_v3.request_send(path=path, params=params)
    assert response.status_code in [200, 404]
    # todo как можно дожидаться окончания звонка?


@allure.feature('Получение статистики по группе диалогов, валидные bulk_uuid')
def test_get_group_dialogs_statistic(api_v3, upload_group_dialogs):
    path = api_v3.path_end_point['get_group_dialogs_statistic']
    bulk_uuid = upload_group_dialogs['bulk_uuid']
    params = {'bulk_uuid': bulk_uuid}
    response = api_v3.request_send(path=path, params=params)
    assert response.status_code in [200, 404]


@allure.feature('Получение output entities статистики по заданомму временному интервалу, валидные данные')
def test_get_output_entities_time_slot_valid(api_v3):
    path = api_v3.path_end_point['get_statistic_output_entities']
    agent_uuid = api_v3.test_data['agent_uuid']
    data = {'agent_uuid': agent_uuid, 'start': "2020-11-26 10:08:05.0", 'end': "2020-12-10 12:08:05.0"}
    response = api_v3.request_send(method='POST', path=path, json=data)
    assert response.status_code == 200
    assert 'result' in response.json()


@allure.feature('Получение записи звнока, несуществующий uuid')
def test_get_call_record_does_not_exist_uuid(api_v3):
    path = api_v3.path_end_point['get_download_call_record']
    params = {'call_uuid': uuid.uuid4()}
    response = api_v3.request_send(path=path, params=params)
    assert response.status_code == 404


@allure.feature('Получение списка диалогов агента, валидные данные')
def test_get_agent_dialogs_valid(api_v3, params_agent_uuid):
    path = api_v3.path_end_point['get_dialogs_agent']
    response = api_v3.request_send(path=path, params=params_agent_uuid)
    assert response.status_code == 200
    assert 'msisdn' in response.json()
    assert 'dialog_uuid' in response.json()
    assert 'result' in response.json()
    assert 'date_added' in response.json()


@allure.feature('Получение списка звонков агента, валидные данные')
def test_get_agent_dialogs_valid(api_v3, params_agent_uuid):
    path = api_v3.path_end_point['get_calls_agent']
    response = api_v3.request_send(path=path, params=params_agent_uuid)
    assert response.status_code == 200
    assert 'msisdn' in response.json()
    assert 'call_uuid' in response.json()
    assert 'result' in response.json()
    assert 'date_added' in response.json()
    assert 'date_processed' in response.json()


@allure.feature('Остановка диалогов в очереди, валидный agent_uuid')
def test_stop_queue_dialogs_valid(api_v3, params_agent_uuid):
    path = api_v3.path_end_point['stop_queue_dialogs']
    response = api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json={}, status_code=409)
    assert response.status_code == 200


@allure.feature('Возвращение диалогов в очередь, валидный agent_uuid')
def test_return_queue_dialogs_valid(api_v3, params_agent_uuid):
    path = api_v3.path_end_point['return_queue_dialogs']
    response = api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json={})
    assert response.status_code == 200


@allure.feature('Удаление диалогов из очереди, валидный agent_uuid')
def test_return_queue_dialogs_valid(api_v3, params_agent_uuid):
    path = api_v3.path_end_point['remove_queue_dialogs']
    response = api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json={}, status_code=409)
    assert response.status_code == 200
