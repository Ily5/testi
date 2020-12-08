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
        # print(response.text)

    def set_yandex(self, token):
        self.url = "https://api-test-v3.neuro.net/api/v2/rbac/agent/b5b2a743-259b-4641-a007-0dd2abe3e0fa"

        self.payload = json_yandex
        self.headers = {
            'content-type': "application/json",
            'authorization': "Bearer %s" % token
        }

        response = requests.request("PUT", self.url, data=json.dumps(self.payload), headers=self.headers)

        # print(response.text)

    def set_google(self, token):
        self.url = "https://api-test-v3.neuro.net/api/v2/rbac/agent/b5b2a743-259b-4641-a007-0dd2abe3e0fa"

        self.payload = json_google
        self.headers = {
            'content-type': "application/json",
            'authorization': "Bearer %s" % token
        }

        response = requests.request("PUT", self.url, data=json.dumps(self.payload), headers=self.headers)

        print(response.text)

    def get_value(self, response, value):
        return response[value]


json_yandex = {
    "delay": "00:05:00",
    "recall_count": 11,
    "trunk_uuid": "2a5cd86c-5344-42db-a25d-ca1cf10191c4",
    "trunk": {
        "uuid": "2a5cd86c-5344-42db-a25d-ca1cf10191c4",
        "name": "sip-client-test"
    },
    "total_channel_limit": 3,
    "pool_uuid": "4ffb0835-8443-4af0-9bf8-30ddfccb9796",
    "pool": {
        "uuid": "4ffb0835-8443-4af0-9bf8-30ddfccb9796",
        "name": "test-pool"
    },
    "asr": "yandex",
    "tts": "oksana@yandex",
    "asr_key_uuid": "148ef1f0-d81e-415a-8c0b-26c7319138b1",
    "asr_key": {
        "uuid": "148ef1f0-d81e-415a-8c0b-26c7319138b1",
        "name": "yandex_key",
        "platform": "yandex"
    },
    "tts_key_uuid": "86988b9a-35dd-4e4b-bda9-fcc943acb86c",
    "tts_key": {
        "uuid": "86988b9a-35dd-4e4b-bda9-fcc943acb86c",
        "name": "yandex",
        "platform": "yandex"
    },
    "tts_voice": "oksana",
    "uuid": "b5b2a743-259b-4641-a007-0dd2abe3e0fa",
    "name": "release_run",
    "timezone": "Europe/Moscow",
    "description": "release_run",
    "company_uuid": "9db4c04b-deca-480f-ad1f-9399a28ecffa",
    "company": {
        "uuid": "9db4c04b-deca-480f-ad1f-9399a28ecffa",
        "name": "QA Team",
        "timezone": None
    },
    "flag": "test_release",
    "language": "ru-RU"
}

json_google = {
    "delay": "00:05:00",
    "recall_count": 11,
    "trunk_uuid": "2a5cd86c-5344-42db-a25d-ca1cf10191c4",
    "trunk": {
        "uuid": "2a5cd86c-5344-42db-a25d-ca1cf10191c4",
        "name": "sip-client-test"
    },
    "total_channel_limit": 3,
    "pool_uuid": "4ffb0835-8443-4af0-9bf8-30ddfccb9796",
    "pool": {
        "uuid": "4ffb0835-8443-4af0-9bf8-30ddfccb9796",
        "name": "test-pool"
    },
    "asr": "google",
    "tts": "ru-RU-Wavenet-A@google",
    "asr_key_uuid": "68828df6-fabb-4f01-a32b-1359512fd66c",
    "asr_key": {
        "uuid": "68828df6-fabb-4f01-a32b-1359512fd66c",
        "name": "google_asr",
        "platform": "google"
    },
    "tts_key_uuid": "b90fecf7-96c3-48e9-b8a7-8f8ca8280eed",
    "tts_key": {
        "uuid": "b90fecf7-96c3-48e9-b8a7-8f8ca8280eed",
        "name": "google_tts",
        "platform": "google"
    },
    "tts_voice": "ru-RU-Wavenet-A",
    "uuid": "b5b2a743-259b-4641-a007-0dd2abe3e0fa",
    "name": "release_run",
    "timezone": "Europe/Moscow",
    "description": "release_run",
    "company_uuid": "9db4c04b-deca-480f-ad1f-9399a28ecffa",
    "company": {
        "uuid": "9db4c04b-deca-480f-ad1f-9399a28ecffa",
        "name": "QA Team",
        "timezone": None
    },
    "flag": "test_release",
    "language": "ru-RU"
}



