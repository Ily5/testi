import requests
import time


class APIClientV3:

    def __init__(self, base_url=None, token=None, refresh_token=None, test_data=None, path_end_point=None,
                 database=None, headers=None):
        self.base_url = base_url
        self.token = token
        self.refresh_token = refresh_token
        self.test_data = test_data
        self.path_end_point = path_end_point
        self.database = database
        self.api_headers = headers

    def request_send(self, method='GET', path=None, status_code=480, waiting_queue_sec=900, **kwargs):
        if path is None:
            request_url = self.base_url
        else:
            request_url = self.base_url + path

        headers = self.token

        count = 0
        while True:
            count += 1
            response = requests.request(method=method, url=request_url, headers=headers, **kwargs)
            if response.status_code != int(status_code):
                break
            if count % 10 == 0:
                print('\n Код ответа от сервера = {}'.format(response.status_code),
                      '-- попытка № {}'.format(count))
                print('\n', 'Message Error - {}'.format(response.text))
            time.sleep(0.5)
            if count > waiting_queue_sec * 2:
                print('Очередь занята более {} секунд '.format(waiting_queue_sec))
                raise TimeoutError('Превышено время отправки запроса')

        return response

    def get_api_token(self, login, password):
        response = requests.request(method='POST', url=self.base_url + '/api/v2/ext/auth', auth=(login, str(password)))
        token = response.json()['token']
        refresh_token = response.json()['refresh_token']
        return {'Authorization': "Bearer %s" % token}, refresh_token

    def set_media_params_release_project(self, engine: str):
        data = {"speed": 1,
                "pitch": 1,
                "name": self.test_data['data_release_run']['agent_name']}

        if engine in 'yandex':
            data['tts_key_uuid'] = self.test_data['data_release_run']['tts_yandex_uuid']
            data['asr_key_uuid'] = self.test_data['data_release_run']['asr_yandex_uuid']
            data['tts_voice'] = self.test_data['data_release_run']['yandex_voice']
        if engine in 'google':
            data['tts_key_uuid'] = self.test_data['data_release_run']['tts_google_uuid']
            data['asr_key_uuid'] = self.test_data['data_release_run']['asr_google_uuid']
            data['tts_voice'] = self.test_data['data_release_run']['google_voice']
        else:
            raise ValueError('Engine must be yandex or google')

        path = self.path_end_point['set_media_params'] + self.test_data['data_release_run']['agent_uuid']
        return self.request_send(method="PUT", path=path, json=data).json()

    def init_dialog(self, msisdn, agent: str):
        path = self.path_end_point['upload_dialog']
        data = {"msisdn": "{}".format(msisdn), "script_entry_point": "main"}
        params = {}
        if agent in "release_run":
            params['agent_uuid'] = self.test_data['data_release_run']['agent_uuid']
        else:
            params['agent_uuid'] = self.test_data['agent_uuid']
        return self.request_send(method="POST", path=path, params=params, json=data)
