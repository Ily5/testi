from typing import Optional, Union, Tuple, List, Dict, DefaultDict
import requests

from test_3.fixture.api import APIClientV3


class ExternalApi(APIClientV3):

    def upload_group_dialogs(
            self, agent_uuid: str, request_body: List[Dict[str, Union[str, int]]]
    ) -> requests.Response:
        return self.request_send(
            method="POST",
            path=self.path_end_point["upload_group_dialogs"],
            params={"agent_uuid": agent_uuid},
            json=request_body,
        )

    def change_base_agent_setting(
            self, agent_uuid: str, request_body: Dict[str, Union[int, str]]
    ) -> requests.Response:
        r""" "
        Изменять можно не все настройки проекта, только нижеследующие:
        {
        "delay": string,
        "recall_count": integer,
        "flag": string,
        "company_uuid": string,
        "routing_channel_limit": integer,
        "total_channel_limit": integer,
        "language": string,
        "asr": string,
        "tts": string
        }
        """
        return self.request_send(
            method="PUT",
            path=self.path_end_point["put_change_agent_settings"],
            params={"agent_uuid": agent_uuid},
            json=request_body,
        )

    def get_calls_agent(self, agent_uuid: str) -> requests.Response:
        return self.request_send(
            path=self.path_end_point["get_calls_agent"],
            params={"agent_uuid": agent_uuid}
        )

    def get_dialogs_agent(self, agent_uuid: str) -> requests.Response:
        return self.request_send(
            path=self.path_end_point["get_dialogs_agent"],
            params={"agent_uuid": agent_uuid}
        )
