import time
from model.call_transcript import Numbers
import pytest
import json
import logging

# add filemode="w" to overwrite
logging.basicConfig(filename=r"C:\Users\iwear\PycharmProjects\demo\test_asr.log", level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

gwer = 0
divider = 0

with open(r"C:\Users\iwear\PycharmProjects\demo\data.json", encoding='utf-8') as json_file:
    call = json.load(json_file)
    call_py = []
    for i in range(len(call)):
        call_py.append(Numbers(number=call[i]["number"], transcript=call[i]["transcript"]))


# module_logger = logging.getLogger("test_app.test_asr")


@pytest.mark.parametrize("call", call_py, ids=[repr(x.number) for x in call_py])
def test_asr_call(app, db, call):
    global gwer
    global divider
    # logger = logging.getLogger("test_app.test_asr.add")
    # initiate call with central api
    resp = app.api.initiate_call(63, call.number)
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
    divider += 1
    logging.info("call count : %s " % divider)
    logging.info("stream error rate : %s " % (gwer / divider))
    print(gwer / divider)

# def test_file():
#     file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
#     with open(file, "w", encoding='utf8') as f:
#         json_file = json.dumps(call, default=lambda x: x.__dict__, ensure_ascii=False, indent=2).encode('utf8')
#         f.write(json_file.decode())
