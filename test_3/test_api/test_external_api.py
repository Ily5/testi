import pytest
import allure


@allure.feature('Получение списка всех агентов компании')
def test_get_all_agents(api_v3):
    response = api_v3.request_send(path='/api/v2/ext/company-agents',
                                   params={'company_uuid': '9db4c04b-deca-480f-ad1f-9399a28ecffa'})
    assert type(response.json()[0]) is dict

    # print(response.json(), '\n', response.url)


def test_edit_setting_agent(api_v3):
    response = api_v3.request_send(method='PUT', path='/api/v2/ext/agent-settings/general',
                                   params={'agent_uuid': 'b0186434-7f0a-4778-9a2c-609f84342184'},

                                   data='{\n\"name\": \"API_test_automation\",\n\"recall_count\": \"1\",\n\"flag\": \"apiflag\",\n\"routing_channel_limit\": null,\n\"asr\": \"yandex\",\n\"tts\": \"jane@yandex\"\n}')

    print(response)
