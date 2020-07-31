import json


class AsrHelper:

    def __init__(self, app):
        self.app = app
        self.knowns = []
        self.detect = []
        self.val = 0

    def get_data(self, response):
        json = self.app.api.get_json(response.json())
        return json["result"]["call_id"]

    def get_wer(self, known, detected):
        extend = len(known)
        match = [s for s in detected if s in known]
        detected = list(set(detected) - set(match))
        known = list(set(known) - set(match))
        for t in known:
            strt = t[:-1]
            if len(strt) >= 2:
                self.knowns.append(strt)
            else:
                self.val += 1
        for y in detected:
            strt = y[:-1]
            if len(strt) >= 2:
                self.detect.append(strt)
            else:
                self.val += 1
        matchs = [s for s in self.detect if s in self.knowns]
        detect = list(set(self.detect) - set(matchs))
        knowns = list(set(self.knowns) - set(matchs))
        wer = (self.val + len(detect) + len(knowns)) / extend
        self.knowns = []
        self.detect = []
        self.val = 0
        print(wer)
        return wer


