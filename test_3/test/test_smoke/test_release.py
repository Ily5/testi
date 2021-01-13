# делаем auth cms 3.0
import time

import pytest
import allure

result = []


# @allure.feature("Smoke 3.0")
# @allure.story("Работа cms")
# def test_v3_cms(app_3, db):
#     # token = app_3.api.auth()
#     with allure.step("логин в cms v3"):
#         app_3.session.login()
#     with allure.step("Переходим в проект release_run"):
#         time.sleep(3)
#         # app_3.page.go_to_project("b5b2a743-259b-4641-a007-0dd2abe3e0fa")
#         app_3.page.go_to_project("f29c639f-f3ff-46bb-9425-fe2ffb27796c")
#         time.sleep(5)
#     with allure.step("Наличие элементов меню"):
#         app_3.page.check_menu()
#         app_3.session.logout()


# @allure.feature("Smoke 3.0")
# @allure.story("Yandex")
# def test_v3_init_call_yandex(app_3, db):
#     global result
#     db.create_connect(app_3.database["rw"]["prod"])
#     with allure.step("Авторизация в external_api"):
#         token = app_3.api.auth()
#         assert type(token) == str
#     with allure.step("Изменение параметров в cms_api"):
#         app_3.api.set_yandex(token)
#     with allure.step("Иницализация диалога в external_api"):
#         dialog_uuid = app_3.api.init_dialog(token, 55555)
#     db.wait_for_done(dialog_uuid)
#     with allure.step("Выгрузка данных по диалогу из rw базы"):
#         dialog_id = db.select_data(table='dialog', column='uuid', sdata='id', data=str(dialog_uuid))[0][0]
#         print('dialog id - ', dialog_id)
#     print('call uuid - ', db.select_data(table='call', column='dialog_id', sdata='uuid', data=int(dialog_id)))
#     result = db.execute_call_data(table='dialog_stats', data=dialog_id)

