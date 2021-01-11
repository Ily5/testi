# делаем auth cms 3.0
import time

import pytest
import allure
#
# database = {"rw":
#                 {"test": {"database": "pbx_refactor",
#                           "user": "postgres",
#                           "password": "",
#                           "host": "10.131.0.116",
#                           "port": 5001},
#                  "prod": {"database": "pbx_main_pool",
#                           "user": "postgres",
#                           "password": "",
#                           "host": "10.129.0.26",
#                           "port": 5432
#                           }
#                  },
#             "ro":
#                 {"test": {"database": "pbx_refactor",
#                           "user": "postgres",
#                           "password": "",
#                           "host": "10.131.0.116",
#                           "port": 5000},
#                  "prod": {"database": "pbx_main_pool",
#                           "user": "postgres",
#                           "password": "",
#                           "host": "10.129.0.26",
#                           "port": 5432
#                           }
#                  },
#             }
#
#
# @allure.feature("Проверка 3.0 yandex")
# def test_v3(app_3, db):
#     with allure.step("логин в cms v3"):
#         app_3.session.login()
#     with allure.step("Проверка доступности cms"):
#         time.sleep(3)
#         app_3.page.go_to_project("b5b2a743-259b-4641-a007-0dd2abe3e0fa")
#         time.sleep(5)
#         app_3.page.check_menu()
#         app_3.session.logout()
#     db.create_connect(database["rw"]["test"])
#     with allure.step("Авторизация в external_api"):
#         token = app_3.api.auth()
#     with allure.step("Изменение параметров в cms_api"):
#         app_3.api.set_yandex(token)
#     with allure.step("Иницализация диалога в external_api"):
#         dialog_uuid = app_3.api.init_dialog(token, 55555)
#     db.wait_for_done(dialog_uuid)
#     with allure.step("Выгрузка данных по диалогу из rw базы"):
#         dialog_id = db.select_data(table='dialog', column='uuid', sdata='id', data=str(dialog_uuid))[0][0]
#     result = db.execute_call_data(table='dialog_stats', data=dialog_id)


# бридж +
# реког в тишину + реког в тишину + рек в запись + рек в тишину - сдлеать общий лоджик юнит и добавить екст для фс
# задекомпозировать отчёт
#  выбросить call_uuid + project_uuid
# всё выбросить в ci завтра в адекватное время
# начать задачи с мрсп медиа пятн / четв

def test_test(app_3):
    print(app_3.api.auth())
    print(app_3.api.auth())
    print(app_3.api.auth())