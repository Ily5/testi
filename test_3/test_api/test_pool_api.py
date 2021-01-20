import pytest
import allure
from random import randint


class TestPoolApiCalls:

    @allure.feature('Получение списков звонков в очереди')
    def test_get_list_queue_calls(self, pool_api_v3, params_agent_uuid, creation_queue_calls):
        path = pool_api_v3.path_end_point['get_list_queue_calls']
        params = {**{"page": "1",
                     "by_count": "50"}, **params_agent_uuid}
        response = pool_api_v3.request_send(path=path, params=params)

        assert response.status_code == 200
        assert 'calls' in response.json()
        assert 'total' in response.json()
        assert 'id' in response.json()['calls'][0]
        assert 'msisdn' in response.json()['calls'][0]
        assert 'date_added' in response.json()['calls'][0]
        assert 'trunk_id' in response.json()['calls'][0]
        assert 'uuid' in response.json()['calls'][0]
        assert response.json()['total'] > 0
        assert response.json()['total'] >= len(response.json()['calls'])

    @allure.feature('Получение звонка из очереди')
    def test_get_calls_queue(self, pool_api_v3, creation_queue_calls):
        path = pool_api_v3.path_end_point['get_calls']
        response = pool_api_v3.request_send(path=path)
        assert response.status_code == 200

    @allure.feature('Получение звонка из очереди с лимитом')
    def test_get_calls_queue(self, pool_api_v3, creation_queue_calls):
        path = pool_api_v3.path_end_point['get_calls']
        params = {'limit': str(randint(2, 10))}
        response = pool_api_v3.request_send(path=path, params=params)
        assert response.status_code == 200

    @allure.feature('Получение списка выполняющихся звонков')
    def test_get_progress_calls(self, pool_api_v3, params_agent_uuid, creation_queue_calls):
        path = pool_api_v3.path_end_point['get_progress_calls']
        response = pool_api_v3.request_send(path=path, params=params_agent_uuid)
        assert response.status_code in [200, 400]

    @allure.feature('Вернуть один звонок из отложенных')
    def test_return_one_call_valid(self, pool_api_v3, params_agent_uuid, creation_queue_calls):
        with allure.step('Получаем список звонков в очереди'):
            response_list_queue_calls = pool_api_v3.request_send(
                path=pool_api_v3.path_end_point['get_list_queue_calls'],
                params={**{"page": "1",
                           "by_count": "50"}, **params_agent_uuid})
            call_id = response_list_queue_calls.json()['calls'][0]['id']
            call_msisdn = response_list_queue_calls.json()['calls'][0]['msisdn']

        with allure.step('Ставим один звонок на паузу'):
            path = pool_api_v3.path_end_point['defer_calls']
            params = {**{'call_id': str(call_id)}, **params_agent_uuid}
            pool_api_v3.request_send(method='POST', path=path, params=params, json={})

        with allure.step('Возвращяем звонок обратно, провряем статус код'):
            path = pool_api_v3.path_end_point['return_calls']
            params = {**{'call_id': str(call_id)}, **params_agent_uuid}
            response = pool_api_v3.request_send(method='POST', path=path, params=params, json={})
            assert response.status_code == 200

        with allure.step('Получаем список звонков в очереди, поверяем, что отложенный звонок есть в списке'):
            response_list_queue_calls = pool_api_v3.request_send(
                path=pool_api_v3.path_end_point['get_list_queue_calls'],
                params={**{"page": "1",
                           "by_count": "50"}, **params_agent_uuid})
            list_active_call_id = [call['msisdn'] for call in response_list_queue_calls.json()['calls']]
            assert call_msisdn in list_active_call_id

    @allure.feature('Сбросить очередь звонков')
    def test_drop_queue_calls(self, pool_api_v3, params_agent_uuid, creation_queue_calls):
        path = pool_api_v3.path_end_point['drop_queue_calls']
        response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json={})
        assert response.status_code == 200

    @allure.feature('Получить объект очереди звонков')
    def test_get_full_queue_calls(self, pool_api_v3, params_agent_uuid, creation_queue_calls):
        path = pool_api_v3.path_end_point['get_full_queue']
        response = pool_api_v3.request_send(path=path, params=params_agent_uuid)
        assert response.status_code == 200

    @allure.feature('Получить все валидные звонки')
    def test_get_all_valid_calls(self, pool_api_v3, params_agent_uuid, creation_queue_calls):
        path = pool_api_v3.path_end_point['get_all_valid_calls']
        params = {**{"page": "1",
                     "by_count": "50"}, **params_agent_uuid}
        response = pool_api_v3.request_send(path=path, params=params)
        assert response.status_code == 200

    @allure.feature('Отложить все звонки в очереди')
    def test_defer_all_calls(self, pool_api_v3, params_agent_uuid, creation_queue_calls):
        with allure.step('Ставим все звонки на паузу'):
            path = pool_api_v3.path_end_point['defer_calls']
            response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json={})
            assert response.status_code == 200

        with allure.step('Получаем список звонков в очереди, проверяем, что он пуст'):
            response_list_queue_calls = pool_api_v3.request_send(
                path=pool_api_v3.path_end_point['get_list_queue_calls'],
                params={**{"page": "1",
                           "by_count": "50"}, **params_agent_uuid})
            assert len(response_list_queue_calls.json()['calls']) == 0
            assert response_list_queue_calls.json()['total'] == 0

    @allure.feature('Вернуть все звонки из отложенных, валидный')
    def test_return_all_calls_valid(self, pool_api_v3, params_agent_uuid, creation_queue_calls):
        with allure.step('Ставим все звонки на паузу'):
            pool_api_v3.request_send(method='POST', path=pool_api_v3.path_end_point['defer_calls'],
                                     params=params_agent_uuid, json={})

        with allure.step('Возвращаем все звонки из отложенных'):
            path = pool_api_v3.path_end_point['return_calls']
            response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json={})
            assert response.status_code == 200

        with allure.step('Получаем список звонков в очереди, проверям, что не пустой'):
            response_list_queue_calls = pool_api_v3.request_send(
                path=pool_api_v3.path_end_point['get_list_queue_calls'],
                params={**{"page": "1",
                           "by_count": "50"}, **params_agent_uuid})
            assert len(response_list_queue_calls.json()['calls']) > 0
            assert response_list_queue_calls.json()['total'] > 0

    @allure.feature('Отложить один звонок в очереди, валидный')
    def test_defer_one_call_valid(self, pool_api_v3, params_agent_uuid, creation_queue_calls):
        with allure.step('Получаем список звонков в очереи'):
            response_list_queue_calls = pool_api_v3.request_send(
                path=pool_api_v3.path_end_point['get_list_queue_calls'],
                params={**{"page": "1",
                           "by_count": "50"}, **params_agent_uuid})
            call_id = response_list_queue_calls.json()['calls'][0]['id']

        with allure.step('Ставим один звонок на паузу'):
            path = pool_api_v3.path_end_point['defer_calls']
            params = {**{'call_id': str(call_id)}, **params_agent_uuid}
            response = pool_api_v3.request_send(method='POST', path=path, params=params, json={})
            assert response.status_code == 200

        with allure.step('Получаем список звонков, поверяем, что отложеного звонка там нет, возвращяем его в очередь'):
            response_list_queue_calls = pool_api_v3.request_send(
                path=pool_api_v3.path_end_point['get_list_queue_calls'],
                params={**{"page": "1",
                           "by_count": "50"}, **params_agent_uuid})
            list_active_call_id = [call['id'] for call in response_list_queue_calls.json()['calls']]
            path = pool_api_v3.path_end_point['return_calls']
            pool_api_v3.request_send(method='POST', path=path, params=params_agent_uuid, json={})
            assert call_id not in list_active_call_id

    @allure.feature('Отменить один звонок в очереди')
    def test_cancel_one_call_valid(self, pool_api_v3, params_agent_uuid, creation_queue_calls):
        with allure.step('Получаем список звонков в очереди'):
            response_list_queue_calls = pool_api_v3.request_send(
                path=pool_api_v3.path_end_point['get_list_queue_calls'],
                params={**{"page": "1",
                           "by_count": "50"}, **params_agent_uuid})
            call_id = response_list_queue_calls.json()['calls'][0]['id']
        with allure.step('Отменяем один звонок'):
            path = pool_api_v3.path_end_point['get_list_queue_calls']
            params = {**{'call_id': str(call_id)}, **params_agent_uuid}
            response = pool_api_v3.request_send(method='DELETE', path=path, params=params, json={})
            assert response.status_code == 200

        with allure.step('Получаем список звонков в очереди, проверяем, что отмененного нет в списке'):
            response_list_queue_calls = pool_api_v3.request_send(
                path=pool_api_v3.path_end_point['get_list_queue_calls'],
                params={**{"page": "1",
                           "by_count": "50"}, **params_agent_uuid})
            list_call_id = [call['id'] for call in response_list_queue_calls.json()['calls']]
            assert call_id not in list_call_id

    @allure.feature('Отменить все звонки в очереди, валидный')
    def test_cancel_all_calls_valid(self, pool_api_v3, params_agent_uuid, creation_queue_calls):
        path = pool_api_v3.path_end_point['get_list_queue_calls']
        response = pool_api_v3.request_send(method='DELETE', path=path, params=params_agent_uuid, json={})

        assert response.status_code == 200
        response = pool_api_v3.request_send(path=pool_api_v3.path_end_point['get_list_queue_calls'],
                                            params={**{"page": "1",
                                                       "by_count": "50"}, **params_agent_uuid})
        assert len(response.json()['calls']) == 0
        assert response.json()['total'] == 0