@allure.feature("Smoke 3.0")
@allure.story("Yandex")
def test_test(app_3, db):
    global result
    db.create_connect(app_3.database["rw"]["prod"])
    result = db.execute_call_data(table='dialog_stats', data='474679')
    # print('\n', result)
    # listen_list = [res[1].split(',') for res in result if 'nv.listen' in res]
    # utterance_listen_list = [i[i.find(':') + 2:] for res in listen_list for i in res if
    #                          'utterance' in i]
    #
    # # print('\n', utterance_listen_list)
    # log_list = [res[1] for res in result if 'nn.log' in res]
    # extract_person = None
    # extract_address = None
    # dict_log = {}
    # for item in [res[1] for res in result if 'nn.log' in res]:
    #     if 'city' in item:
    #         dict_log['extract_address'] = item
    #     if 'first' in item:
    #         dict_log['extract_person'] = item
    #     if 'bot' in item:
    #         dict_log['call_transcription'] = item
    #     if len(item) <= 4:
    #         dict_log['call_duration'] = item
    # # print(dict_log)
    # tut = 'FdfsDD dfgdfg DFFFGF'
    # for item in [res[1] for res in result if 'nn.dump' in res]:
    #     print(item.lower())
    #     assert 'error' not in item.lower()


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
def test_v3_media_part_yandex(app_3, db):
    global result
    with allure.step("nv_say"):
        for res in result:
            if 'nv.say' in res:
                assert any('hello' in d for d in res)
        if not any('nv.say' in d for d in result):
            assert False
    with allure.step("nv_background"):
        # ____ nv background
        for res in result:
            if 'nv.background' in res:
                assert any('Office_sound' in d for d in res)
        if not any('nv.background' in d for d in result):
            assert False
    # ____ nv play random sound
    with allure.step("nv.play_random_sound"):
        for res in result:
            if 'nv.play_random_sound' in res:
                assert any('ага' or 'min_delay' in d for d in res)
        if not any('nv.play_random_sound' in d for d in result):
            assert False
    # nv synth
    with allure.step("nv_synth"):
        count = 0
        for res in result:
            if 'nv.synthesize' in res:
                count += 1
                assert len(res[1]) > 20
        assert count == 12
        if not any('nv.synthesize' in d for d in result):
            assert False
    with allure.step("nv_listen и перебивание"):
        # nv listen / перебивание
        for res in result:
            if 'nv.listen' in res:
                for r in res:
                    if "распознавание" in r:
                        assert "распознавание" or "пока" in r
                    elif "перебивание" in r:
                        assert "перебивание" in r
        if not any('nv.listen' in d for d in result):
            assert False
    with allure.step("nv_bridge"):
        # ____ nv bridge
        for res in result:
            if 'nv.bridge' in res:
                assert '555555' in res[1]
        if not any('nv.bridge' in d for d in result):
            assert False

    synth_phrase_list = [res[1][res[1].find(':') + 4: res[1].find(',') - 1] for res in result if 'nv.synthesize' in res]

    with allure.step("nn.env"):
        assert 'Вытащили переменную окружения' in synth_phrase_list

    with allure.step('nn.storage'):
        assert 'Хранилище работает' in synth_phrase_list

    with allure.step('nn.counter'):
        assert 'Счетчик работает' in synth_phrase_list

    with allure.step('nn.has_record - valid'):
        assert 'Проверка наличия записи работает' in synth_phrase_list

    with allure.step('nn.has_record - no valid'):
        assert 'Проверка наличия записи работает некорректно' not in synth_phrase_list

    with allure.step('nn.has_records - valid'):
        assert 'Работает наличия записей проверка' in synth_phrase_list

    with allure.step('nn.has_records - no valid'):
        assert 'Проверка наличия записей работает некорректно' not in synth_phrase_list

    logs_dict = {}
    for item in [res[1] for res in result if 'nn.log' in res]:
        if 'city' in item:
            logs_dict['extract_address'] = item
        if 'first' in item:
            logs_dict['extract_person'] = item
        if 'bot' in item:
            logs_dict['call_transcription'] = item
        if len(item) <= 4:
            logs_dict['call_duration'] = item
        if 'no_input_timeout' in item:
            logs_dict['get_default'] = item

    with allure.step('nlu.extract_person'):
        assert logs_dict['extract_person'] == "{'first': 'иван', 'last': 'петров', 'middle': 'алексеевич'}"

    # with allure.step('nlu.extract_address'):
    #     assert logs_dict['extract_address'] == "{'city': ['москва', None], 'street': ['ленина', 'улица']," \
    #                                            " 'building': ['16', None, None], 'appartment': '5'}"

    with allure.step('nv.listen - тишина'):
        listen_list = [res[1].split(',') for res in result if 'nv.listen' in res]
        utterance_listen_list = [i[i.find(':') + 2:] for res in listen_list for i in res if
                                 'utterance' in i]
        assert 'null' in utterance_listen_list
        for item in [res[1] for res in result if 'nn.dump' in res]:
            assert 'error' not in item.lower()

    with allure.step('get_call_transcription'):
        for synth in synth_phrase_list:
            assert synth in logs_dict['call_transcription']

    with allure.step('get_call_duration'):
        assert len(logs_dict['call_duration']) > 0
        assert int(logs_dict['call_duration']) > 0

    with allure.step('get_default'):
        assert logs_dict['get_default'] == "{'no_input_timeout': 5000, 'recognition_timeout': 30000," \
                                           " 'speech_complete_timeout': 5000, 'asr_complete_timeout': 5000}"


@allure.feature("Smoke 3.0")
# @allure.story("Проверка медиа части Yandex")
@allure.title('Проверка построения отчета')
def test_test_01():
    print('Смотрим как постоился отчет')


