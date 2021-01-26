import time
import pytest
import allure

result = []
synth_phrase_list = []
logs_dict = {}


@allure.feature("Smoke 3.0")
@allure.story("Работа cms")
@allure.title('Провека UI')
def test_v3_cms(db, app_3_web):
    # todo рефакторинг этого теста
    with allure.step("логин в cms v3"):
        pass
    with allure.step("Переходим в проект release_run"):
        agent_setting_url = app_3_web.test_data['agent_setting_url'] + \
                            app_3_web.test_data['test_data']['data_release_run']['agent_uuid']
        app_3_web.BasePage.goto_page(agent_setting_url)
    with allure.step("Наличие элементов меню"):
        app_3_web.AnyAgentPage.opening_all_page_agent()
    with allure.step('Логаут'):
        app_3_web.AnyPage.logout()


@allure.feature("Smoke 3.0")
@allure.story("Yandex")
@allure.title('Создание диалога, получение статистики из БД')
def test_v3_init_call_yandex(api_v3, db):
    global result, logs_dict
    global synth_phrase_list
    db.create_connect(api_v3.database["rw"])
    with allure.step("Авторизация в external_api"):
        token = api_v3.token
        assert len(token['Authorization']) > 10
    with allure.step("Изменение параметров в cms_api"):
        api_v3.set_media_params_release_project(engine='yandex')
    with allure.step("Иницализация диалога в external_api"):
        response = api_v3.init_dialog(msisdn=55555, agent='release')
        dialog_uuid = response.json()['dialog_uuid']
    db.wait_for_done(dialog_uuid)
    with allure.step("Выгрузка данных по диалогу из rw базы"):
        dialog_id = db.select_data(table='dialog', column='uuid', sdata='id', data=str(dialog_uuid))[0][0]
        print('dialog id - ', dialog_id)
    print('call uuid - ', db.select_data(table='call', column='dialog_id', sdata='uuid', data=int(dialog_id)))

    result = db.execute_call_data(table='dialog_stats', data=dialog_id)
    synth_phrase_list = [res[1][res[1].find(':') + 4: res[1].find(',') - 1] for res in result if 'nv.synthesize' in res]

    transcription = ''
    for item in [res[1] for res in result if 'nn.log' in res]:
        if 'city' in item:
            logs_dict['extract_address'] = item
        if 'first' in item:
            logs_dict['extract_person'] = item
        if 'bot' in item:
            transcription += item
        if len(item) <= 4:
            logs_dict['call_duration'] = item
        if 'no_input_timeout' in item:
            logs_dict['get_default'] = item
        if '@yandex' in item or '@google' in item:
            logs_dict['tts_engine'] = item
        if 'yandex' == item or 'google' == item:
            logs_dict['asr_engine'] = item
    logs_dict['call_transcription'] = transcription


