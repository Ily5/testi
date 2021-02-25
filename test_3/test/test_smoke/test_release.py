import time
import pytest
import allure


@allure.story("Работа cms")
@allure.title('Провека UI')
def test_v3_cms(db, app_3_web):
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
@allure.story("Проверка медиа части Yandex")
class TestYandexEngine:

    @allure.title('nv_say')
    def test_v3_media_part_yandex_say(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        for res in result:
            if 'nv.say' in res:
                assert any('hello' in d for d in res)
        if not any('nv.say' in d for d in result):
            assert False

    @allure.title('nv_background')
    def test_v3_media_part_yandex_background(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        for res in result:
            if 'nv.background' in res:
                assert any('Office_sound' in d for d in res)
        if not any('nv.background' in d for d in result):
            assert False

    @allure.title('nv_random_sound')
    def test_v3_media_part_yandex_play_random_sound(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
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

    @allure.title('nv_synthesize')
    def test_v3_media_part_yandex_synthesize(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        count = 0
        for res in result:
            if 'nv.synthesize' in res:
                count += 1
                assert len(res[1]) > 20
        assert count == 15
        if not any('nv.synthesize' in d for d in result):
            assert False

    @allure.title('listen распознавание')
    def test_v3_media_part_yandex_listen_interruption(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        for r in [res[1] for res in result if 'nv.listen' in res]:

            if "распознавание" in r:
                text = 'распознавание пока произносится это синтезированный тест это нужно говорить и' \
                       ' смотреть результаты распознавания'
                assert text in r
        if not any('nv.listen' in d for d in result):
            assert False

    @allure.title('listen перебивание по количеству символов')
    def test_v3_media_part_yandex_listen_interruption(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        for r in [res[1] for res in result if 'nv.listen' in res]:
            if "перебивание" in r:
                assert "не должна попасть в результаты распознавания" not in r

    @allure.title('nv.listen прерывание по сущности')
    def test_v3_media_part_yandex_nv_listen_stop_entity(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        for item in [res for res in result if 'nv.listen' in res]:
            if "сущность" in item[1]:
                assert 'робот' in item[1]
                assert 'этого текста не должно быть в результатах' not in item[1]

    @allure.title('nv_listen тишина')
    def test_v3_media_part_yandex_nlu_extract_person(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        listen_list = [res[1].split(',') for res in result if 'nv.listen' in res]
        utterance_listen_list = [i[i.find(':') + 2:] for res in listen_list for i in res if
                                 'utterance' in i]
        assert 'null' in utterance_listen_list
        assert all('error' not in res[1].lower() for res in result if 'nn.dump' in res)

    @allure.title('nv_bridge')
    def test_v3_media_part_yandex_bridge(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        for res in result:
            if 'nv.bridge' in res:
                assert '555555' in res[1]
        if not any('nv.bridge' in d for d in result):
            assert False

    @allure.title('nn_env')
    def test_v3_media_part_yandex_nn_env(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        assert 'Вытащили переменную окружения' in synth_phrase_list

    @allure.title('nn_storage')
    def test_v3_media_part_yandex_nn_storage(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        assert 'Хранилище работает' in synth_phrase_list

    @allure.title('nn_counter')
    def test_v3_media_part_yandex_nn_counter(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        assert 'Счетчик работает' in synth_phrase_list

    @allure.title('nn_has_record valid')
    def test_v3_media_part_yandex_nn_has_record_valid(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        assert 'Проверка наличия записи работает' in synth_phrase_list

    @allure.title('nn_has_record no valid')
    def test_v3_media_part_yandex_nn_has_record_no_valid(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        assert 'Проверка наличия записи работает некорректно' not in synth_phrase_list

    @allure.title('nn_has_records_valid')
    def test_v3_media_part_yandex_nn_has_records_valid(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        assert 'Работает наличия записей проверка' in synth_phrase_list

    @allure.title('nn_has_records no valid')
    def test_v3_media_part_yandex_nn_has_records_no_valid(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        assert 'Проверка наличия записей работает некорректно' not in synth_phrase_list

    @allure.title('nlu_extract_person')
    def test_v3_media_part_yandex_nlu_extract_person(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        assert logs_dict['extract_person'] == "{'first': 'иван', 'last': 'петров', 'middle': 'алексеевич'}"

    @allure.title('nlu_extract_address')
    def test_v3_media_part_yandex_nlu_extract_address(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        assert logs_dict['extract_address'] == "{'city': ['москва', None], 'street': ['ленина', 'улица']," \
                                               " 'building': ['16', None, None], 'appartment': None}"

    @allure.title('nv.get_call_transcription')
    def test_v3_media_part_yandex_nv_get_call_transcription(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        for synth in synth_phrase_list:
            assert synth in logs_dict['call_transcription']

    @allure.title('nv.get_call_duration')
    def test_v3_media_part_yandex_nv_get_call_duration(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        assert len(logs_dict['call_duration']) > 0
        assert int(logs_dict['call_duration']) > 0

    @allure.title('nv.get_default')
    def test_v3_media_part_yandex_nv_get_default(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        assert logs_dict['get_default'] == "{'no_input_timeout': 5000, 'recognition_timeout': 30000," \
                                           " 'speech_complete_timeout': 5000, 'asr_complete_timeout': 5000}"

    @allure.title('nv.hold_and_call и nv.bridge_to_caller')
    def test_v3_media_part_yandex_nv_hold_and_call(self, api_v3, db, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        assert 'Выполним удержание и звонок на другой номер' in synth_phrase_list
        assert 'Привет. Удержание и вызов работает. Сейчас переключу обратно' in synth_phrase_list

    @allure.title('nv_media_params изменение параметров tts, asr на другие')
    def test_v3_media_part_yandex_nv_media_params(self, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        media_params_list = [res[1] for res in result if 'nv.update_media_tokens' in res]
        assert len(media_params_list) > 0
        assert logs_dict['asr_engine'] == 'google'
        assert '@google' in logs_dict['tts_engine']

    @allure.title('Сравнение аудиозаписи звонка с эталонной')
    def test_comparison_audio_files_yandex(self, db, file_helper, api_v3, v3_init_yandex):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_yandex
        call_uuid = db.get_call_uuid_by_dialog_id(dialog_id=dialog_id, call_duration=70)[0][0]
        file_name = 'call_sound_{uuid}'.format(uuid=call_uuid)
        test_file_prop = file_helper.get_call_file_properties(create_file_name=file_name, call_uuid=call_uuid)
        reference_file_prop = file_helper.get_call_file_properties('reference_call_yandex',
                                                                   api_v3.test_data['reference_call_uuid_yandex'])
        print(reference_file_prop)
        print(test_file_prop)
        assert file_helper.get_percent(test_file_prop['size'], reference_file_prop['size']) < 5
        assert file_helper.get_percent(test_file_prop['duration'], reference_file_prop['duration']) < 5
        assert file_helper.get_percent(test_file_prop['rms_sum'], reference_file_prop['rms_sum']) < 5
        assert file_helper.get_percent(test_file_prop['cent_sum'], reference_file_prop['cent_sum']) < 5


@allure.feature("Smoke 3.0")
@allure.story("Проверка медиа части Google")
class TestGoogleEngine:

    @allure.title('nv_say')
    def test_v3_media_part_google_say(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        for res in result:
            if 'nv.say' in res:
                assert any('hello' in d for d in res)
        if not any('nv.say' in d for d in result):
            assert False

    @allure.title('nv_background')
    def test_v3_media_part_google_background(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        for res in result:
            if 'nv.background' in res:
                assert any('Office_sound' in d for d in res)
        if not any('nv.background' in d for d in result):
            assert False

    @allure.title('nv_random_sound')
    def test_v3_media_part_google_play_random_sound(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
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

    @allure.title('nv_synthesize')
    def test_v3_media_part_google_synthesize(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        count = 0
        for res in result:
            if 'nv.synthesize' in res:
                count += 1
                assert len(res[1]) > 20
        assert count == 15
        if not any('nv.synthesize' in d for d in result):
            assert False

    @allure.title('listen распознавание')
    def test_v3_media_part_google_listen_interruption(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        for r in [res[1] for res in result if 'nv.listen' in res]:

            if "распознавание" in r:
                text = 'распознавание пока произносится это синтезированный тест это нужно говорить и' \
                       ' смотреть результаты распознавания'
                assert text in r
        if not any('nv.listen' in d for d in result):
            assert False

    @allure.title('listen перебивание по количеству символов')
    def test_v3_media_part_google_listen_interruption(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        for r in [res[1] for res in result if 'nv.listen' in res]:
            if "перебивание" in r:
                assert "не должна попасть в результаты распознавания" not in r

    @allure.title('nv.listen прерывание по сущности')
    def test_v3_media_part_google_nv_listen_stop_entity(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        for item in [res for res in result if 'nv.listen' in res]:
            if "сущность" in item[1]:
                assert 'робот' in item[1]
                assert 'этого текста не должно быть в результатах' not in item[1]

    @allure.title('nv_listen тишина')
    def test_v3_media_part_google_nlu_extract_person(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        listen_list = [res[1].split(',') for res in result if 'nv.listen' in res]
        utterance_listen_list = [i[i.find(':') + 2:] for res in listen_list for i in res if
                                 'utterance' in i]
        assert 'null' in utterance_listen_list
        assert all('error' not in res[1].lower() for res in result if 'nn.dump' in res)

    @allure.title('nv_bridge')
    def test_v3_media_part_google_bridge(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        for res in result:
            if 'nv.bridge' in res:
                assert '555555' in res[1]
        if not any('nv.bridge' in d for d in result):
            assert False

    @allure.title('nn_env')
    def test_v3_media_part_google_nn_env(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        assert 'Вытащили переменную окружения' in synth_phrase_list

    @allure.title('nn_storage')
    def test_v3_media_part_google_nn_storage(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        assert 'Хранилище работает' in synth_phrase_list

    @allure.title('nn_counter')
    def test_v3_media_part_google_nn_counter(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        assert 'Счетчик работает' in synth_phrase_list

    @allure.title('nn_has_record valid')
    def test_v3_media_part_google_nn_has_record_valid(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        assert 'Проверка наличия записи работает' in synth_phrase_list

    @allure.title('nn_has_record no valid')
    def test_v3_media_part_google_nn_has_record_no_valid(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        assert 'Проверка наличия записи работает некорректно' not in synth_phrase_list

    @allure.title('nn_has_records_valid')
    def test_v3_media_part_google_nn_has_records_valid(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        assert 'Работает наличия записей проверка' in synth_phrase_list

    @allure.title('nn_has_records no valid')
    def test_v3_media_part_google_nn_has_records_no_valid(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        assert 'Проверка наличия записей работает некорректно' not in synth_phrase_list

    @allure.title('nlu_extract_person')
    def test_v3_media_part_google_nlu_extract_person(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        assert logs_dict['extract_person'] == "{'first': 'иван', 'last': 'петров', 'middle': 'алексеевич'}"

    @allure.title('nlu_extract_address')
    def test_v3_media_part_google_nlu_extract_address(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        assert logs_dict['extract_address'] == "{'city': ['москва', None], 'street': ['ленина', 'улица']," \
                                               " 'building': ['16', None, None], 'appartment': None}"

    @allure.title('nv.get_call_transcription')
    def test_v3_media_part_google_nv_get_call_transcription(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        for synth in synth_phrase_list:
            assert synth in logs_dict['call_transcription']

    @allure.title('nv.get_call_duration')
    def test_v3_media_part_google_nv_get_call_duration(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        assert len(logs_dict['call_duration']) > 0
        assert int(logs_dict['call_duration']) > 0

    @allure.title('nv.get_default')
    def test_v3_media_part_google_nv_get_default(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        assert logs_dict['get_default'] == "{'no_input_timeout': 5000, 'recognition_timeout': 30000," \
                                           " 'speech_complete_timeout': 5000, 'asr_complete_timeout': 5000}"

    @allure.title('nv.hold_and_call и nv.bridge_to_caller')
    def test_v3_media_part_google_nv_hold_and_call(self, api_v3, db, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        assert 'Выполним удержание и звонок на другой номер' in synth_phrase_list
        assert 'Привет. Удержание и вызов работает. Сейчас переключу обратно' in synth_phrase_list

    @allure.title('nv_media_params изменение параметров tts, asr на другие')
    def test_v3_media_part_google_nv_media_params(self, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        media_params_list = [res[1] for res in result if 'nv.update_media_tokens' in res]
        assert len(media_params_list) > 0
        assert logs_dict['asr_engine'] == 'yandex'
        assert '@yandex' in logs_dict['tts_engine']

    @allure.title('Сравнение аудиозаписи звонка с эталонной')
    def test_comparison_audio_files_google(self, db, file_helper, api_v3, v3_init_google):
        result, synth_phrase_list, logs_dict, dialog_id = v3_init_google
        call_uuid = db.get_call_uuid_by_dialog_id(dialog_id=dialog_id, call_duration=70)[0][0]
        file_name = 'call_sound_{uuid}'.format(uuid=call_uuid)
        test_file_prop = file_helper.get_call_file_properties(create_file_name=file_name, call_uuid=call_uuid)
        reference_file_prop = file_helper.get_call_file_properties('reference_call_google',
                                                                   api_v3.test_data['reference_call_uuid_google'])
        print(reference_file_prop)
        print(test_file_prop)
        assert file_helper.get_percent(test_file_prop['size'], reference_file_prop['size']) < 5
        assert file_helper.get_percent(test_file_prop['duration'], reference_file_prop['duration']) < 5
        assert file_helper.get_percent(test_file_prop['rms_sum'], reference_file_prop['rms_sum']) < 5
        assert file_helper.get_percent(test_file_prop['cent_sum'], reference_file_prop['cent_sum']) < 5


@allure.feature("Silence")
@allure.story("Тишина + тишина")
def test_v3_silence(api_v3, db):
    time.sleep(10)
    db.create_connect(api_v3.database["RW"])
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
