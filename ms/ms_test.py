import json
import uuid
import time
import asyncio
import random
from aiohttp import ClientSession, ClientTimeout

array = []


class MediaApi:
    def __init__(self, pid, api_url):
        self.pid = pid
        self.uuid = uuid.uuid4()
        self._api_url = api_url
        self.response = None

    async def originate(self):
        await asyncio.sleep(random.randint(1, 3))
        json = {
            "uri": "sip:55555@10.129.0.112:5061",
            "X-Neuro-UUID": "%s" % str(self.uuid),
            "X-Via-Trunk": "sip-client"}
        response = await self.request('/originate', method='POST', json_body=dict(json))
        print('#{pid} {uuid} originate done, response: {response}'.format(pid=self.pid, uuid=self.uuid,
                                                                          response=response))

    async def write(self):
        await asyncio.sleep(random.randint(1, 3))
        json = {
            "action": {"write_record": "/neuro-files/test/%s.wav" % str(self.uuid)},
            "call": {"uuid": "%s" % str(self.uuid)}}
        response = await self.request('/calls/execute', method='PUT', json_body=dict(json))
        print('#{pid} {uuid} write done, response: {response}'.format(pid=self.pid, uuid=self.uuid,
                                                                      response=response))

    async def playback(self):
        await asyncio.sleep(random.randint(1, 3))
        json = {
            "action": {"playback": "/neuro-files/22222.wav"},
            "call": {"uuid": "%s" % str(self.uuid)}}
        response = await self.request('/calls/execute', method='PUT', json_body=dict(json))
        print('#{pid} {uuid} playback done, response: {response}'.format(pid=self.pid, uuid=self.uuid,
                                                                         response=response))

    async def set_background(self):
        await asyncio.sleep(random.randint(1, 3))
        json = {
            "action": {"set_background": "/neuro-files/back.wav"},
            "call": {"uuid": "%s" % str(self.uuid)}}
        response = await self.request('/calls/execute', method='PUT', json_body=dict(json))
        print('#{pid} {uuid} set_background done, response: {response}'.format(pid=self.pid, uuid=self.uuid,
                                                                               response=response))

    async def bridge(self):
        await asyncio.sleep(random.randint(1, 3))
        json = {
            "action": {"bridge":
                           {"sip_uri": "sip:55555@10.129.0.112:5061",
                            "channel": "sip-client"}},
            "call": {"uuid": "%s" % str(self.uuid)}}
        response = await self.request('/calls/execute', method='PUT', json_body=dict(json))
        print('#{pid} {uuid} bridge done, response: {response}'.format(pid=self.pid, uuid=self.uuid,
                                                                       response=response))

    async def hangup(self):
        await asyncio.sleep(random.randint(1, 3))
        json = {"action": {"hangup": True},
                "call": {"uuid": "%s" % str(self.uuid)}}
        response = await self.request('/calls/execute', method='PUT', json_body=dict(json))
        print('#{pid} {uuid} hangup done, response: {response}'.format(pid=self.pid, uuid=self.uuid, response=response))

    async def wait_for_call(self):
        # await asyncio.sleep(random.randint(5, 10))
        json = {"X-Neuro-UUID": "%s" % str(self.uuid)}
        response = await self.request('/wait_for_call', method='POST', json_body=dict(json))
        print('#{pid} {uuid} wait_for_call done, response: {response}'.format(pid=self.pid, uuid=self.uuid,
                                                                              response=response))
        print('#{pid} {uuid}, call duration is {duration}'.format(pid=self.pid, uuid=self.uuid,
                                                                  duration=response['call']['duration']))
        array.append(response['call']['duration'])
        return {'result': 'done'}

    async def request(self, url, method='GET', json_body: dict = None):
        # timeout = ClientTimeout(total=timeout)
        try:
            async with ClientSession() as session:
                async with session.request(method, '{api_url}{url}'.format(api_url=self._api_url, url=url),
                                           json=json_body) as resp:
                    response = await resp.json()
        except Exception:
            raise Exception("Failed to make request {api_url}{url}".format(api_url=self._api_url, url=url))

        if 'error' in response:
            raise ValueError('Invalid response: %s' % str(response['error']))

        return response


async def test_request(pid):
    print('#{pid} process started'.format(pid=pid))
    await asyncio.sleep(0.5)
    a = MediaApi(pid, 'http://10.129.0.12:8088')
    await a.originate()
    await a.write()
    # a.wait_for_answer()
    # a.update_callbacks()
    await a.set_background()
    await a.playback()
    await a.hangup()
    # await a.bridge()

    response = await a.wait_for_call()
    a.response = response
    return a


async def test_requests_asynchronous():
    start = time.time()
    # futures = []
    futures = [test_request(i) for i in range(1, 2)]
    # for i in range(1, 2):
    #     futures.append(test_request(i))
    #     time.sleep(1)
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        # print('#{i} {uuid}, {response}'.format(i=i, uuid=result.uuid, response=result.response))
        # print('#{i} {uuid}, call duration is {duration}'.format(i=i, uuid=result.uuid, duration=result.response['result']))

    print("Process took: {:.2f} seconds".format(time.time() - start))
    print(array)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_requests_asynchronous())
