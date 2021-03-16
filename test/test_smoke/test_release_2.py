# play_detect+тишина
# recognition_complete
# no_input timeout:
#
# 5000
#
# более 5000
#
# start_input_timeout (true)

# MRCP Кейс 2
# recognition_complete
#
# start_input_timeout (false)
#
# recognition_timeout (10000)
#
# Метод speak - послушать сколько длится и учесть разницу во времени (time-diff), не должен быть 0
#
# Должны покрываться следующие actions IVR (v2)
#
# recall
#
# if
#
# goto
#
# playback
#
# play_detect
#
# speak
#
# set
#
# say
#
# bridge
#
# before/after call unit


import allure
import pytest
import time

pools_py = ["test_pool", "main_pool"]


@allure.feature("Проверка работы cms")
def test_auth_cms(app):
    time.sleep(3)
    with allure.step("Переходим в проект Release_run"):
        app.page.go_to_project("Release_run")
        time.sleep(3)
    with allure.step("Проверяем наличие элементов на странице"):
        app.page.check_navigate_elements()
        app.cancel()


@allure.feature("Проверка рапознавания, синтеза")
@pytest.mark.parametrize("pools", pools_py, ids=[repr(x) for x in pools_py])
def test_edit_asr(app, pools, db, mdb):
    with allure.step("Задаём Pool"):
        db.create_connect(app.database["cms"])
        pool_id = [i[0] for i in (db.select_data('server_pools', 'name', 'id', pools))][0]
        db.change_project_data("pool_id", pool_id, app.project)
    with allure.step("Задаём logic unit"):
        db.change_project_data("start_unit", "Test_Unit", app.project)
    with allure.step("Убираем звонки из queue api"):
        app.p_api.queue_clean(app.project)
    for asr, tts in app.speech_engine.items():
        with allure.step("Отправляем звонок на api"):
            resp = app.api.initiate_release_call(app.project, "test_asr_901", asr, tts)
            assert resp.status_code == 200
            call_id = app.asr.get_data(resp, "call_id")

        with allure.step("Проверяем результаты распознование %s из rw базы" % asr):
            db.create_connect(app.database["rw"][str(pools)])
            z = mdb.check_value({"main_id": call_id}, 'result', '+OK')
            detected = list(set(db.get_detected_speech_from_call_id(call_id)))
            # detected = list(set(detected))
            matches = ["тарифный", "план", "линейки", "новой", "тарифные", "планы", "при", "этом", "вас", "любой", "тариф"]
            assert any(x in detected for x in matches)

        with allure.step("call_uuid"):
            print(db.select_data('calls', 'main_id', 'uuid', int(call_id)))

        with allure.step("Проверяем результаты синтеза %s из mongodb" % asr):
            mongo_array = mdb.request({"main_id": call_id})
            speak = mdb.parse(result=mongo_array, array="actions", key="speak", value="action_data")
            assert speak == '"Hello"'


@allure.feature("Проверка корректности работы распознавания для без входящего потока")
def test_silence(app, db, mdb):
    with allure.step("Задаём logic unit"):
        db.create_connect(app.database["cms"])
        db.change_project_data("start_unit", "test_unit_silence", app.project)
        # pool_id = [i[0] for i in (db.select_data('server_pools', 'name', 'id', pools))][0]
        # db.change_project_data("pool_id", pool_id, app.project)
    with allure.step("Убираем звонки из queue api"):
        app.p_api.queue_clean(app.project)
    with allure.step("Отправляем звонок на api"):
        resp = app.api.initiate_call(app.project, "test_asr_silence")
        assert resp.status_code == 200
        call_id = app.asr.get_data(resp, "call_id")
        db.create_connect(app.database["rw"]["main_pool"])
        z = mdb.check_value({"main_id": call_id}, 'result', '+OK')
    with allure.step("call_uuid"):
        print(db.select_data('calls', 'main_id', 'uuid', int(call_id)))
        # TODO в юнит базовый recall if goto set say bridge before/after call unit
        # метод переключения лоджик юнитов метод чека time diff из базы
        # MRCPv2 Кейс 1

        # play_detect + тишина
        # recognition_complete

        # no_input
        # timeout: 5000
        # более 5000
        # start_input_timeout(true)
        #
        # MRCP Кейс 2

        # recognition_complete
        # start_input_timeout(false)
        # recognition_timeout(10000)