@pytest.mark.skip(reason='test method')
@allure.feature("Smoke 3.0")
@allure.story("Yandex")
@allure.title('Отладочный метод')
def test_test(api_v3, db):
    global result, logs_dict
    global synth_phrase_list
    db.create_connect(api_v3.database["rw"]["prod"])
    db.wait_for_done('7dc5a6fc-77f6-4ca0-828e-9a5f78622580')
    result = db.execute_call_data(table='dialog_stats', data='587878')
    # count_call = db.select_data(table='call', column='dialog_id', sdata='count(uuid)', data=int(587878))
    synth_phrase_list = [res[1][res[1].find(':') + 4: res[1].find(',') - 1] for res in result if 'nv.synthesize' in res]

    transcription = ''
    for item in [res[1] for res in result if 'nn.log' in res]:
        if 'city' in item:
            logs_dict['extract_address'] = item
        if 'first' in item:
            logs_dict['extract_person'] = item
        if 'bot' in item:
            transcription += item
        if len(item) <= 4:
            logs_dict['call_duration'] = item
        if 'no_input_timeout' in item:
            logs_dict['get_default'] = item
        if '@yandex' in item or '@google' in item:
            logs_dict['tts_engine'] = item
        if 'yandex' == item or 'google' == item:
            logs_dict['asr_engine'] = item
    logs_dict['call_transcription'] = transcription


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nv_say')
def test_v3_media_part_yandex_say(api_v3, db):
    for res in result:
        if 'nv.say' in res:
            assert any('hello' in d for d in res)
    if not any('nv.say' in d for d in result):
        assert False


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nv_background')
def test_v3_media_part_yandex_background(api_v3, db):
    for res in result:
        if 'nv.background' in res:
            assert any('Office_sound' in d for d in res)
    if not any('nv.background' in d for d in result):
        assert False


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nv_random_sound')
def test_v3_media_part_yandex_play_random_sound(api_v3, db):
    for res in result:
        if 'nv.play_random_sound' in res:
            for i in res:
                flag, flag_2 = 'ага' in i, 'min_delay' in i
                if flag or flag_2 is True:
                    assert True
                    break
            else:
                assert False

    if not any('nv.play_random_sound' in d for d in result):
        assert False


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nv_synthesize')
def test_v3_media_part_yandex_synthesize(api_v3, db):
    count = 0
    for res in result:
        if 'nv.synthesize' in res:
            count += 1
            assert len(res[1]) > 20
    assert count == 15
    if not any('nv.synthesize' in d for d in result):
        assert False


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('listen распознование')
def test_v3_media_part_yandex_listen_interruption(api_v3, db):
    for r in [res[1] for res in result if 'nv.listen' in res]:

        if "распознование" in r:
            text = 'распознование пока произносится это синтезированный тест это нужно говорить и' \
                   ' смотреть результаты распознавания'
            assert text in r
    if not any('nv.listen' in d for d in result):
        assert False


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('listen перебивание по количеству символов')
def test_v3_media_part_yandex_listen_interruption(api_v3, db):
    for r in [res[1] for res in result if 'nv.listen' in res]:
        if "перебивание" in r:
            assert "не должна попасть в результаты распознавания" not in r


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nv.listen прерывание по сущности')
def test_v3_media_part_yandex_nv_listen_stop_entity(api_v3, db):
    for item in [res for res in result if 'nv.listen' in res]:
        if "сущность" in item:
            assert 'этого текста не должно быть в результатах' not in item


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nv_listen тишина')
def test_v3_media_part_yandex_nlu_extract_person(api_v3, db):
    listen_list = [res[1].split(',') for res in result if 'nv.listen' in res]
    utterance_listen_list = [i[i.find(':') + 2:] for res in listen_list for i in res if
                             'utterance' in i]
    assert 'null' in utterance_listen_list
    assert all('error' not in res[1].lower() for res in result if 'nn.dump' in res)


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nv_bridge')
def test_v3_media_part_yandex_bridge(api_v3, db):
    for res in result:
        if 'nv.bridge' in res:
            assert '555555' in res[1]
    if not any('nv.bridge' in d for d in result):
        assert False


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nn_env')
def test_v3_media_part_yandex_nn_env(api_v3, db):
    assert 'Вытащили переменную окружения' in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nn_storage')
def test_v3_media_part_yandex_nn_storage(api_v3, db):
    assert 'Хранилище работает' in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nn_counter')
def test_v3_media_part_yandex_nn_counter(api_v3, db):
    assert 'Счетчик работает' in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nn_has_record valid')
def test_v3_media_part_yandex_nn_has_record_valid(api_v3, db):
    assert 'Проверка наличия записи работает' in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nn_has_record no valid')
def test_v3_media_part_yandex_nn_has_record_no_valid(api_v3, db):
    assert 'Проверка наличия записи работает некорректно' not in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nn_has_records_valid')
def test_v3_media_part_yandex_nn_has_records_valid(api_v3, db):
    assert 'Работает наличия записей проверка' in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nn_has_records no valid')
def test_v3_media_part_yandex_nn_has_records_no_valid(api_v3, db):
    assert 'Проверка наличия записей работает некорректно' not in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nlu_extract_person')
def test_v3_media_part_yandex_nlu_extract_person(api_v3, db):
    assert logs_dict['extract_person'] == "{'first': 'иван', 'last': 'петров', 'middle': 'алексеевич'}"


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nlu_extract_address')
def test_v3_media_part_yandex_nlu_extract_address(api_v3, db):
    assert logs_dict['extract_address'] == "{'city': ['москва', None], 'street': ['ленина', 'улица']," \
                                           " 'building': ['16', None, None], 'appartment': None}"


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nv.get_call_transcription')
def test_v3_media_part_yandex_nv_get_call_transcription(api_v3, db):
    for synth in synth_phrase_list:
        assert synth in logs_dict['call_transcription']


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nv.get_call_duration')
def test_v3_media_part_yandex_nv_get_call_duration(api_v3, db):
    assert len(logs_dict['call_duration']) > 0
    assert int(logs_dict['call_duration']) > 0


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nv.get_default')
def test_v3_media_part_yandex_nv_get_default(api_v3, db):
    assert logs_dict['get_default'] == "{'no_input_timeout': 5000, 'recognition_timeout': 30000," \
                                       " 'speech_complete_timeout': 5000, 'asr_complete_timeout': 5000}"


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nv.hold_and_call и nv.bridge_to_caller')
def test_v3_media_part_yandex_nv_hold_and_call(api_v3, db):
    assert 'Выполним удержание и звонок на другой номер' in synth_phrase_list
    assert 'Привет. Удержание и вызов работает. Сейчас переключу обратно' in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Yandex")
