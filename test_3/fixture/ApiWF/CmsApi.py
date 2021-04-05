from typing import Optional, Union, Tuple, List, Dict, DefaultDict
import requests

from test_3.fixture.api import APIClientV3


class CmsApi(APIClientV3):
    def get_call_logs(self, call_uuid: str) -> requests.Response:
        return self.request_send(
            path=f"{self.path_end_point['get_call_logs']}{call_uuid}"
        )

    def get_call_nn_log(self, call_uuid: str) -> Dict[str, str]:
        nn_logs = dict(call_uuid=call_uuid)
        resp = self.get_call_logs(call_uuid).json()['data']
        for action in resp:
            if 'nn.log' in action['action']:
                nn_logs[action['name']] = action['data']
        return nn_logs


