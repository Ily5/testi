import requests
import json
import time
import random
import logging
from test_3.fixture.api import APIClientV3




def get_value(response, value):
    return response[value]


class MediaHelper:

    def __init__(self):
        self.url = "https://api-test-v3.neuro.net/api/v2/ext/auth"
        self.payload = "{}"
        self.headers = {
            'Content-type': "application/json",
            'Authorization': "Basic aWtvc2hraW5AbmV1cm8ubmV0Omlrb3Noa2lu"
            # 'Authorization': "Basic aWtvc2hraW5AbmV1cm8ubmV0OjEyMzQ1Ng=="
        }
        self.querystring = {"agent_uuid": "61664bbc-3826-4107-85bd-5b093c9e1909"}
        self.times = []
        self.result = []
        logging.basicConfig(filename=None, level=logging.INFO,
                            format='%(asctime)s  - %(levelname)s - %(message)s')

    def auth(self):
        response = requests.request("POST", self.url, data=self.payload, headers=self.headers)
        token = get_value(json.loads(response.text), "token")
        return token

    def init_dialog_with_recog(self, token, delay):
        self.url = "https://api-test-v3.neuro.net/api/v2/ext/dialog/dialog-initial"

        payload = "{\n  \"phone\": \"%d\",\n  \"script_name\": \"outgoing_call\",\n  \"script_entry_point\": \"main\"\n}" % random.randrange(
            90000, 90019)
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer %s" % token}
        # t = time.perf_counter()
        response = requests.request("POST", self.url, data=payload, headers=headers, params=self.querystring)
        # t2 = time.perf_counter()
        # self.times.append({t2 - t})
        # time.sleep(delay)
        return response
        # print(response)

    def push_dialogs(self, token, value):
        self.url = "https://api-test-v3.neuro.net/api/v2/ext/dialog/dialog-initial"
        z = 0
        while z < value:
            payload = "{\n  \"phone\": \"%d\",\n  \"script_name\": \"outgoing_call\",\n  \"script_entry_point\": \"main\"\n}" % random.choice(
                [
                    90017, 90009, 90012, 90016, 90008, 90010, 90015])
            headers = {
                'content-type': "application/json",
                'authorization': "Bearer %s" % token}
            response = requests.request("POST", self.url, data=payload, headers=headers, params=self.querystring)
            z += 1
        # return response

    # def get_calls(self):
    #     self.url = "http://10.131.0.60:8088/get_calls_number"
    #     self.payload = ""
    #     t = time.perf_counter()
    #     response = requests.request("GET", self.url, data=self.payload, timeout=15)
    #     t2 = time.perf_counter()
    #     print(t2 - t)
    #     self.times.append({t2 - t})
    #     self.result.append((json.loads(response.text)["calls_number"]))
    #     return json.loads(response.text)["calls_number"]

    def get_active_calls(self, token):
        self.url = "https://api-test-v3.neuro.net/api/v2/ext/queue/call"
        self.headers = {
            'content-type': "application/json",
            'authorization': "Bearer %s" % token}
        self.payload = "{\"limit\":1000,\"offset\":0,\"where\":{" \
                       "\"agent_uuid\":\"61664bbc-3826-4107-85bd-5b093c9e1909\",\"msisdn\":[],\"result\":[" \
                       "\"active\"]}} "

        response = requests.request("POST", self.url, data=self.payload, headers=self.headers, params=self.querystring)
        print(response.json()['total_count'])
        return response.json()['total_count']

    def get_calls(self, token):
        self.url = "https://api-test-v3.neuro.net/api/v2/ext/queue/call"
        self.headers = {
            'content-type': "application/json",
            'authorization': "Bearer %s" % token}
        self.payload = "{\"limit\":1000,\"offset\":0,\"where\":{" \
                       "\"agent_uuid\":\"61664bbc-3826-4107-85bd-5b093c9e1909\",\"msisdn\":[],\"result\":[" \
                       "\"active\"]}} "

        response = requests.request("GET", self.url, data=self.payload, headers=self.headers, params=self.querystring)
        print(response.json()['total_count'])
        return response.json()['total_count']

    def get_la(self):
        self.url = "http://10.129.0.108:8088/get_la"
        response = requests.request("get", self.url, data=self.payload, headers=self.headers, params=self.querystring)
        logging.info("la_ms_1: " + str(response.json()))
        # print("la_ms_1: " + str(response.json()))
        self.url = "http://10.131.0.60:8088/get_la"
        response = requests.request("get", self.url, data=self.payload, headers=self.headers, params=self.querystring)
        logging.info("la_ms_2: " + str(response.json()))
        # print("la_ms_2: " + str(response.json()))
        return response

    def set_media_params_release_project(self, engine: str):
        data = {"speed": 1,
                "pitch": 1,
                "name": "load_gett"}

        if engine in 'yandex':
            data['tts_key_uuid'] = "86988b9a-35dd-4e4b-bda9-fcc943acb86c"
            data['asr_key_uuid'] = "148ef1f0-d81e-415a-8c0b-26c7319138b1"
            data['tts_voice'] = "zahar"

        #          "asr_google_uuid": "68828df6-fabb-4f01-a32b-1359512fd66c",
        #       "tts_google_uuid": "b90fecf7-96c3-48e9-b8a7-8f8ca8280eed",
        #       "google_voice": "ru-RU-Wavenet-E",
        elif engine in 'neuro':
            data['tts_key_uuid'] = "86988b9a-35dd-4e4b-bda9-fcc943acb86c"
            data['asr_key_uuid'] = "ccdca58f-2976-417e-876b-b59a5b914e90"
            data['tts_voice'] = "zahar"
        elif engine in 'google':
            data['tts_key_uuid'] = self.test_data['data_release_run']['tts_google_uuid']
            data['asr_key_uuid'] = self.test_data['data_release_run']['asr_google_uuid']
            data['tts_voice'] = self.test_data['data_release_run']['google_voice']
        if engine.lower() not in ['google', 'yandex']:
            raise ValueError('Engine must be yandex or google')

        path = self.path_end_point['set_media_params'] + self.test_data['data_release_run']['agent_uuid']
        return self.request_send(method="PUT", path=path, json=data).json()