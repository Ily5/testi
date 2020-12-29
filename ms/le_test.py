import requests
import time
import json
times = []
result = []


def get_calls():
    url = "http://10.129.0.108:8088/get_calls_number"
    payload = ""
    t = time.perf_counter()
    response = requests.request("GET", url, data=payload, timeout=180)
    t2 = time.perf_counter()
    times.append({t2 - t})
    result.append(response)
    print(json.loads(response.text)["calls_number"])
    print(times)
    return response


if __name__ == '__main__':
    get_calls()
