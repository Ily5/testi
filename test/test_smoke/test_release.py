import allure
import pytest
import time

project = 214
# pools_py = ["test_pool", "main_pool"]
pools_py = ["test_pool"]
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
        db.create_connect(database["cms"])
        pool_id = [i[0] for i in (db.select_data('server_pools', 'name', 'id', pools))][0]
        db.change_project_data("pool_id", pool_id, app.project)

    with allure.step("Убираем звонки из queue api"):
        app.p_api.queue_clean(app.project)
    for asr, tts in speech_engine.items():
        with allure.step("Отправляем звонок на api"):
            resp = app.api.initiate_release_call(app.project, "test_asr_901", asr, tts)
            assert resp.status_code == 200
            call_id = app.asr.get_data(resp, "call_id")

        with allure.step("Проверяем результаты распознование %s из rw базы" % asr):
            db.create_connect(database["rw"][str(pools)])
            z = mdb.check_value({"main_id": call_id}, 'result', '+OK')
            detected = list(set(db.get_detected_speech_from_call_id(call_id)))
            matches = ["тарифный", "план", "линейки", "новой",  "тарифные", "планы", "при", "этом", "вас"]
            assert any(x in detected for x in matches)

        with allure.step("Проверяем результаты синтеза %s из mongodb" % asr):
            mongo_array = mdb.request({"main_id": call_id})
            speak = mdb.parse(result=mongo_array, array="actions", key="speak", value="action_data")
            assert speak == '"Hello"'
