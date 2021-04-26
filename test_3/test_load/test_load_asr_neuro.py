import time
from datetime import datetime
from typing import List, Union, Dict, Any

import pytest

from test_3.fixture.Helper import AsrResultHelper
from test_3.conftest import clear_queue

r""""

Примерный скрипт тестирования:
0. set_up -- set default settings -> TCL <=> +- 10, ASR engine, pool
1. Загружаем много дилогов через API
2. Смотрим результаты распознавания при теущем числе каналов, если ок -> set TCL + 10
    - ждем пока активные звонки == set_TCL ->
    - получам uuid в
3. Доходим до необходимого значения если все ок -> превышаем это значение и чекаем триггер превышения допустимой нагрузки
"""
agent_uuid = "a4096ad9-f0b8-41fc-8393-93a88ef18c40"


def test_asr(cms_api_v3, api_v3, pool_api_v3, db):
    expected_result = "это бесплатная услуга никакой абонентской платой подключение бесплатный на тариф тоже не повлияет это просто как постраховка вас выручит если вдруг не успейте средство внести на телефон вы сможете всегда позвонить потраченую сумму сможете внести поднее в течении трех дней будет просто врежемие ожидание находиться активизируется она только если баланс безокнулю то есть если у вас есть средства на телефоне вы её даже не зонитите"
    # чистим очередь
    asr_helper = AsrResultHelper()
    for step in range(1, 4, 1):
        clear_queue(api_v3,
                    {"agent_uuid": agent_uuid},
                    pool_api_v3)
        asr_results = asr_result_check(api_v3, cms_api_v3, db, step, step * 2)
        for result in asr_results:
            print(asr_helper.get_wer_cer(expected_result, result.get("utterance")))

    # оцениваем продолжительность

    # если все ок -- увеличиваем tcl


def asr_result_check(api_v3, cms_api_v3, db, step_rise: int, count_dialog: int):
    # count_dialog = 50
    # TODO вынести изменение TCL
    tcl = 0
    resp_change_tcl = api_v3.change_base_agent_setting(
        agent_uuid=agent_uuid,
        request_body={"total_channel_limit": tcl}
    )
    print(f"\n {datetime.now()} - Change TCL = {tcl} - status code = {resp_change_tcl.status_code}")
    upload_dialog_body = [{"msisdn": 123123} for _ in range(count_dialog)]
    resp_upload_dialog = api_v3.upload_group_dialogs(agent_uuid, upload_dialog_body)
    print(f"\n {datetime.now()} - Upload dialogs - status code = {resp_upload_dialog.status_code}")
    print(f"\n {datetime.now()} - Waiting while created dialogs = uploaded dialogs")
    upload_timeout = time.time() + 600
    count_dialogs: int = 0
    while count_dialogs != len(upload_dialog_body):
        count_dialogs = api_v3.get_dialogs_agent(agent_uuid).json()['total_count']
        print(f"\n {datetime.now()} - Dialogs were upload {count_dialogs} of {len(upload_dialog_body)}")
        if time.time() >= upload_timeout:
            raise TimeoutError
    tcl += step_rise
    resp_change_tcl = api_v3.change_base_agent_setting(
        agent_uuid=agent_uuid,
        request_body={"total_channel_limit": tcl}
    )
    print(f"\n {datetime.now()} - Change TCL = {tcl} - status code = {resp_change_tcl.status_code}")
    # ожидаем пока активные звонки = tcl и получаем uuid этих звонков, диалогов
    active_calls: List[Dict[str, str]] = []
    count_active_calls = 0
    timeout_active_calls = time.time() + 600
    while count_active_calls != tcl:
        all_active_calls = cms_api_v3.get_calls_agent_in_queue(agent_uuid=agent_uuid, result="active").json()
        count_active_calls = all_active_calls["total_count"]
        time.sleep(1)
        print(f"\n {datetime.now()} - Count active calls - {count_active_calls}, All calls {len(all_active_calls)}")
        if time.time() >= timeout_active_calls:
            raise TimeoutError

    # меняем TCL на 0
    # resp_change_tcl = api_v3.change_base_agent_setting(
    #     agent_uuid=agent_uuid,
    #     request_body={"total_channel_limit": 0}
    # )
    # print(f"\n {datetime.now()} - Change TCL = 0 - status code = {resp_change_tcl.status_code}")
    # print(active_calls)

    # дожидаемся пока завершаться диалоги получем результаты распознавания и продолжительность
    active_dialogs_uuid = tuple(dialog["dialog_uuid"] for dialog in active_calls)
    while True:
        status_set = set()
        dialogs_status = db.db_conn(
            f"SELECT result FROM dialog WHERE uuid in {active_dialogs_uuid}"
        )
        for status in dialogs_status:
            status_set.add(status[0])
        print(f"\n {datetime.now()} - Dialogs status set - {status_set}")
        dialog_need_update = db.db_conn(
            f"SELECT count(id) FROM dialog WHERE uuid in {active_dialogs_uuid} and need_update is false"
        )
        print(f"\n {datetime.now()} - Dialogs update - {dialog_need_update[0][0]} of {len(active_dialogs_uuid)}")
        if len(status_set) == 1 and 'done' in status_set and dialog_need_update[0][0] == len(active_dialogs_uuid):
            break
        time.sleep(1)
    utterance_and_duration: List[Dict[str, Union[str, int]]] = []
    for calls in active_calls:
        utterance_and_duration.append(cms_api_v3.get_call_nn_log(calls["call_uuid"]))
    for result in utterance_and_duration:
        print(result['utterance'])
    return utterance_and_duration
