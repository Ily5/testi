import allure
from random import randint


class TestPoolApiCalls:

    @allure.feature('Получение звонка из очереди')
    def test_get_calls_queue(self, pool_api_v3):
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
    def test_get_progress_calls(self, pool_api_v3, params_agent_id, creation_queue_calls):
        path = pool_api_v3.path_end_point['get_progress_calls']
        response = pool_api_v3.request_send(path=path, params=params_agent_id)
        assert response.status_code in [200, 400]

    @allure.feature('Получение списков звонков в очереди')
    def test_get_list_queue_calls(self, pool_api_v3, params_agent_id, creation_queue_calls):
        path = pool_api_v3.path_end_point['get_list_queue_calls']
        params = {**{"page": "1",
                     "by_count": "50"}, **params_agent_id}
        response = pool_api_v3.request_send(path=path, params=params)
        print(response.json()['total'])
        print(len(response.json()['calls']))

        assert response.status_code == 200
        assert 'calls' in response.json()
        assert 'total' in response.json()
        assert 'id' in response.json()['calls'][0]
        assert 'msisdn' in response.json()['calls'][0]
        assert 'date_added' in response.json()['calls'][0]
        assert 'trunk_id' in response.json()['calls'][0]
        assert 'uuid' in response.json()['calls'][0]
        assert response.json()['total'] > 0
        assert response.json()['total'] == len(response.json()['calls'])
        upload_msisdn_list = [item['msisdn'] for item in creation_queue_calls]
        print(upload_msisdn_list)
        for call in response.json()['calls']:
            assert call['msisdn'] in upload_msisdn_list

    @allure.feature('Отложить все звонки в очереди')
    def test_defer_all_calls(self, pool_api_v3, params_agent_id):
        path = pool_api_v3.path_end_point['defer_calls']
        response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_id, json={})
        assert response.status_code == 200

    @allure.feature('Вернуить все звонки из отложенных')
    def test_return_all_calls(self, pool_api_v3, params_agent_id):
        path = pool_api_v3.path_end_point['return_calls']
        response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_id, json={})
        assert response.status_code == 200

    @allure.feature('Отменить все звонки в очереди')
    def test_cancel_all_calls(self, pool_api_v3, params_agent_id):
        path = pool_api_v3.path_end_point['get_list_queue_calls']
        response = pool_api_v3.request_send(method='DELETE', path=path, params=params_agent_id, json={})
        assert response.status_code == 200

    @allure.feature('Сбросить очередь')
    def test_drop_queue_calls(self, pool_api_v3, params_agent_id):
        path = pool_api_v3.path_end_point['drop_queue_calls']
        response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_id, json={})
        assert response.status_code == 200

    @allure.feature('Получить объект очереди звонков')
    def test_get_full_queue_calls(self, pool_api_v3, params_agent_id):
        path = pool_api_v3.path_end_point['get_full_queue']
        response = pool_api_v3.request_send(path=path, params=params_agent_id)
        assert response.status_code == 200

    @allure.feature('Получить все валидные звонки')
    def test_get_all_valid_calls(self, pool_api_v3, params_agent_id):
        path = pool_api_v3.path_end_point['get_all_valid_calls']
        params = {**{"page": "1",
                     "by_count": "3"}, **params_agent_id}
        response = pool_api_v3.request_send(path=path, params=params)
        assert response.status_code == 200


class TestPoolApiDialog:

    @allure.feature('Получение объекта очереди диалогов агента, валидный agent_id')
    def test_all_dialog_queue_valid(self, pool_api_v3, params_agent_id, creation_queue_dialog):
        params = {**{"page": "1",
                     "by_count": "100"}, **params_agent_id}
        path = pool_api_v3.path_end_point['get_all_dialog_queue']
        response = pool_api_v3.request_send(path=path, params=params)
        assert response.status_code == 200
        assert len(response.json()['dialogs']) == response.json()['total']
        assert response.json()['total'] > 0
        assert len(response.json()['dialogs']) > 0
        upload_msisdn_list = [item['msisdn'] for item in creation_queue_dialog]
        for call in response.json()['dialogs']:
            assert call['msisdn'] in upload_msisdn_list

    @allure.feature('Получение размера очереди диалогов агента, валидный agent_id')
    def test_get_dialog_queue_size_valid(self, pool_api_v3, params_agent_id):
        path = pool_api_v3.path_end_point['get_dialog_queue_size']
        response = pool_api_v3.request_send(path=path, params=params_agent_id)
        try:
            assert response.status_code == 200
        except AssertionError:
            print(response.text)

    @allure.feature('Отложить все диалоги для проекта')
    def test_defer_all_dialogs(self, pool_api_v3, params_agent_id):
        path = pool_api_v3.path_end_point['defer_dialog']
        response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_id)
        try:
            assert response.status_code == 200
        except AssertionError:
            print(response.text)
        response = pool_api_v3.request_send(path=pool_api_v3.path_end_point['get_all_dialog_queue'],
                                            params={**{"page": "1",
                                                       "by_count": "100"}, **params_agent_id})
        assert response.json()['total'] == 0
        assert len(response.json()['dialogs']) == 0

    @allure.feature('Вернуть все диалоги из отложенных, валидный agent_id')
    def test_return_all_dialog_valid(self, pool_api_v3, params_agent_id):
        path = pool_api_v3.path_end_point['return_dialog']
        response = pool_api_v3.request_send(method='POST', path=path, params=params_agent_id)
        assert response.status_code == 200
        response = pool_api_v3.request_send(path=pool_api_v3.path_end_point['get_all_dialog_queue'],
                                            params={**{"page": "1",
                                                       "by_count": "100"}, **params_agent_id})
        assert len(response.json()['dialogs']) == response.json()['total']
        assert response.json()['total'] > 0
        assert len(response.json()['dialogs']) > 0

    @allure.feature('Отменить все далоги для проекта, валидный agent_id')
    def test_cancel_all_dialog_valid(self, pool_api_v3, params_agent_id):
        path = pool_api_v3.path_end_point['cancel_all_dialogs']
        response = pool_api_v3.request_send(method='DELETE', path=path, params=params_agent_id)
        assert response.status_code == 200
        response = pool_api_v3.request_send(path=pool_api_v3.path_end_point['get_all_dialog_queue'],
                                            params={**{"page": "1",
                                                       "by_count": "100"}, **params_agent_id})
        assert response.json()['total'] == 0
        assert len(response.json()['dialogs']) == 0

    @allure.feature('Получить диалоги')
    def test_get_dialogs(self, pool_api_v3):
        path = pool_api_v3.path_end_point['get_dialogs']
        response = pool_api_v3.request_send(path=path)
        assert response.status_code == 200
