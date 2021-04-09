from typing import Optional, Union, Tuple, List, Dict, DefaultDict, Any
import requests

from test_3.fixture.api import APIClientV3


class CmsApi(APIClientV3):
    def get_call_logs(self, call_uuid: str) -> requests.Response:
        return self.request_send(
            path=f"{self.path_end_point['get_call_logs']}{call_uuid}"
        )

    def get_call_nn_log(self, call_uuid: str) -> Dict[str, str]:
        nn_logs = dict(call_uuid=call_uuid)
        resp = self.get_call_logs(call_uuid).json()["data"]
        for action in resp:
            if "nn.log" in action["action"]:
                nn_logs[action["name"]] = action["data"]
        return nn_logs

    def get_calls_agent_in_queue(
            self,
            agent_uuid: str,
            msisdn: Optional[str] = None,
            result: Optional[str] = None,
            bulk_uuid: Optional[str] = None,
            call_uuid: Optional[str] = None,
            sort: Optional[str] = None,
            field_sort: Optional[str] = None,
            limit=2000,
            offset=0,
    ) -> requests.Response:
        """" Метод получения звонков агента
        :param agent_uuid: обязательный параметр, передаем agent_uuid
        :param msisdn: необязательно, передаем для фильтрации по номеру
        :param result: необязательо, передаем для фильтрации по статусу
        :param bulk_uuid: необязательно, передаем для фильтрации по bulk_uuid
        :param call_uuid: необязательно, передаем для для фильтрации по call_uuid
        :param sort: необязательно, передаем для активации сортировки: asc, desc, так же небходимо передать field_sort
        :param field_sort: обязательно, если sort is not None, передаем выбора параметра сортировки: result, date_added
        :param limit: количество выводимых звонков, по дефолту 2000
        :param offset: количетсов пропускаемых звонков, по дефолту 0
        """

        request_data = {
            "limit": limit,
            "offset": offset,
            "where": {"agent_uuid": agent_uuid, "msisdn": [], "result": []},
        }
        if msisdn is not None:
            request_data['where']["msisdn"].append(msisdn)
        if result is not None:
            request_data['where']["result"].append(result)
        if call_uuid is not None:
            request_data["where"]["call_uuid"] = call_uuid
        if bulk_uuid is not None:
            request_data["where"]["bulk_uuid"] = bulk_uuid
        if sort is not None:
            if sort not in ["asc", "desc"]:
                raise ValueError("Param sort must be asc or desc")
            if field_sort not in ["result", "date_added"]:
                raise ValueError("Param field_sort must be result or date_added")
            request_data["sort"] = {}
            request_data["sort"][field_sort] = sort

        return self.request_send(
            method="POST",
            path=self.path_end_point["get_calls_agent_in_queue"],
            json=request_data,
        )
