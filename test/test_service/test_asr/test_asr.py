import time


gwer = 0
div=0


def test_bad_call(app, db):
    global div
    global gwer
    knowns = []
    detect = []
    val = 0
    # initiate call with central api
    resp = app.api.initiate_call(63, "bad_call")
    assert resp.status_code == 200
    # get call_id from api response
    call_id = app.asr.get_data(resp)
    # wait migration call to r/w base
    time.sleep(45)
    # check call status "+OK"
    while True:
        conn = db.db_conn("SELECT result FROM calls WHERE main_id = %s" % str(call_id))
        if conn[0][0] == "+OK":
            break
        else:
            continue
    # get data from "detected_speech" column
    detected = list(db.db_conn("SELECT action_data FROM call_stats WHERE ACTION = 'detected_speech' and uuid = '"
                               + str(db.db_conn("SELECT uuid FROM calls WHERE main_id = %s" % str(call_id))[0][0])
                               + "'")[0][0].split(" "))
    known = list("але ну да что вы хотите да да да что вы хотите але не знаю у меня еще один есть я звоню другим"
                 "не знаю даже как вот ну с меня потом выдирать".split(" "))
    extend = len(known)
    match = [s for s in detected if s in known]
    detected = list(set(detected) - set(match))
    known = list(set(known) - set(match))
    for t in known:
        strt = t[:-1]
        if len(strt) >= 2:
            knowns.append(strt)
        else:
            val += 1
    for y in detected:
        strt = y[:-1]
        if len(strt) >= 2:
            detect.append(strt)
        else:
            val += 1
    matchs = [s for s in detect if s in knowns]
    detect = list(set(detect) - set(matchs))
    knowns = list(set(knowns) - set(matchs))
    wer = (val + len(detect) + len(knowns)) / extend
    print(wer)
    print(knowns)
    gwer += wer
    divider +=1


def test_good_call(app, db):
    global div
    global gwer
    knowns = []
    detect = []
    val = 0
    # initiate call with central api
    resp = app.api.initiate_call(63, "good_call")
    assert resp.status_code == 200
    # get call_id from api response
    call_id = app.asr.get_data(resp)
    # wait migration call to r/w base
    time.sleep(45)
    # check call status "+OK"
    while True:
        conn = db.db_conn("SELECT result FROM calls WHERE main_id = %s" % str(call_id))
        if conn[0][0] == "+OK":
            break
        else:
            continue
    # get data from "detected_speech" column
    detected = list(db.db_conn("SELECT action_data FROM call_stats WHERE ACTION = 'detected_speech' and uuid = '"
                               + str(db.db_conn("SELECT uuid FROM calls WHERE main_id = %s" % str(call_id))[0][0])
                               + "'")[0][0].split(" "))
    known = list("да здравствуйте мария ну давайте пару минут можно нет ну в настоящий момент десять "
                 "ну как бы больше никаких у меня трений не было все хорошо я что-то не поняла просто мне все "
                 "понравилось наоборот все хорошо ".split(" "))
    extend = len(known)
    match = [s for s in detected if s in known]
    detected = list(set(detected) - set(match))
    known = list(set(known) - set(match))
    for t in known:
        strt = t[:-1]
        if len(strt) >= 2:
            knowns.append(strt)
        else:
            val += 1
    for y in detected:
        strt = y[:-1]
        if len(strt) >= 2:
            detect.append(strt)
        else:
            val += 1
    matchs = [s for s in detect if s in knowns]
    detect = list(set(detect) - set(matchs))
    knowns = list(set(knowns) - set(matchs))
    wer = (val + len(detect) + len(knowns)) / extend
    print(knowns)
    print(wer)
    gwer += wer
    divider += 1


def test_neutral_call(app, db):
    global div
    global gwer
    knowns = []
    detect = []
    val = 0
    # initiate call with central api
    resp = app.api.initiate_call(63, "neutral_call")
    assert resp.status_code == 200
    # get call_id from api response
    call_id = app.asr.get_data(resp)
    # wait migration call to r/w base
    time.sleep(45)
    # check call status "+OK"
    while True:
        conn = db.db_conn("SELECT result FROM calls WHERE main_id = %s" % str(call_id))
        if conn[0][0] == "+OK":
            break
        else:
            continue
    # get data from "detected_speech" column
    detected = list(db.db_conn("SELECT action_data FROM call_stats WHERE ACTION = 'detected_speech' and uuid = '"
                               + str(db.db_conn("SELECT uuid FROM calls WHERE main_id = %s" % str(call_id))[0][0])
                               + "'")[0][0].split(" "))
    known = list("ало да давайте попробуем понятия не имею если честно давайте на пятёрке "
                 "остановимся будет везде средний результат ставить а я говорю давайте пять поставим "
                 "потому что я не вижу смысла повторять этот вопрос".split(" "))
    extend = len(known)
    match = [s for s in detected if s in known]
    detected = list(set(detected) - set(match))
    known = list(set(known) - set(match))
    for t in known:
        strt = t[:-1]
        if len(strt) >= 2:
            knowns.append(strt)
        else:
            val += 1
    for y in detected:
        strt = y[:-1]
        if len(strt) >= 2:
            detect.append(strt)
        else:
            val += 1
    matchs = [s for s in detect if s in knowns]
    detect = list(set(detect) - set(matchs))
    knowns = list(set(knowns) - set(matchs))
    wer = (val + len(detect) + len(knowns)) / extend
    gwer += wer
    divider += 1
    print(knowns)
    print(gwer/divider)
 # необходимо тестировать вынести скрипт в хелпер , вызывать его тут, возвращать wer gwer тоже суммировать простой функцией