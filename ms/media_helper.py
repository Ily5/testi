import requests
import json
import time
import random


def get_value(response, value):
    return response[value]


class MediaHelper:

    def __init__(self):
        self.url = "https://api-v3.neuro.net/api/v2/ext/auth"
        self.payload = "{}"
        self.headers = {
            'Content-type': "application/json",
            # 'Authorization': "Basic aWtvc2hraW5AbmV1cm8ubmV0Omlrb3Noa2lu"
            'Authorization': "Basic aWtvc2hraW5AbmV1cm8ubmV0OjEyMzQ1Ng=="

        }
        self.querystring = {"agent_uuid": "445fd938-58f3-4056-b6e0-2a9679a833d1"}
        self.times = []
        self.result = []

    def auth(self):
        response = requests.request("POST", self.url, data=self.payload, headers=self.headers)
        token = get_value(json.loads(response.text), "token")
        return token

    def init_dialog_with_recog(self, token):
        self.url = "https://api-v3.neuro.net/api/v2/ext/dialog/dialog-initial"

        payload = "{\n  \"phone\": \"%d\",\n  \"script_name\": \"outgoing_call\",\n  \"script_entry_point\": \"main\"\n}" % random.randrange(
            90000, 90019)
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer %s" % token}
        t = time.perf_counter()
        response = requests.request("POST", self.url, data=payload, headers=headers, params=self.querystring)
        t2 = time.perf_counter()
        self.times.append({t2 - t})
        time.sleep(5)
        return response
        # print(response)

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

    def get_calls(self, token):
        self.url = "https://api-v3.neuro.net/api/v2/ext/queue/dialog"
        self.headers = {
            'content-type': "application/json",
            'authorization': "Bearer %s" % token}
        response = requests.request("GET", self.url, data=self.payload, headers=self.headers, params=self.querystring)
        return response.json()['total_count']
