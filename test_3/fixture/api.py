import requests


class APIClientV3:
    def __init__(
            self,
            base_url=None,
            token=None,
            refresh_token=None,
            test_data=None,
            path_end_point=None,
            database=None,
            headers=None,
    ):
        self.base_url = base_url
        self.token = token
        self.refresh_token = refresh_token
        self.test_data = test_data
        self.path_end_point = path_end_point
        self.database = database
        self.api_headers = headers

    def request_send(
            self, method="GET", path=None, **kwargs
    ):
        if path is None:
            request_url = self.base_url
        else:
            request_url = self.base_url + path

        headers = self.token

        response = requests.request(
            method=method, url=request_url, headers=headers, **kwargs
        )

        return response

    def get_api_token(self, login, password):
        response = requests.request(
            method="POST",
            url=self.base_url + "/api/v2/ext/auth",
            auth=(login, str(password)),
        )
        try:
            token = response.json()["token"]
            refresh_token = response.json()["refresh_token"]
            return {"Authorization": "Bearer %s" % token}, refresh_token
        except KeyError:
            print("\n Статус код при  получении токена", response.status_code)
            print("\n Тело ответа при получении токена", response.text)
            raise Exception("Get token error")

    def set_media_params_release_project(self, engine: str):
        data = {
            "speed": 1,
            "pitch": 1,
            "name": self.test_data["data_release_run"]["agent_name"],
        }

        if engine in "yandex":
            data["tts_key_uuid"] = self.test_data["data_release_run"]["tts_yandex_uuid"]
            data["asr_key_uuid"] = self.test_data["data_release_run"]["asr_yandex_uuid"]
            data["tts_voice"] = self.test_data["data_release_run"]["yandex_voice"]
            data["reserved_asr_key_uuid"] = self.test_data["data_release_run"]["asr_google_uuid"]
        if engine in "google":
            data["tts_key_uuid"] = self.test_data["data_release_run"]["tts_google_uuid"]
            data["asr_key_uuid"] = self.test_data["data_release_run"]["asr_google_uuid"]
            data["tts_voice"] = self.test_data["data_release_run"]["google_voice"]
            data["reserved_asr_key_uuid"] = self.test_data["data_release_run"]["asr_yandex_uuid"]
        if engine.lower() not in ["google", "yandex"]:
            raise ValueError("Engine must be yandex or google")

        path = (
                self.path_end_point["set_media_params"]
                + self.test_data["data_release_run"]["agent_uuid"]
        )
        return self.request_send(method="PUT", path=path, json=data).json()

    def init_dialog(self, msisdn, agent: str, api, default_logic=True):
        self.request_send(
            method="PUT",
            path=f"/api/v2/rbac/agent/{self.test_data['data_release_run']['agent_uuid']}",
            json={
                "name": self.test_data['data_release_run']['agent_name'],
                "default_priority": 3,
                "pool_uuid": self.test_data['pool_uuid'],
                "trunk_uuid": self.test_data['trunk_uuid'],
                "total_channel_limit": self.test_data['data_release_run']['total_channel_limit'],
                "language": self.test_data['data_release_run']['language'],
                "recall_count": self.test_data['data_release_run']['recall_count'],
                "flag": self.test_data['data_release_run']['agent_flag']

            },
        )
        params = {}

        if agent in "release_run":
            params["agent_uuid"] = self.test_data["data_release_run"]["agent_uuid"]
            if default_logic:
                api: APIClientV3
                body = {
                    **{"uuid": api.test_data["data_release_run"]["logic_uuid"]},
                    **params,
                }
                resp = api.request_send(
                    method="POST",
                    path="/api/v2/logic/logic_unit/default",
                    params=params,
                    json=body,
                )
                if resp.status_code != 200:
                    print(resp.status_code)
                    raise Exception("Change logic error")
        else:
            params["agent_uuid"] = self.test_data["agent_uuid"]
        return self.request_send(
            method="POST",
            path=self.path_end_point["upload_dialog"],
            params=params,
            json={"msisdn": "{}".format(msisdn), "script_entry_point": "main"},
        )
