import requests
import json


class ApiHelper:

    def __init__(self, app_3):
        self.app = app_3
        self.url = "https://api-test-v3.neuro.net/api/v2/ext/auth"
        self.querystring = None
        self.payload = ""
        self.headers = None

    def auth(self):
        self.headers = {
            'content-type': "multipart/form-data; boundary=---011000010111000001101001",
            'authorization': "Basic aWtvc2hraW5AbmV1cm8ubmV0Omlrb3Noa2lu"
        }

        response = requests.request("POST", self.url, data=self.payload, headers=self.headers)
        token = self.get_value(json.loads(response.text), "token")
        # print(response.text)
        return token

    def init_dialog(self, token, number):
        self.url = "https://api-test-v3.neuro.net/api/v2/ext/dialog/dialog-initial"
        self.querystring = {"agent_uuid": "b5b2a743-259b-4641-a007-0dd2abe3e0fa"}
        self.payload = "{\n\"msisdn\": \"%s\",\n\"script_entry_point\": \"main\"\n}" % number
        self.headers = {
            'content-type': "application/json",
            'authorization': "Bearer %s" % token
        }

        response = requests.request("POST", self.url, data=self.payload,
                                    headers=self.headers, params=self.querystring)
        uuid = self.get_value(json.loads(response.text), "dialog_uuid")
        return uuid

    def set_params(self, token, asr, tts):
        self.url = "https://api-test-v3.neuro.net/api/v2/ext/agent-settings/general"
        self.querystring = {"agent_uuid": "b5b2a743-259b-4641-a007-0dd2abe3e0fa"}

        self.payload = {"asr": asr, "tts": tts}
        self.headers = {
            'content-type': "application/json",
            'authorization': "Bearer %s" % token
        }
        response = requests.request("PUT", self.url, data=json.dumps(self.payload), headers=self.headers,
                                    params=self.querystring)
        print(response.text)

    def set_yandex(self, token):
        self.url = "https://api-test-v3.neuro.net/api/v2/rbac/agent/b5b2a743-259b-4641-a007-0dd2abe3e0fa"

        # self.payload = json_yandex
        self.headers = {
            'content-type': "application/json",
            'authorization': "Bearer %s" % token
        }

        response = requests.request("PUT", self.url, data=json.dumps(self.payload), headers=self.headers)

        print(response.text)

    def set_google(self, token):
        self.url = "https://api-test-v3.neuro.net/api/v2/rbac/agent/b5b2a743-259b-4641-a007-0dd2abe3e0fa"

        # self.payload = json_google
        self.headers = {
            'content-type': "application/json",
            'authorization': "Bearer %s" % token
        }

        response = requests.request("PUT", self.url, data=json.dumps(self.payload), headers=self.headers)

        print(response.text)

    def get_value(self, response, value):
        return response[value]


class APIClientV3:

    def __init__(self, base_url=None, token=None, company_uuid=None):
        self.base_url = base_url
        self.token = token
        self.company_uuid = company_uuid

    def request_send(self, method='GET', path=None, params=None, data=None):
        if path is None:
            request_url = self.base_url
        else:
            request_url = self.base_url + path
        if method != 'GET':
            headers = {**{'content-type': "application/json"}, **self.token}
            print(headers)
        else:
            headers = self.token
        return requests.request(method=method, url=request_url, params=params, data=data, headers=headers)

    def get_token(self, login, password):
        response = requests.request(url=self.base_url + '/api/v2/ext/auth', method='POST', auth=(login, password))
        token = response.json()['token']
        return {'Authorization': "Bearer %s" % token}
        # print(response)
