import time


def test_call(app, db):
    # initiate call with central api
    resp = app.api.initiate_call(app.project, "test_asr_10")
    assert resp.status_code == 200
    # get call_id from api response
    call_id = app.asr.get_data(resp)
    # wait migration call to r/w base
    time.sleep(35)
    # check call status "+OK"
    while True:
        conn = db.db_conn("SELECT result FROM calls WHERE main_id = %s" % str(call_id))
        if conn[0][0] == "+OK":
            break
        else:
            continue
    # get data from "detected_speech" column
    speech = list(db.db_conn("SELECT action_data FROM call_stats WHERE ACTION = 'detected_speech' and uuid = '"
                             + str(db.db_conn("SELECT uuid FROM calls WHERE main_id = %s" % str(call_id))[0][0])
                             + "'")[0][0].split(" "))
    # matches = ["сможет", "ответить", "интересующие", "обменяться", "договориться"]
    matches = ["конечно", "буквально", "подключила", "тариф", "поменяла"]
    assert any(x in speech for x in matches)
