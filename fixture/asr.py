import json
import time
import logging


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

        detect = list(set(self.detect) - set(matchs)) # лишние слова
        knowns = list(set(self.knowns) - set(matchs)) # нерасп-е слова
        wer = (self.val + len(detect) + len(knowns)) / extend
        self.knowns = []
        self.detect = []
        self.val = 0
        logging.info("Call error rate : %s " % wer )
        print(wer)
        return wer



    # def start_call(self, app, db):
    #     # initiate call with central api
    #     resp = app.api.initiate_call(63, "neutral_call")
    #     assert resp.status_code == 200
    #     # get call_id from api response
    #     call_id = app.asr.get_data(resp)
    #     # wait migration call to r/w base
    #     time.sleep(45)
    #     # check call status "+OK"
    #     db.check_call_status(call_id)
    #     # get data from "detected_speech" column
    #     detected = db.get_detected_speech(call_id)
    #     known = list(CallTranscript.neutral_call.split(" "))
    #     gwer += app.asr.get_wer(known, detected)
    #     divider += 1
    #     print(gwer / divider)