class TestPoolApiDialog:

    @allure.feature('Получение объекта очереди диалогов агента, валидный agent_id')
    def test_all_dialog_queue_valid(self, pool_api_v3, params_agent_uuid, creation_queue_dialog):
        params = {**{"page": "1",
                     "by_count": "100"}, **params_agent_uuid}
        path = pool_api_v3.path_end_point['get_all_dialog_queue']
        response = pool_api_v3.request_send(path=path, params=params)
        assert response.status_code == 200
        assert len(response.json()['dialogs']) <= response.json()['total']
        assert response.json()['total'] > 0
        assert len(response.json()['dialogs']) > 0
        upload_msisdn_list = [item['msisdn'] for item in creation_queue_dialog]
        for call in response.json()['dialogs']:
            assert call['msisdn'] in upload_msisdn_list

    @allure.feature('Получение размера очереди диалогов агента, валидный agent_id')
    def test_get_dialog_queue_size_valid(self, pool_api_v3, params_agent_uuid, creation_queue_dialog):
        path = pool_api_v3.path_end_point['get_dialog_queue_size']
        response = pool_api_v3.request_send(path=path, params=params_agent_uuid)
        assert response.status_code == 200

    @allure.feature('Отложить один диалог, валидный')
    def test_defer_one_dialog_valid(self, pool_api_v3, params_agent_uuid, creation_queue_dialog):
        with allure.step('Получение списка всех диалогов'):
            response_list_dialogs = pool_api_v3.request_send(path=pool_api_v3.path_end_point['get_all_dialog_queue'],
                                                             params={**{"page": "1",
                                                                        "by_count": "100"}, **params_agent_uuid})
            dialog_id = response_list_dialogs.json()['dialogs'][0]['id']

        with allure.step('Ставим на паузу один диалог'):
            path = pool_api_v3.path_end_point['defer_dialog']
            params = {**{'dialog_id': str(dialog_id)}, **params_agent_uuid}
            response = pool_api_v3.request_send(method='POST', path=path, params=params)
            assert response.status_code == 200

        with allure.step('Получение списка всех диалогов, проверка, что отложенного диалого нет в списке'):
            response_list_dialogs = pool_api_v3.request_send(path=pool_api_v3.path_end_point['get_all_dialog_queue'],
                                                             params={**{"page": "1",
                                                                        "by_count": "100"}, **params_agent_uuid})
            list_dialog_id = [dialog['id'] for dialog in response_list_dialogs.json()['dialogs']]
            assert dialog_id not in list_dialog_id

    @allure.feature('Отложить все диалоги для проекта')
    def test_defer_all_dialogs(self, pool_api_v3, params_agent_uuid, creation_queue_dialog):
        path = pool_api_v3.path_end_point['defer_dialog']
        response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_uuid)
        assert response.status_code == 200

        response = pool_api_v3.request_send(path=pool_api_v3.path_end_point['get_all_dialog_queue'],
                                            params={**{"page": "1",
                                                       "by_count": "100"}, **params_agent_uuid})
        assert response.json()['total'] == 0
        assert len(response.json()['dialogs']) == 0

    @allure.feature('Вернуть все диалоги из отложенных, валидный agent_id')
    def test_return_all_dialog_valid(self, pool_api_v3, params_agent_uuid, creation_queue_dialog):
        path = pool_api_v3.path_end_point['return_dialog']
        response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_uuid)
        assert response.status_code == 200

        response = pool_api_v3.request_send(path=pool_api_v3.path_end_point['get_all_dialog_queue'],
                                            params={**{"page": "1",
                                                       "by_count": "100"}, **params_agent_uuid})
        assert len(response.json()['dialogs']) == response.json()['total']
        assert response.json()['total'] > 0
        assert len(response.json()['dialogs']) > 0

    @allure.feature('Вернуть один диалог из отложенных, валидный')
    def test_return_one_dialog_valid(self, pool_api_v3, params_agent_uuid, creation_queue_dialog):
        with allure.step('Получение списка всех диалогов'):
            response_list_dialogs = pool_api_v3.request_send(path=pool_api_v3.path_end_point['get_all_dialog_queue'],
                                                             params={**{"page": "1",
                                                                        "by_count": "100"}, **params_agent_uuid})
            dialog_id = response_list_dialogs.json()['dialogs'][0]['id']

        with allure.step('Ставим на паузу один диалог'):
            path = pool_api_v3.path_end_point['defer_dialog']
            params = {**{'dialog_id': str(dialog_id)}, **params_agent_uuid}
            pool_api_v3.request_send(method='POST', path=path, params=params)

        with allure.step('Возвращаем с паузы диалог'):
            path = pool_api_v3.path_end_point['return_dialog']
            params = {**{'dialog_id': str(dialog_id)}, **params_agent_uuid}
            response = pool_api_v3.request_send(method='POST', path=path, params=params)
            assert response.status_code == 200

        with allure.step('Получение списка всех диалогов, проверка что отложенный диалог появился в списке'):
            params = {**{"page": "1", "by_count": "100"}, **params_agent_uuid}
            response_list_dialogs = pool_api_v3.request_send(path=pool_api_v3.path_end_point['get_all_dialog_queue'],
                                                             params=params)
            list_dialog_id = [dialog['id'] for dialog in response_list_dialogs.json()['dialogs']]
            assert dialog_id in list_dialog_id

    @allure.feature('Отменить все далоги для проекта, валидный agent_id')
    def test_cancel_all_dialog_valid(self, pool_api_v3, params_agent_uuid, creation_queue_dialog):
        path = pool_api_v3.path_end_point['cancel_all_dialogs']
        response = pool_api_v3.request_send(method='DELETE', path=path, params=params_agent_uuid)
        assert response.status_code == 200
        response = pool_api_v3.request_send(path=pool_api_v3.path_end_point['get_all_dialog_queue'],
                                            params={**{"page": "1",
                                                       "by_count": "100"}, **params_agent_uuid})
        assert response.json()['total'] == 0
        assert len(response.json()['dialogs']) == 0

    @allure.feature('Получить диалоги')
    def test_get_dialogs(self, pool_api_v3, creation_queue_dialog):
        path = pool_api_v3.path_end_point['get_dialogs']
        response = pool_api_v3.request_send(path=path)
        assert response.status_code == 200