# @allure.feature("Smoke 3.0")
# @allure.story("Google")
# def test_v3_init_call_google(app_3, db):
#     global result
#     db.create_connect(app_3.database["rw"]["prod"])
#     with allure.step("Авторизация в external_api"):
#         token = app_3.api.auth()
#         assert type(token) == str
#     with allure.step("Изменение параметров в cms_api"):
#         app_3.api.set_google(token)
#         # print("inside google token" + token)
#     with allure.step("Иницализация диалога в external_api"):
#         dialog_uuid = app_3.api.init_dialog(token, 55555)
#     db.wait_for_done(dialog_uuid)
#     with allure.step("Выгрузка данных по диалогу из rw базы"):
#         dialog_id = db.select_data(table='dialog', column='uuid', sdata='id', data=str(dialog_uuid))[0][0]
#     result = db.execute_call_data(table='dialog_stats', data=dialog_id)
#     print(db.select_data(table='call', column='dialog_id', sdata='uuid', data=int(dialog_id)))


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Google")
def test_v3_media_part_google(app_3, db):
    global result
    with allure.step("nv_say"):
        for res in result:
            print(res)
            if 'nv.say' in res:
                assert any('hello' in d for d in res)
        if not any('nv.say' in d for d in result):
            assert False
    with allure.step("nv_background"):
        # ____ nv background
        for res in result:
            if 'nv.background' in res:
                assert any('Office_sound' in d for d in res)
        if not any('nv.background' in d for d in result):
            assert False
    # ____ nv play random sound
    with allure.step("nv.play_random_sound"):
        for res in result:
            if 'nv.play_random_sound' in res:
                assert any('ага' or 'min_delay' in d for d in res)
        if not any('nv.play_random_sound' in d for d in result):
            assert False
    # nv synth
    with allure.step("nv_synth"):
        count = 0
        for res in result:
            if 'nv.synthesize' in res:
                count += 1
                assert len(res[1]) > 20
        assert count == 12
        if not any('nv.synthesize' in d for d in result):
            assert False
    with allure.step("nv_listen и перебивание"):
        # nv listen / перебивание
        for res in result:
            if 'nv.listen' in res:
                for r in res:
                    if "распознавание" in r:
                        assert "распознавание" or "пока" in r
                    elif "перебивание" in r:
                        assert "перебивание" or "часть" or "смотреть" in r
        if not any('nv.listen' in d for d in result):
            assert False
    with allure.step("nv_bridge"):
        # ____ nv bridge
        for res in result:
            if 'nv.bridge' in res:
                assert '555555' in res[1]
        if not any('nv.bridge' in d for d in result):
            assert False

    synth_phrase_list = [res[1][res[1].find(':') + 4: res[1].find(',') - 1] for res in result if 'nv.synthesize' in res]

    with allure.step("nn.env"):
        assert 'Вытащили переменную окружения' in synth_phrase_list

    with allure.step('nn.storage'):
        assert 'Хранилище работает' in synth_phrase_list

    with allure.step('nn.counter'):
        assert 'Счетчик работает' in synth_phrase_list

    with allure.step('nn.has_record - valid'):
        assert 'Проверка наличия записи работает' in synth_phrase_list

    with allure.step('nn.has_record - no valid'):
        assert 'Проверка наличия записи работает некорректно' not in synth_phrase_list

    with allure.step('nn.has_records - valid'):
        assert 'Работает наличия записей проверка' in synth_phrase_list

    with allure.step('nn.has_records - no valid'):
        assert 'Проверка наличия записей работает некорректно' not in synth_phrase_list

    logs_dict = {}
    for item in [res[1] for res in result if 'nn.log' in res]:
        if 'city' in item:
            logs_dict['extract_address'] = item
        if 'first' in item:
            logs_dict['extract_person'] = item
        if 'bot' in item:
            logs_dict['call_transcription'] = item
        if len(item) <= 4:
            logs_dict['call_duration'] = item
        if 'no_input_timeout' in item:
            logs_dict['get_default'] = item

    with allure.step('nlu.extract_person'):
        assert logs_dict['extract_person'] == "{'first': 'иван', 'last': 'петров', 'middle': 'алексеевич'}"

    # with allure.step('nlu.extract_address'):
    #     assert logs_dict['extract_address'] == "{'city': ['москва', None], 'street': ['ленина', 'улица']," \
    #                                            " 'building': ['16', None, None], 'appartment': '5'}"

    with allure.step('nv.listen - тишина'):
        listen_list = [res[1].split(',') for res in result if 'nv.listen' in res]
        utterance_listen_list = [i[i.find(':') + 2:] for res in listen_list for i in res if
                                 'utterance' in i]
        assert 'null' in utterance_listen_list
        for item in [res[1] for res in result if 'nn.dump' in res]:
            assert 'error' not in item.lower()

    with allure.step('get_call_transcription'):
        for synth in synth_phrase_list:
            assert synth in logs_dict['call_transcription']

    with allure.step('get_call_duration'):
        assert len(logs_dict['call_duration']) > 0
        assert int(logs_dict['call_duration']) > 0

    with allure.step('get_default'):
        assert logs_dict['get_default'] == "{'no_input_timeout': 5000, 'recognition_timeout': 30000," \
                                           " 'speech_complete_timeout': 5000, 'asr_complete_timeout': 5000}"

