import json
class AsrHelper:
    def __init__(self, app):
        self.app = app

    def get_data(self, response):
        json = self.app.api.get_json(response.json())
        return json["result"]["call_id"]
