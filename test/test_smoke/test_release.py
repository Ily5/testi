from model.call_transcript import Voice
from model.project import Project
import allure
import pytest
import time

pools_py = ["main_pool"]
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
                          "port": 5432}
                  }}


@allure.feature("Проверка работы cms")
def test_auth_cms(app, mdb):
    time.sleep(3)
    with allure.step("Переходим в проект Release_run"):
        app.page.go_to_project("Release_run")
        time.sleep(3)
    with allure.step("Проверяем наличие элементов на странице"):
        app.page.check_navigate_elements()


@allure.feature("Проверка рапознавания, синтеза")
@pytest.mark.parametrize("pools", pools_py, ids=[repr(x) for x in pools_py])
def test_edit_asr(app, pools, db, mdb):
    with allure.step("Задаём Pool"):
        app.page.go_to_project("Release_run")
        time.sleep(3)
        app.page.edit_pool(Project(pool=pools))
    with allure.step("Отправляем звонок на api"):
        time.sleep(3)
        resp = app.api.initiate_release_call(app.project, "test_asr_901", "yandex", "oksana@yandex")
        assert resp.status_code == 200
        call_id = app.asr.get_data(resp)
        app.page.check_navigate_elements()
        time.sleep(50)
        app.page.check_navigate_elements()
        time.sleep(50)
    with allure.step("Проверяем результаты распознование яндекс из rw базы"):
        db.create_connect(database["rw"][str(pools)])
        detected = db.get_detected_speech(call_id)
        detected= list(set(detected))
        print(detected)
        matches = ["тарифный", "план", "включайся"]
        assert any(x in detected for x in matches)
        # TODO: for cycle here
    with allure.step("Проверяем результаты синтеза яндекс из mongodb"):
        mongo_array = mdb.request({"main_id": int(call_id)})
        speak = mdb.parse(result=mongo_array, array="actions", key="speak", value="action_data")
        print(speak)
        assert speak == '"Hello"'
    with allure.step("Отправляем звонок на api"):
        resp = app.api.initiate_release_call(app.project, "test_asr_901", "google", "ru-RU-Wavenet-A@google")
        assert resp.status_code == 200
        call_id = app.asr.get_data(resp)
        app.page.check_navigate_elements()
        time.sleep(50)
        app.page.check_navigate_elements()
        time.sleep(50)
    with allure.step("Проверяем результаты распознование google из rw базы"):
        db.create_connect(database["rw"][str(pools)])
        detected = db.get_detected_speech(call_id)
        detected= list(set(detected))
        matches = ["тарифный", "план", "включайся"]
        assert any(x in detected for x in matches)
    with allure.step("Проверяем результаты синтеза google из mongodb"):
        mongo_array = mdb.request({"main_id": int(call_id)})
        speak = mdb.parse(result=mongo_array, array="actions", key="speak", value="action_data")
        assert speak == '"Hello"'