#
# @allure.feature("Silence")
# @allure.story("Тишина + тишина")
# def test_v3_silence(app_3, db):
#     db.create_connect(app_3.database["rw"]["prod"])
#     # with allure.step("Авторизация в external_api"):
#     #     token = app_3.api.auth()
#     with allure.step("Изменение параметров в cms_api"):
#         # app_3.api.set_yandex(token)
#         token = app_3.api.auth()
#         assert type(token) == str
#     with allure.step("Иницализация диалога в external_api"):
#         dialog_uuid = app_3.api.init_dialog(token, 55555)
#     with allure.step("Звонок завершён успешно"):
#         db.wait_for_done(dialog_uuid)
#         dialog_id = db.select_data(table='dialog', column='uuid', sdata='id', data=str(dialog_uuid))[0][0]
#         result = db.execute_call_data(table='dialog_stats', data=dialog_id)
#         print(db.select_data(table='call', column='dialog_id', sdata='uuid', data=int(dialog_id)))


    # with allure.step("Изменение параметров в cms_api"):
    #     app_3.api.set_google(token)
    # with allure.step("Иницализация диалога в external_api"):
    #     dialog_uuid = app_3.api.init_dialog(token, 55555)
    # db.wait_for_done(dialog_uuid)
    # with allure.step("Выгрузка данных по диалогу из rw базы"):
    #     dialog_id = db.select_data(table='dialog', column='uuid', sdata='id', data=str(dialog_uuid))[0][0]
    # result = db.execute_call_data(table='dialog_stats', data=dialog_id)
    # for i in result:
    #     for j in i:
    #         matches = ['Распознавание', 'Пока', 'Сейчас', 'Простой', 'следующий', 'синтезированный', 'ага']
    #         if 'nv.say' in j:
    #             with allure.step("проверка метода nv.say"):
    #                 assert 'hello' in i[i.index(j) + 1]
    #         elif 'main_logic' in j:
    #             with allure.step("проверка отсутствия ошибок в звонке"):
    #                 assert 'Error' not in i[i.index(j) + 1]
    #         elif 'nv.listen' in j and 'utterance' in i[i.index(j) + 1]:
    #             # if 'null' not in i[i.index(j) + 1]:
    #             with allure.step("проверка наличия результатов распознавания"):
    #                 print(i[i.index(j) + 1])
    #                 # assert any(x in i[i.index(j) + 1] for x in matches)
    #         elif 'nv.synthesize' in j:
    #             with allure.step("проверка метода nv.synthesize"):
    #                 assert any(x in i[i.index(j) + 1] for x in matches)
    #         elif 'nv.play_random_sound' in j:
    #             with allure.step("проверка метода nv.play_random_sound"):
    #                 assert any(x in i[i.index(j) + 1] for x in matches)
    #         elif 'nv.background' in j:
    #             with allure.step("проверка метода nv.background"):
    #                 assert 'Office_local' in i[i.index(j) + 1]
    #
    # # ____ nv say
    # for res in result:
    #     if 'nv.say' in res:
    #         assert any('hello' in d for d in res)
    # if not any('nv.say' in d for d in result):
    #     assert False
    # # ____ nv background
    # for res in result:
    #     if 'nv.background' in res:
    #         assert any('Office_local' in d for d in res)
    # if not any('nv.background' in d for d in result):
    #     assert False
    # # ____ nv play random sound
    # for res in result:
    #     if 'nv.random_sound' in res:
    #         assert any('ага' or 'min_delay' in d for d in res)
    # if not any('nv.random_sound' in d for d in result):
    #     assert False
    # # nv synth
    # count = 0
    # for res in result:
    #     if 'nv.synthesize' in res:
    #         count += 1
    #         assert len(res[1]) > 20
    # assert count == 5
    # if not any('nv.synthesize' in d for d in result):
    #     assert False
    # # nv listen / перебивание
    # for res in result:
    #     if 'nv.listen' in res:
    #         for r in res:
    #             if "распознавание" in r:
    #                 assert "распознавание" or "пока" in r
    #             elif "перебивание" in r:
    #                 assert "перебивание" in r
    # if not any('nv.listen' in d for d in result):
    #     assert False
    # # ____ nv bridge
    # for res in result:
    #     if 'nv.bridge' in res:
    #         assert '555555' in res[1]
    # if not any('nv.bridge' in d for d in result):
    #     assert False

