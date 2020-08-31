import time
from model.call_transcript import Numbers
import pytest
import json
import logging
import os
import sys

# add filemode="w" to overwrite
logging.basicConfig(filename=sys.path[1] + "/log/test_asr.log", level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

gwer = 0
div = 0
ids = []
calls = []
mng_calls = {}

with open("data_test.json", encoding='utf-8') as json_file:
    call_test = json.load(json_file)
    call_py = []
    for i in range(len(call_test)):
        call_py.append(Numbers(number=call_test[i]["number"], transcript=call_test[i]["transcript"]))


@pytest.mark.parametrize("call", call_py, ids=[repr(x.number) for x in call_py])
def test_send_call(app, mdb, call):
    global ids
    global calls
    global mng_calls
    # logger = logging.getLogger("test_app.test_asr.add")
    # initiate call with central api
    resp = app.api.initiate_call(app.project, call.number)
    time.sleep(5)
    logging.info("api_response : %s " % (resp.json()))
    logging.info("number: %s   human_transcript : %s " % (call.number, call.transcript))
    assert resp.status_code == 200
    # get call_id from api response
    call_id = app.asr.get_data(resp)
    # wait migration call to stat base
    ids.append(call_id)
    calls.append(call.number)
    mng_calls = dict(zip(calls, ids))
    # check call status "+OK"
    # db.check_call_status(call_id)
    # get data from "detected_speech" column


def test_call(app, db, call):
    global gwer
    global div
    # logger = logging.getLogger("test_app.test_asr.add")
    # initiate call with central api
    resp = app.api.initiate_call(app.project, call.number)
    logging.info("api_response : %s " % (resp.json()))
    logging.info("number: %s   human_transcript : %s " % (call.number, call.transcript))
    assert resp.status_code == 200
    # get call_id from api response
    call_id = app.asr.get_data(resp)
    # wait migration call to r/w base
    time.sleep(45)
    # check call status "+OK"
    db.check_call_status(call_id)
    # get data from "detected_speech" column
    detected = db.get_detected_speech(call_id)
    logging.info("detected speech  %s" % detected)
    known = list(call.transcript.split(" "))
    gwer += app.asr.get_wer(known, detected)
    div += 1
    logging.info("call count : %s " % div)
    logging.info("stream error rate : %s " % (gwer / div))



# @pytest.mark.parametrize("call", call_py, ids=[repr(x.number) for x in call_py])
# def test_call(app, mdb, call):
#     global gwer
#     global div
#     global mng_calls
#     mongo_array = mdb.request({"main_id": mng_calls[call.number]})
#     while True:
#         if mongo_array is not None:
#             break
#         else:
#             mongo_array = mdb.request({"main_id": mng_calls[call.number]})
#             time.sleep(2)
#             continue
#     detected = mdb.parse(result=mongo_array, array="actions", key="detected_speech", value="action_data")
#     logging.info("detected speech  %s" % detected)
#     detected = list(detected.split(" "))
#     known = list(call.transcript.split(" "))
#     gwer += app.asr.get_wer(known, detected)
#     div += 1
#     logging.info("call count : %s " % div)
#     logging.info("stream error rate : %s " % (gwer / div))