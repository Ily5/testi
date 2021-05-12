import time
from datetime import datetime
from typing import List, Union, Dict, Any

import pytest
import requests

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


# agent_uuid = "a4096ad9-f0b8-41fc-8393-93a88ef18c40"
# agent_uuid = "051100aa-f1dd-4e41-889d-a7673c4d5c59"


def test_hello(get_step_max_min):
    step, max_channels, min_channels = get_step_max_min
    print(get_step_max_min)
    for i in range(min_channels, max_channels + step, step):
        print(i)


def test_asr(cms_api_v3, api_v3, pool_api_v3, db, get_step_max_min):
    expected_result = "это бесплатная услуга никакой абонентской платы подключение бесплатное на тариф\
    тоже не повлияет это просто как постраховка вас выручит если вдруг не успеете средства внести на телефон\
    вы сможете всегда позвонить потраченую сумму сможете внести поднее в течении трех дней будет просто в режиме\
    ожидание находиться активизируется она только если баланс близок к нолю то есть если у вас есть средства на \
    телефоне вы её даже не заметите"
    # чистим очередь
    asr_helper = AsrResultHelper()
    agent_uuid = api_v3.test_data["for_asr_tests"]["agent_uuid"]
    step, max_channels, min_channels = get_step_max_min
    for i in range(min_channels, max_channels + step, step):
        clear_queue(api_v3, {"agent_uuid": agent_uuid}, pool_api_v3)
        asr_results = asr_result_check(
            api_v3, cms_api_v3, db, step_rise=i, count_dialog=i * 2, agent_uuid=agent_uuid
        )
        for result in asr_results:
            wer, cer = asr_helper.get_wer_cer(expected_result, result.get("utterance"))
            call_duration = result["call_duration"]
            print("duration", call_duration)
            print(result["utterance"])
            print("wer= ", wer)
            print("cer= ", cer)
            # assert int(call_duration) <= 30
            # assert wer <= 0.35
            # assert cer <= 0.15

    # оцениваем продолжительность

    # если все ок -- увеличиваем tcl


def test_tcl(api_v3):
    agent_uuid = api_v3.test_data["for_asr_tests"]["agent_uuid"]
    # agent_uuid = 'f29c639f-f3ff-46bb-9425-fe2ffb27796c'
    # agent_uuid = "327b3679-3cda-4540-b6df-1804127aa1a8"
    upload_dialog_body = [{"msisdn": 123123} for _ in range(1000)]
    resp_upload_dialog = api_v3.upload_group_dialogs(agent_uuid, upload_dialog_body)
    print(resp_upload_dialog.request.url)
    print(resp_upload_dialog.request.headers)

    print(resp_upload_dialog.request.body)

    print(resp_upload_dialog.request.hooks)

    print(resp_upload_dialog.request.method)
    print(resp_upload_dialog.status_code)
    print(resp_upload_dialog.json())


def asr_result_check(
    api_v3, cms_api_v3, db, step_rise: int, count_dialog: int, agent_uuid: str
) -> List[Dict[str, Union[str, int]]]:
    tcl = 0
    change_tcl(agent_uuid, api_v3, tcl)

    upload_dialog_body = [{"msisdn": 123123} for _ in range(count_dialog)]
    resp_upload_dialog = api_v3.upload_group_dialogs(agent_uuid, upload_dialog_body)
    print(
        f"\n {datetime.now()} - Upload dialogs - status code = {resp_upload_dialog.status_code}"
    )
    print(f"\n {datetime.now()} - Waiting while created dialogs = uploaded dialogs")
    upload_timeout = time.time() + 600
    count_dialogs: int = 0
    while count_dialogs != len(upload_dialog_body):
        count_dialogs = api_v3.get_dialogs_agent(agent_uuid).json()["total_count"]
        print(
            f"\n {datetime.now()} - Dialogs were upload {count_dialogs} of {len(upload_dialog_body)}"
        )
        if time.time() >= upload_timeout:
            raise TimeoutError

    tcl += step_rise
    change_tcl(agent_uuid, api_v3, tcl)

    # ожидаем пока активные звонки = tcl и получаем uuid этих звонков, диалогов
    active_calls: List[Dict[str, str]] = []
    count_active_calls = 0
    timeout_active_calls = time.time() + 600
    while count_active_calls < tcl:
        all_active_calls = cms_api_v3.get_calls_agent_in_queue(
            agent_uuid=agent_uuid, result="active"
        ).json()
        count_all_calls = cms_api_v3.get_calls_agent_in_queue(
            agent_uuid=agent_uuid
        ).json()["total_count"]
        count_active_calls = all_active_calls["total_count"]
        # time.sleep(0.4)
        print(
            f"\n {datetime.now()} - Count active calls - {count_active_calls}, All calls {count_all_calls}"
        )
        if time.time() >= timeout_active_calls:
            raise TimeoutError
        active_calls = [
            dict(
                call_uuid=call["uuid"],
                dialog_uuid=call["dialog"]["uuid"],
                status=call["result"],
            )
            for call in all_active_calls["data"]
        ]
    print(active_calls)

    # меняем TCL на 0
    # change_tcl(agent_uuid, api_v3, 0)

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
        print(
            f"\n {datetime.now()} - Dialogs update - {dialog_need_update[0][0]} of {len(active_dialogs_uuid)}"
        )
        if (
            len(status_set) == 1
            and "done" in status_set
            and dialog_need_update[0][0] == len(active_dialogs_uuid)
        ):
            break
        time.sleep(1)
    utterance_and_duration: List[Dict[str, Union[str, int]]] = []
    for calls in active_calls:
        utterance_and_duration.append(cms_api_v3.get_call_nn_log(calls["call_uuid"]))
    return utterance_and_duration


def change_tcl(agent_uuid, api_v3, tcl):
    resp_change_tcl = api_v3.change_base_agent_setting(
        agent_uuid=agent_uuid, request_body={"total_channel_limit": tcl}
    )
    print(
        f"\n {datetime.now()} - Change TCL = {tcl} - status code = {resp_change_tcl.status_code}"
    )