# def test_v3_2(app_3, db):
#     with allure.step("логин в cms v3"):
#         app_3.session.login()
#     with allure.step("Проверка доступности cms"):
#         app_3.page.go_to_project("b5b2a743-259b-4641-a007-0dd2abe3e0fa")
#         app_3.page.check_menu()
#         app_3.session.logout()
#     db.create_connect(database["rw"]["test"])
#     with allure.step("Авторизация в external_api"):
#         token = app_3.api.auth()
#     with allure.step("Изменение параметров в cms_api"):
#         app_3.api.set_google(token)
#     with allure.step("Иницализация диалога в external_api"):
#         dialog_uuid = app_3.api.init_dialog(token, 55555)
#     db.wait_for_done(dialog_uuid)
#     with allure.step("Выгрузка данных по диалогу из rw базы"):
#         dialog_id = db.select_data(table='dialog', column='uuid', sdata='id', data=str(dialog_uuid))[0][0]
#     result = db.execute_call_data(table='dialog_stats', data=dialog_id)
#     for i in result:
#         for j in i:
#             matches = ['Распознавание', 'Пока', 'Сейчас', 'Простой', 'следующий', 'синтезированный', 'ага']
#             if 'nv.say' in j:
#                 with allure.step("проверка метода nv.say"):
#                     assert 'hello' in i[i.index(j) + 1]
#             elif 'main_logic' in j:
#                 with allure.step("проверка отсутствия ошибок в звонке"):
#                     assert 'Error' not in i[i.index(j) + 1]
#             elif 'nv.listen' in j and 'utterance' in i[i.index(j) + 1]:
#                 if 'null' not in i[i.index(j) + 1]:
#                     with allure.step("проверка наличия результатов распознавания"):
#                         assert any(x in i[i.index(j) + 1] for x in matches)
#             elif 'nv.synthesize' in j:
#                 with allure.step("проверка метода nv.say"):
#                     assert any(x in i[i.index(j) + 1] for x in matches)
#             elif 'nv.play_random_sound' in j:
#                 with allure.step("проверка метода nv.play_random_sound"):
#                     assert any(x in i[i.index(j) + 1] for x in matches)
#             elif 'nv.background' in j:
#                 with allure.step("проверка метода nv.background"):
#                     assert 'Office_local' in i[i.index(j) + 1]
