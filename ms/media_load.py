import requests
import json
import time

token = ""
result = []
times = []


def auth():
    global token
    url = "https://api-test-v3.neuro.net/api/v2/ext/auth"

    payload = "{\n\n}"
    headers = {
        'Content-type': "application/json",
        'Authorization': "Basic aWtvc2hraW5AbmV1cm8ubmV0Omlrb3Noa2lu"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    token = get_value(json.loads(response.text), "token")
    # print(response.text)
    # print(token)
    return token


def get_value(response, value):
    return response[value]


def init_bridged_dialog():
    global token
    url = "https://api-test-v3.neuro.net/api/v2/ext/dialog/dialog-initial"

    querystring = {"agent_uuid": "b5b2a743-259b-4641-a007-0dd2abe3e0fa"}

    payload = "{\n  \"msisdn\": \"55555\",\n  \"script_name\": \"media\",\n  \"script_entry_point\": \"main\"\n}"
    headers = {
        'content-type': "application/json",
        'Authorization': "Bearer %s" % token
    }
    # print(headers)
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    # print(response.text)
    time.sleep(5)


def init_dialog_with_recog():
    url = "https://api-test-v3.neuro.net/api/v2/ext/dialog/dialog-initial"

    querystring = {"agent_uuid": "82034644-98ed-4ced-acb7-98017b9ad5ce"}

    payload = "{\n  \"msisdn\": \"55555\",\n  \"script_name\": \"smoke_media_server\",\n  \"script_entry_point\": \"main_online\"\n}"
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer %s" % token}
    t = time.perf_counter()
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    t2 = time.perf_counter()
    times.append({t2 - t})
    time.sleep(5)

    # print(response)


def get_calls():
    url = "http://10.129.0.108:8088/get_calls_number"
    payload = ""
    t = time.perf_counter()
    response = requests.request("GET", url, data=payload, timeout=15)
    t2 = time.perf_counter()
    print(t2-t)
    times.append({t2 - t})
    result.append((json.loads(response.text)["calls_number"]))
    return json.loads(response.text)["calls_number"]


def rtest():
    auth()
    resp = get_calls()
    print(resp)
    while resp < 160:
        try:
            init_bridged_dialog()
            init_dialog_with_recog()
            resp = get_calls()
            print(resp)
            time.sleep(3)
        except TimeoutError:
            init_dialog_with_recog()
            print("timer", times)
            print("channel limit", result)
    print(times)
    print(result)


if __name__ == '__main__':
    rtest()
