import time
import pytest
import allure


@pytest.fixture(scope='class')
def v3_init_yandex(api_v3, db, params_agent_uuid):
    return init_dialog('yandex', db, api_v3)


@pytest.fixture(scope='class')
def v3_init_google(api_v3, db, params_agent_uuid):
    time.sleep(7)
    return init_dialog('google', db, api_v3)


def init_dialog(engine: str, db, api_v3):
    db.create_connect(api_v3.database["RW"])
    with allure.step("Авторизация в external_api"):
        token = api_v3.token
        assert len(token['Authorization']) > 10
    with allure.step("Изменение параметров в cms_api"):
        api_v3.set_media_params_release_project(engine=engine)
    with allure.step("Иницализация диалога в external_api"):
        response = api_v3.init_dialog(msisdn=55555, agent='release',  api=api_v3)
        dialog_uuid = response.json()['dialog_uuid']
        print('\n dialog_uuid ', dialog_uuid)
    db.wait_for_done(dialog_uuid)
    with allure.step("Выгрузка данных по диалогу из rw базы"):
        dialog_id = db.select_data(table='dialog', column='uuid', sdata='id', data=str(dialog_uuid))[0][0]
        print('dialog id - ', dialog_id)
    print('call uuid - ', db.select_data(table='call', column='dialog_id', sdata='uuid', data=int(dialog_id)))

    result = db.execute_call_data(table='dialog_stats', data=dialog_id)
    synth_phrase_list = [res[1][res[1].find(':') + 4: res[1].find(',') - 1] for res in result if
                         'nv.synthesize' in res]

    transcription = ''
    logs_dict = {}
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
    return result, synth_phrase_list, logs_dict, dialog_id
