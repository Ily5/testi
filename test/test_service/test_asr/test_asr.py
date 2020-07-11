import time


def test_call(app, db):
    # initiate call with central api
    resp = app.api.initiate_call(63, "ss_12345_ss")
    assert resp.status_code == 200
    # check call status "+OK"
    while True:
        conn = db.db_conn("SELECT result FROM calls WHERE main_id = 3509364")
        if conn[0][0] == "+OK":
            break
        else:
            continue
    # get data from "detected_speech" column
    speech = list(db.db_conn("SELECT action_data FROM call_stats WHERE ACTION = 'detected_speech' "
                             "and uuid = '416e643c-c36e-11ea-a653-8b7d554f4005'")[0][0].split(" "))
    matches = ["сможет", "ответить", "интересующие", "обменяться", "договориться"]
    assert all(x in speech for x in matches)
