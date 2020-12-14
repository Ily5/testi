import pytest
import allure
from random import randint


@allure.feature('Получение звонка из очереди')
def test_get_calls_queue(pool_api_v3):
    path = pool_api_v3.path_end_point['get_calls']
    response = pool_api_v3.request_send(path=path)
    assert response.status_code == 200


@allure.feature('Получение звонка из очереди с лимитом')
def test_get_calls_queue(pool_api_v3):
    path = pool_api_v3.path_end_point['get_calls']
    params = {'limit': str(randint(2, 10))}
    response = pool_api_v3.request_send(path=path, params=params)
    assert response.status_code == 200


@allure.feature('Получение списка выполняющихся звонков')
def test_get_progress_calls(pool_api_v3, params_agent_id):
    path = pool_api_v3.path_end_point['get_progress_calls']
    response = pool_api_v3.request_send(path=path, params=params_agent_id)
    assert response.status_code in [200, 400]


@allure.feature('Получение списков звонков в очереди')
def test_get_list_queue_calls(pool_api_v3, params_agent_id):
    path = pool_api_v3.path_end_point['get_list_queue_calls']
    params = {**{"page": "1",
                 "by_count": "3"}, **params_agent_id}
    response = pool_api_v3.request_send(path=path, params=params)
    assert response.status_code == 200
    assert 'calls' in response.json()
    assert 'total' in response.json()


@allure.feature('Отложить все звонки в очереди')
def test_defer_all_calls(pool_api_v3, params_agent_id):
    path = pool_api_v3.path_end_point['defer_all_calls']
    response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_id, json={})
    assert response.status_code == 200


@allure.feature('Отложить один звонок, валидный call_id')
def test_defer_call(pool_api_v3, params_agent_id):
    pass
