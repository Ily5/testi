import allure
import pytest
import time

project = 214
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
speech_engine = {"yandex": "oksana@yandex"}


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
    # with allure.step("Задаём logic unit"):
    #     db.change_project_data("start_unit", "Test_Unit", app.project)
    with allure.step("Убираем звонки из queue api"):
        app.p_api.queue_clean(app.project)
    for asr, tts in speech_engine.items():
        with allure.step("Отправляем звонок на api"):
            resp = app.api.initiate_release_call(app.project, "test_asr_silence", asr, tts)
            assert resp.status_code == 200
            call_id = app.asr.get_data(resp, "call_id")

        with allure.step("Проверяем результаты распознование %s из rw базы" % asr):
            db.create_connect(database["rw"][str(pools)])
            z = mdb.check_value({"main_id": call_id}, 'result', '+OK')
            detected = list(set(db.get_detected_speech_from_call_id(call_id)))
            # detected = list(set(detected))
            matches = ["тарифный", "план", "линейки", "новой", "тарифные", "планы", "при", "этом", "вас"]
            assert any(x in detected for x in matches)

        with allure.step("Проверяем результаты синтеза %s из mongodb" % asr):
            mongo_array = mdb.request({"main_id": call_id})
            speak = mdb.parse(result=mongo_array, array="actions", key="speak", value="action_data")
            assert speak == '"Hello"'
#
#
# @allure.feature("Проверка корректности работы распознавания для без входящего потока")
# def test_silence(app, db, mdb):
#     with allure.step("Задаём logic unit"):
#         db.create_connect(database["cms"])
#         db.change_project_data("start_unit", "Test_Unit", app.project)
#         # pool_id = [i[0] for i in (db.select_data('server_pools', 'name', 'id', pools))][0]
#         # db.change_project_data("pool_id", pool_id, app.project)
#     with allure.step("Убираем звонки из queue api"):
#         app.p_api.queue_clean(app.project)
#     with allure.step("Отправляем звонок на api"):
#         resp = app.api.initiate_call(app.project, "test_asr_901")
#         assert resp.status_code == 200
#         call_id = app.asr.get_data(resp, "call_id")
# ну сделать звонок в котором ансвер и всё проверить что выходит
# если норм сделать ещё два лоджик юнита