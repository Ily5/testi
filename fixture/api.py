import requests
import json


class ApiHelper:
    def __init__(self, app):
        self.url = app.api_url
        self.headers = app.api_headers
        self.methods = app.api_methods
        self.app = app

    def get_methods(self, s):
        methods = self.methods
        if s == 'agent':
            new_methods = list(filter(lambda x: s in x, methods))
        # elif s == 'others':
        # new_methods=list(filter(lambda x: 'agent','initial','output' is not in x, methods)
        return new_methods

    def get_json(self, s):
        try:
            s = json.dumps(s)
            return json.loads(s)
        except ConnectionError:
             print("Connection error")


    def get_agents(self):
        data = {"jsonrpc": "2.0", "method": "get_agents", "id": "test"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def set_agent_param(self, agent_id, parameter, value):
        data = {"jsonrpc": "2.0", "method": "set_agent_param",
                "params": {"agent_id": agent_id, "param_name": parameter, "value": value},
                "id": "test"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def get_agent_param(self, agent_id, parameter):
        data = {"jsonrpc": "2.0",
                "method": "get_agent_param",
                "params": {
                    "agent_id": agent_id,
                    "param_name": parameter},
                "id": "test"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def get_agent_params(self, agent_id):
        data = {
            "jsonrpc": "2.0",
            "method": "get_agent_params",
            "params": {"agent_id": agent_id},
            "id": "test"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def get_initial_entities(self, agent_id):
        data = {"jsonrpc": "2.0", "method": "get_initial_entities", "params": {"agent_id": agent_id}, "id": "test"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def set_initial_entity(self, agent_id, name, type, number):
        data = {"jsonrpc": "2.0", "method": "set_initial_entity",
                "params": {"agent_id": agent_id, "initial_entity_name": name, "initial_entity_type": type,
                           "initial_entity_number_cell": number, "initial_entity_synthesis": 'false'}, "id": "test"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def get_initial_entity(self, agent_id, name):
        data = {"jsonrpc": "2.0", "method":
            "get_initial_entity", "params":
                    {"agent_id": agent_id, "initial_entity_name": name}, "id": "test"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def delete_initial_entity(self, agent_id, name):
        data = {"jsonrpc": "2.0", "method": "delete_initial_entity",
                "params": {"agent_id": agent_id, "initial_entity_name": name}, "id": "test"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def get_output_entities(self, agent_id):
        data = {"jsonrpc": "2.0", "method": "get_output_entities", "params": {"agent_id": agent_id}, "id": "tested"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def set_output_entity(self, agent_id, name, type, number):
        data = {"jsonrpc": "2.0", "method": "set_output_entity",
                "params": {"agent_id": agent_id, "output_entity_name": name, "output_entity_type": type,
                           "output_entity_number_cell": number}, "id": "tested"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def get_output_entity(self, agent_id, name):
        data = {"jsonrpc": "2.0", "method": "get_output_entity", "params":
            {"agent_id": agent_id, "output_entity_name": name}, "id": "test"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def delete_output_entity(self, agent_id, name):
        data = {"jsonrpc": "2.0", "method": "delete_output_entity",
                "params": {"agent_id": agent_id, "output_entity_name": name}, "id": "tested"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def initiate_call(self, agent_id, phone):
        data = {"jsonrpc": "2.0", "method": "initiate_call",
                "params": {"agent_id": agent_id, "phone": phone,
                           "name": "name", "id": "name2"}, "id": "test"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def initiate_bulk_calls(self, agent_id, phone):
        data = {"jsonrpc": "2.0", "method": "initiate_bulk_calls",
                "params": {"agent_id": agent_id,
                           "data": [{"phone": phone, "name": "name"}]}, "id": "test"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def get_data_by_bulk_id(self, agent_id, bulk_id):
        data = {"jsonrpc": "2.0", "method": "get_data_by_bulk_id",
                "params": {"agent_id": agent_id, "bulk_id": bulk_id}, "id": "test"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def get_data_by_call_group_id(self, agent_id, call_gr_id):
        data = {"jsonrpc": "2.0", "method": "get_data_by_call_group_id",
                "params": {"agent_id": agent_id, "call_group_id": call_gr_id}, "id": "tested"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def get_data_by_timeslot(self, agent_id, f, t):
        date_from = "2020-" + f + "T13:00:00Z"
        date_to = "2020-" + t + "T13:00:00Z"
        data = {"jsonrpc": "2.0", "method": "get_data_by_timeslot",
                "params": {"agent_id": agent_id, "from": date_from, "to": date_to
                           }, "id": "tested"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer

    def get_call_records(self, agent_id, file):
        data = {"jsonrpc": "2.0", "method": "get_call_records", "params":
            {"agent_id": agent_id, "record_session": file}, "id": "tested"}
        answer = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return answer


class PoolApiHelper:
    def __init__(self, app):
        self.url = app.pool_api
        self.headers = app.p_api_headers
        self.app = app

    def get_calls(self):
        answer = requests.get(self.url + '/get_calls')
        return answer

    def get_pending_calls(self, p_id):
        parameters = {'project_id': str(p_id)}
        answer = requests.get(self.url + '/pending', params=parameters)
        return answer

    def get_queued_calls(self, p_id, page, by):
        parameters = {'project_id': str(p_id), 'page': str(page), 'by_count': str(by)}
        answer = requests.get(self.url + '/queue', params=parameters)
        return answer

    def queue_defer(self, p_id):
        parameters = {'project_id': str(p_id)}
        answer = requests.post(self.url + '/queue/defer', params=parameters)
        return answer

    def queue_return(self, p_id):
        parameters = {'project_id': str(p_id)}
        answer = requests.post(self.url + '/queue/return', params=parameters)
        return answer

    def queue_clean(self, p_id):
        parameters = {'project_id': str(p_id)}
        answer = requests.delete(self.url + '/queue', params=parameters)
        return answer

    def queue_clean_call(self, p_id, c_id):
        parameters = {'project_id': str(p_id), 'call_id': str(c_id)}
        answer = requests.delete(self.url + '/queue', params=parameters)
        return answer

    def refresh_queue(self, p_id):
        parameters = {'project_id': str(p_id)}
        answer = requests.post(self.url + '/queue/flush', params=parameters)
        return answer

    def pending_count(self):
        answer = requests.get(self.url + '/pending_count')
        return answer
