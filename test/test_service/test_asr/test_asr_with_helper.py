import time
from model.call_transcript import CallTranscript
gwer = 0
div = 0


def test_bad_call(app, db):
    global gwer
    global div
    # initiate call with central api
    resp = app.api.initiate_call(63, "bad_call")
    assert resp.status_code == 200
    # get call_id from api response
    call_id = app.asr.get_data(resp)
    # wait migration call to r/w base
    time.sleep(45)
    # check call status "+OK"
    db.check_call_status(call_id)
    # get data from "detected_speech" column
    detected = db.get_detected_speech(call_id)
    known = list(CallTranscript.bad_call.split(" "))
    gwer += app.asr.get_wer(known, detected)
    divider += 1


def test_good_call(app, db):
    global gwer
    global div
    # initiate call with central api
    resp = app.api.initiate_call(63, "good_call")
    assert resp.status_code == 200
    # get call_id from api response
    call_id = app.asr.get_data(resp)
    # wait migration call to r/w base
    time.sleep(45)
    # check call status "+OK"
    db.check_call_status(call_id)
    # get data from "detected_speech" column
    detected = db.get_detected_speech(call_id)
    known = list(CallTranscript.good_call.split(" "))
    gwer += app.asr.get_wer(known, detected)
    divider += 1


def test_neutral_call(app, db):
    global gwer
    global div
    # initiate call with central api
    resp = app.api.initiate_call(63, "neutral_call")
    assert resp.status_code == 200
    # get call_id from api response
    call_id = app.asr.get_data(resp)
    # wait migration call to r/w base
    time.sleep(45)
    # check call status "+OK"
    db.check_call_status(call_id)
    # get data from "detected_speech" column
    detected = db.get_detected_speech(call_id)
    known = list(CallTranscript.neutral_call.split(" "))
    gwer += app.asr.get_wer(known, detected)
    divider += 1
    print(gwer/divider)
 # необходимо тестировать вынести скрипт в хелпер , вызывать его тут, возвращать wer gwer тоже суммировать простой функцией


def test_asr(app, db):
    global gwer
    global div
    # initiate call with central api
    resp = app.api.initiate_call(63, "neutral_call")
    assert resp.status_code == 200
    # get call_id from api response
    call_id = app.asr.get_data(resp)
    # wait migration call to r/w base
    time.sleep(45)
    # check call status "+OK"
    db.check_call_status(call_id)
    # get data from "detected_speech" column
    detected = db.get_detected_speech(call_id)
    known = list(CallTranscript.neutral_call.split(" "))
    gwer += app.asr.get_wer(known, detected)
    divider += 1
    print(gwer / divider)