@allure.title('nv_media_params изменение параметров tts, asr на другие')
def test_v3_media_part_yandex_nv_media_params():
    media_params_list = [res[1] for res in result if 'nv.update_media_tokens' in res]
    assert len(media_params_list) > 0
    assert logs_dict['asr_engine'] == 'google'
    assert '@google' in logs_dict['tts_engine']


# @pytest.mark.skip(reason='test')
@allure.feature("Smoke 3.0")
@allure.story("Google")
@allure.title('Создание диалога, получение статистики из БД')
def test_v3_init_call_google(api_v3, db):
    global result, logs_dict
    global synth_phrase_list
    db.create_connect(api_v3.database['rw'])
    with allure.step("Авторизация в external_api"):
        token = api_v3.token
        assert len(token['Authorization']) > 10
    with allure.step("Изменение параметров в cms_api"):
        api_v3.set_media_params_release_project(engine='google')
    with allure.step("Иницализация диалога в external_api"):
        dialog_uuid = api_v3.init_dialog(msisdn=55555, agent='release').json()['dialog_uuid']
    db.wait_for_done(dialog_uuid)
    with allure.step("Выгрузка данных по диалогу из rw базы"):
        dialog_id = db.select_data(table='dialog', column='uuid', sdata='id', data=str(dialog_uuid))[0][0]
        print('dialog id - ', dialog_id)
    result = db.execute_call_data(table='dialog_stats', data=dialog_id)
    print('call uuid - ', db.select_data(table='call', column='dialog_id', sdata='uuid', data=int(dialog_id)))
    synth_phrase_list = [res[1][res[1].find(':') + 4: res[1].find(',') - 1] for res in result if 'nv.synthesize' in res]

    transcription = ''
    for item in [res[1] for res in result if 'nn.log' in res]:
        if 'city' in item:
            logs_dict['extract_address'] = item
        if 'first' in item:
            logs_dict['extract_person'] = item
        if 'bot' in item:
            transcription += item
        if len(item) <= 4:
            logs_dict['call_duration'] = item
        if 'no_input_timeout' in item:
            logs_dict['get_default'] = item
        if '@yandex' in item or '@google' in item:
            logs_dict['tts_engine'] = item
        if 'yandex' == item or 'google' == item:
            logs_dict['asr_engine'] = item
    logs_dict['call_transcription'] = transcription


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nv_say')
def test_v3_media_part_google_say(api_v3, db):
    for res in result:
        if 'nv.say' in res:
            assert any('hello' in d for d in res)
    if not any('nv.say' in d for d in result):
        assert False


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nv_background')
def test_v3_media_part_google_background(api_v3, db):
    for res in result:
        if 'nv.background' in res:
            assert any('Office_sound' in d for d in res)
    if not any('nv.background' in d for d in result):
        assert False


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nv_random_sound')
def test_v3_media_part_google_play_random_sound(api_v3, db):
    for res in result:
        if 'nv.play_random_sound' in res:
            for i in res:
                flag, flag_2 = 'ага' in i, 'min_delay' in i
                if flag or flag_2 is True:
                    assert True
                    break
            else:
                assert False

    if not any('nv.play_random_sound' in d for d in result):
        assert False


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nv_synthesize')
def test_v3_media_part_google_synthesize(api_v3, db):
    count = 0
    for res in result:
        if 'nv.synthesize' in res:
            count += 1
            assert len(res[1]) > 20
    assert count == 15
    if not any('nv.synthesize' in d for d in result):
        assert False


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('listen распознование')
def test_v3_media_part_google_listen_interruption(api_v3, db):
    for r in [res[1] for res in result if 'nv.listen' in res]:

        if "распознование" in r:
            text = 'распознование пока произносится это синтезированный тест это нужно говорить и' \
                   ' смотреть результаты распознавания'
            assert text in r
    if not any('nv.listen' in d for d in result):
        assert False


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('listen перебивание по количеству символов')
def test_v3_media_part_google_listen_interruption(api_v3, db):
    for r in [res[1] for res in result if 'nv.listen' in res]:
        if "перебивание" in r:
            assert "не должна попасть в результаты распознавания" not in r


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nv.listen прерывание по сущности')
def test_v3_media_part_google_nv_listen_stop_entity(api_v3, db):
    for item in [res for res in result if 'nv.listen' in res]:
        if "сущность" in item:
            assert 'этого текста не должно быть в результатах' not in item


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nv_listen тишина')
def test_v3_media_part_google_nlu_extract_person(api_v3, db):
    listen_list = [res[1].split(',') for res in result if 'nv.listen' in res]
    utterance_listen_list = [i[i.find(':') + 2:] for res in listen_list for i in res if
                             'utterance' in i]
    assert 'null' in utterance_listen_list
    assert all('error' not in res[1].lower() for res in result if 'nn.dump' in res)


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nv_bridge')
def test_v3_media_part_google_bridge(api_v3, db):
    for res in result:
        if 'nv.bridge' in res:
            assert '555555' in res[1]
    if not any('nv.bridge' in d for d in result):
        assert False


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nn_env')
def test_v3_media_part_google_nn_env(api_v3, db):
    assert 'Вытащили переменную окружения' in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nn_storage')
