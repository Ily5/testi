import pytest
import allure
import requests
import json


@pytest.mark.parametrize('data', ["потом", "не хочу", "да давайте", "хм"], ids=["not_now", "dont_want", "yes", "other"])
@allure.feature('Проверка работы nlu_api')
@allure.title('nlu_base')
def test_nlu(nlu_api_v3, data):
    request_url = nlu_api_v3.base_url + [x for x in nlu_api_v3.path_end_point if "nlu_engine" in x][0]
    load = {"utterance": data}
    response = requests.request("POST", request_url, data=json.dumps(load), headers=nlu_api_v3.api_headers)
    assert response.status_code == 200
    assert response.headers.get('content-type') == 'application/json; charset=utf-8'
    if "потом" in load.values():
        assert 'false' and "\"wrong_time\": [\"true\"" in response.text
    elif "не хочу" in load.values():
        assert 'false' and "dont_want" in response.text
    elif "да давайте" in load.values():
        assert 'true' in response.text
    else:
        assert response.text == "{}"


@pytest.mark.parametrize('data', ["москва щелковское шоссе 35 подъезд 3 квартира 9",
                                  "нижний новгород улица пушкина дом 2 квартира 5",
                                  "в нижнем живу кароче на пушкина в доме пять в третьей квартире"],
                         ids=["msk_correct", "nn_correct", "nn_incorrect"])
@allure.feature('Проверка работы nlu_api')
@allure.title('ner_address')
def test_ner_address(nlu_api_v3, data):
    request_url = nlu_api_v3.base_url + [x for x in nlu_api_v3.path_end_point if "ner_address" in x][0]
    load = {"address": data}
    response = requests.request("POST", request_url, data=json.dumps(load), headers=nlu_api_v3.api_headers)

    assert response.status_code == 200
    assert response.headers.get('content-type') == 'application/json; charset=utf-8'
    if any("москва" in x for x in load.values()):
        assert 'москва' in response.json()["city"]
        assert 'щелковское' and 'шоссе' in response.json()["street"]
        assert any("35" in x for x in response.json()["building"])
        assert any("9" in x for x in response.json()["appartment"])
    elif any("нижний новгород" in x for x in load.values()):
        assert 'нижний новгород' in response.json()["city"]
        assert 'пушкина' and 'улица' in response.json()["street"]
        assert any("2" in x for x in response.json()["building"])
        assert any("5" in x for x in response.json()["appartment"])
    else:
        assert None in response.json()["city"] and response.json()["building"][0] is None


@pytest.mark.parametrize('data', ["Иванов Иван Иванович"],
                         ids=["Correct"])
@allure.feature('Проверка работы nlu_api')
@allure.title('ner_person')
def test_ner_person(nlu_api_v3, data):
    request_url = nlu_api_v3.base_url + [x for x in nlu_api_v3.path_end_point if "ner_person" in x][0]
    load = {"person": data}
    response = requests.request("POST", request_url, data=json.dumps(load), headers=nlu_api_v3.api_headers)

    assert response.status_code == 200
    assert response.headers.get('content-type') == 'application/json; charset=utf-8'
    assert response.json()["first"] == 'Иван'
    assert response.json()["last"] == 'Иванов'
    assert response.json()["middle"] == 'Иванович'
