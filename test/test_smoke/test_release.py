from fixture.asr import AsrHelper
from fixture.api import ApiHelper, PoolApiHelper
import allure
import pytest
import time

project = 214
pools_py = ["test_pool", "main_pool"]
database = {"rw":
                {"test_pool": {"database": "test_pool_pbx",
                               "user": "postgres",
                               "password": "",
                               "host": "10.129.0.33",
                               "port": 5432},
                 "main_pool": {"database": "pbx_main_pool",
                               "user": "postgres",
                               "password": "",
                               "host": "10.129.0.26",
                               "port": 5432
                               }
                 },
            "cms":
                {"database": "pbx",
                    "user": "postgres",
                    "password": "",
                    "host": "10.129.0.7",
                    "port": 5432
                 }
            }
speech_engine = {"yandex": "oksana@yandex", "google": "ru-RU-Wavenet-A@google"}


# speech_engine = {"yandex": "oksana@yandex"}


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
        # app.page.edit_pool(Project(pool=pools)
        db.create_connect(database["cms"])
        pool_id = [i[0] for i in (db.select_data('server_pools', 'name', 'id', pools))][0]
        # print("pool_id is %s" % pool_id)
        db.change_project_data("pool_id", pool_id, app.project)
        # db.change_pool_id(2,app.project)
        # print(db.select_data('projects', 'id', 'pool_id', app.project))

    with allure.step("Убираем звонки из queue api"):
        app.p_api.queue_clean(app.project)   # papi
    for asr, tts in speech_engine.items():
        with allure.step("Отправляем звонок на api"):
            resp = app.api.initiate_release_call(app.project, "test_asr_901", asr, tts) # api
            assert resp.status_code == 200
            call_id = app.asr.get_data(resp, "call_id")  # asr

        with allure.step("Проверяем результаты распознование %s из rw базы" % asr):
            db.create_connect(database["rw"][str(pools)])
            z = mdb.check_value({"main_id": call_id}, 'result', '+OK')
            detected = list(set(db.get_detected_speech_from_call_id(call_id)))
            # detected = list(set(detected))
            matches = ["тарифный", "план", "линейки", "новой",  "тарифные", "планы", "при", "этом", "вас"]
            assert any(x in detected for x in matches)

        with allure.step("Проверяем результаты синтеза %s из mongodb" % asr):
            mongo_array = mdb.request({"main_id": call_id})
            speak = mdb.parse(result=mongo_array, array="actions", key="speak", value="action_data")
            print(speak)
            assert speak == '"Hello"'