def test_v3_media_part_google_nn_storage(api_v3, db):
    assert 'Хранилище работает' in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nn_counter')
def test_v3_media_part_google_nn_counter(api_v3, db):
    assert 'Счетчик работает' in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nn_has_record valid')
def test_v3_media_part_google_nn_has_record_valid(api_v3, db):
    assert 'Проверка наличия записи работает' in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nn_has_record no valid')
def test_v3_media_part_google_nn_has_record_no_valid(api_v3, db):
    assert 'Проверка наличия записи работает некорректно' not in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nn_has_records_valid')
def test_v3_media_part_google_nn_has_records_valid(api_v3, db):
    assert 'Работает наличия записей проверка' in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nn_has_records no valid')
def test_v3_media_part_google_nn_has_records_no_valid(api_v3, db):
    assert 'Проверка наличия записей работает некорректно' not in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nlu_extract_person')
def test_v3_media_part_google_nlu_extract_person(api_v3, db):
    assert logs_dict['extract_person'] == "{'first': 'иван', 'last': 'петров', 'middle': 'алексеевич'}"


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nlu_extract_address')
def test_v3_media_part_google_nlu_extract_address(api_v3, db):
    assert logs_dict['extract_address'] == "{'city': ['москва', None], 'street': ['ленина', 'улица']," \
                                           " 'building': ['16', None, None], 'appartment': None}"


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nv.get_call_transcription')
def test_v3_media_part_google_nv_get_call_transcription(api_v3, db):
    for synth in synth_phrase_list:
        assert synth in logs_dict['call_transcription']


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nv.get_call_duration')
def test_v3_media_part_google_nv_get_call_duration(api_v3, db):
    assert len(logs_dict['call_duration']) > 0
    assert int(logs_dict['call_duration']) > 0


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nv.get_default')
def test_v3_media_part_google_nv_get_default(api_v3, db):
    assert logs_dict['get_default'] == "{'no_input_timeout': 5000, 'recognition_timeout': 30000," \
                                       " 'speech_complete_timeout': 5000, 'asr_complete_timeout': 5000}"


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nv.hold_and_call и nv.bridge_to_caller')
def test_v3_media_part_google_nv_hold_and_call(api_v3, db):
    assert 'Выполним удержание и звонок на другой номер' in synth_phrase_list
    assert 'Привет. Удержание и вызов работает. Сейчас переключу обратно' in synth_phrase_list


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части google")
@allure.title('nv_media_params изменение параметров tts, asr на другие')
def test_v3_media_part_google_nv_media_params():
    media_params_list = [res[1] for res in result if 'nv.update_media_tokens' in res]
    assert len(media_params_list) > 0
    assert logs_dict['asr_engine'] == 'yandex'
    assert '@yandex' in logs_dict['tts_engine']


@allure.feature("Silence")
@allure.story("Тишина + тишина")
def test_v3_silence(api_v3, db):
    db.create_connect(api_v3.database["rw"])
    # with allure.step("Авторизация в external_api"):
    #     token = api_v3.api.auth()
    with allure.step("Изменение параметров в cms_api"):
        # api_v3.api.set_yandex(token)
        token = api_v3.token
        assert len(token['Authorization']) > 10
    with allure.step("Иницализация диалога в external_api"):
        dialog_uuid = api_v3.init_dialog(msisdn=55555, agent='release').json()['dialog_uuid']
    with allure.step("Звонок завершён успешно"):
        db.wait_for_done(dialog_uuid)
        dialog_id = db.select_data(table='dialog', column='uuid', sdata='id', data=str(dialog_uuid))[0][0]
        result_test = db.execute_call_data(table='dialog_stats', data=dialog_id)
        print(db.select_data(table='call', column='dialog_id', sdata='uuid', data=int(dialog_id)))

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
