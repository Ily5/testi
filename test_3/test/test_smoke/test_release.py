# делаем auth cms 3.0
#

import pytest
import allure
database = {"rw":
                {"test": {"database": "pbx_refactor",
                               "user": "postgres",
                               "password": "",
                               "host": "10.131.0.116",
                               "port": 5001},
                 "prod": {"database": "pbx_main_pool",
                               "user": "postgres",
                               "password": "",
                               "host": "10.129.0.26",
                               "port": 5432
                               }
                 },
            "ro":
                {"test": {"database": "pbx_refactor",
                               "user": "postgres",
                               "password": "",
                               "host": "10.131.0.116",
                               "port": 5000},
                 "prod": {"database": "pbx_main_pool",
                               "user": "postgres",
                               "password": "",
                               "host": "10.129.0.26",
                               "port": 5432
                               }
                 },
            }


@allure.feature("Проверка 3.0 yandex")
def test_v3(app_3, db):
    with allure.step("логин в cms v3"):
        app_3.session.login()
    with allure.step("Проверка доступности cms"):
        app_3.page.go_to_project("b5b2a743-259b-4641-a007-0dd2abe3e0fa")
        app_3.page.check_menu()
        app_3.session.logout()
    db.create_connect(database["rw"]["test"])
    with allure.step("Авторизация в external_api"):
        token = app_3.api.auth()
    with allure.step("Изменение параметров в cms_api"):
        app_3.api.set_yandex(token)
    with allure.step("Иницализация диалога в external_api"):
        dialog_uuid = app_3.api.init_dialog(token, 55555)
    db.wait_for_done(dialog_uuid)
    with allure.step("Выгрузка данных по диалогу из rw базы"):
        dialog_id = db.select_data(table='dialog', column='uuid', sdata='id', data=str(dialog_uuid))[0][0]
    result = db.execute_call_data(table='dialog_stats', data=dialog_id)
    for i in result:
        for j in i:
            matches = ['Распознавание', 'Пока', 'Сейчас', 'Простой', 'следующий', 'синтезированный', 'ага']
            if 'nv.say' in j:
                with allure.step("проверка метода nv.say"):
                    assert 'hello' in i[i.index(j) + 1]
            elif 'main_logic' in j:
                with allure.step("проверка отсутствия ошибок в звонке"):
                    assert 'Error' not in i[i.index(j) + 1]
            elif 'nv.listen' in j and 'utterance' in i[i.index(j) + 1]:
                if 'null' not in i[i.index(j) + 1]:
                    with allure.step("проверка наличия результатов распознавания"):
                        assert any(x in i[i.index(j) + 1] for x in matches)
            elif 'nv.synthesize' in j:
                with allure.step("проверка метода nv.say"):
                    assert any(x in i[i.index(j) + 1] for x in matches)
            elif 'nv.play_random_sound' in j:
                with allure.step("проверка метода nv.play_random_sound"):
                    assert any(x in i[i.index(j) + 1] for x in matches)
            elif 'nv.background' in j:
                with allure.step("проверка метода nv.background"):
                    assert 'Office_local' in i[i.index(j) + 1]

    with allure.step("логин в cms v3"):
        app_3.session.login()
    with allure.step("Проверка доступности cms"):
        app_3.page.go_to_project("b5b2a743-259b-4641-a007-0dd2abe3e0fa")
        app_3.page.check_menu()
        app_3.session.logout()
    db.create_connect(database["rw"]["test"])
    # with allure.step("Авторизация в external_api"):
    #     token = app_3.api.auth()
    with allure.step("Изменение параметров в cms_api"):
        app_3.api.set_google(token)
    with allure.step("Иницализация диалога в external_api"):
        dialog_uuid = app_3.api.init_dialog(token, 55555)
    db.wait_for_done(dialog_uuid)
    with allure.step("Выгрузка данных по диалогу из rw базы"):
        dialog_id = db.select_data(table='dialog', column='uuid', sdata='id', data=str(dialog_uuid))[0][0]
    result = db.execute_call_data(table='dialog_stats', data=dialog_id)
    for i in result:
        for j in i:
            matches = ['Распознавание', 'Пока', 'Сейчас', 'Простой', 'следующий', 'синтезированный', 'ага']
            if 'nv.say' in j:
                with allure.step("проверка метода nv.say"):
                    assert 'hello' in i[i.index(j) + 1]
            elif 'main_logic' in j:
                with allure.step("проверка отсутствия ошибок в звонке"):
                    assert 'Error' not in i[i.index(j) + 1]
            elif 'nv.listen' in j and 'utterance' in i[i.index(j) + 1]:
                if 'null' not in i[i.index(j) + 1]:
                    with allure.step("проверка наличия результатов распознавания"):
                        assert any(x in i[i.index(j) + 1] for x in matches)
            elif 'nv.synthesize' in j:
                with allure.step("проверка метода nv.say"):
                    assert any(x in i[i.index(j) + 1] for x in matches)
            elif 'nv.play_random_sound' in j:
                with allure.step("проверка метода nv.play_random_sound"):
                    assert any(x in i[i.index(j) + 1] for x in matches)
            elif 'nv.background' in j:
                with allure.step("проверка метода nv.background"):
                    assert 'Office_local' in i[i.index(j) + 1]



