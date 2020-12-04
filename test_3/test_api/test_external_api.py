import pytest
import allure
import requests
from random import randint

@pytest.mark.parametrize('login', ['rdevetiarov@neuro.net', 'sddsf@neuro.net'])
@pytest.mark.parametrize('password', [randint(21341231, 312423234234)])
@allure.feature('Получение токена невалидный данные')
def test_get_token_no_valid(api_v3, login, password):
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


@pytest.mark.parametrize('no_valid_token', [str(randint(12123, 45345343543)), 'sdfgagsdfgaa', '   '])
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
    params = {"company_uuid": f"{company_uuid}"}
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

