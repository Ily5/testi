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
    path = pool_api_v3.path_end_point['defer_calls']
    response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_id, json={})
    assert response.status_code == 200


@allure.feature('Вернуить все звонки из отложенных')
def test_return_all_calls(pool_api_v3, params_agent_id):
    path = pool_api_v3.path_end_point['return_calls']
    response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_id, json={})
    assert response.status_code == 200


@allure.feature('Отменить все звонки в очереди')
def test_cancel_all_calls(pool_api_v3, params_agent_id):
    path = pool_api_v3.path_end_point['get_list_queue_calls']
    response = pool_api_v3.request_send(method='DELETE', path=path, params=params_agent_id, json={})
    assert response.status_code == 200


@allure.feature('Сбросить очередь')
def test_drop_queue_calls(pool_api_v3, params_agent_id):
    path = pool_api_v3.path_end_point['drop_queue_calls']
    response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_id, json={})
    assert response.status_code == 200


@allure.feature('Получить объект очереди звонков')
def test_get_full_queue_calls(pool_api_v3, params_agent_id):
    path = pool_api_v3.path_end_point['get_full_queue']
    response = pool_api_v3.request_send(path=path, params=params_agent_id)
    assert response.status_code == 200


@allure.feature('Получить все валидные звонки')
def test_get_all_valid_calls(pool_api_v3, params_agent_id):
    path = pool_api_v3.path_end_point['get_all_valid_calls']
    params = {**{"page": "1",
                 "by_count": "3"}, **params_agent_id}
    response = pool_api_v3.request_send(path=path, params=params)
    assert response.status_code == 200


@allure.feature('Получение объекта очереди диалогов агента, валидный agent_id')
def test_all_dialog_queue_valid(pool_api_v3, params_agent_id):
    params_agent_id = {'agent_id': '97'}
    params = {**{"page": "1",
                 "by_count": "3"}, **params_agent_id}
    path = pool_api_v3.path_end_point['get_all_dialog_queue']
    response = pool_api_v3.request_send(path=path, params=params)
    assert response.status_code == 200


@allure.feature('Получение размера очереди диалогов агента, валидный agent_id')
def test_get_dialog_queue_size_valid(pool_api_v3, params_agent_id):
    params_agent_id = {'agent_id': '97'}
    path = pool_api_v3.path_end_point['get_dialog_queue_size']
    response = pool_api_v3.request_send(path=path, params=params_agent_id)
    assert response.status_code == 200


@allure.feature('Отложить все диалоги для проекта')
def test_defer_all_dialogs(pool_api_v3, params_agent_id):
    path = pool_api_v3.path_end_point['defer_dialog']
    response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_id)
    assert response.status_code == 200


@allure.feature('Вернуть все диалоги из отложенных, валидный agent_id')
def test_return_all_dialog_valid(pool_api_v3, params_agent_id):
    path = pool_api_v3.path_end_point['return_dialog']
    response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_id)
    assert response.status_code == 200


@allure.feature('Отменить все далоги для проекта, валидный agent_id')
def test_cancel_all_dialog_valid(pool_api_v3, params_agent_id):
    path = pool_api_v3.path_end_point['cancel_all_dialogs']
    response = pool_api_v3.request_send(method='DELETE', path=path, params=params_agent_id)
    assert response.status_code == 200


@allure.feature('Получить диалоги')
def test_get_dialogs(pool_api_v3):
    path = pool_api_v3.path_end_point['get_dialogs']
    response = pool_api_v3.request_send(path=path)
    assert response.status_code == 200
