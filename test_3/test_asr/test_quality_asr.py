import os
import time
import json
from datetime import datetime
from typing import Dict, Union
from test_3.fixture.Helper import AsrResultHelper
import pathlib

""""
1. Запускам звонки
2. Дожидаемся пока закончатся
3. Парсим базу с результатами распознавания
4. Считаем средний ver, cer
"""


def test_quality_asr(api_v3, db):
    agent_uuid = 'f7cf51e8-5022-4d40-9b04-4bc97b5f142f'
    agent_id = '57'
    dialogs_count = 30

    data_create_dialog = []
    for i in range(dialogs_count):
        data_create_dialog.append(
            {"msisdn": "55555", "call_number": f"{i + 1}", "script_entry_point": "main"}
        )
    response_upload_dialogs = api_v3.request_send(
        method="POST",
        path=api_v3.path_end_point["upload_group_dialogs"],
        params={"agent_uuid": agent_uuid},
        json=data_create_dialog,
        status_code=409,
    )
    print(response_upload_dialogs.status_code)
    print(response_upload_dialogs.text)
    last_id_dialog_stats = db.db_conn(
        f"SELECT id FROM dialog_stats ORDER BY id DESC limit 1"
    )[0][0]
    last_dialog_id = db.db_conn(
        f"SELECT id FROM dialog WHERE agent_id = {agent_id} ORDER BY id DESC limit 1"
    )[0][0]

    # дожидаемся пока все диалоги завершаться
    timeout_done = time.time() + 1500
    while True:
        if time.time() >= timeout_done:
            raise TimeoutError("Timeout execute dialogs")
        results_all_dialogs = db.db_conn(
            f"SELECT result FROM dialog where id > {last_dialog_id} and agent_id = {agent_id}"
        )
        results_set = set()
        for dialog_result in results_all_dialogs:
            results_set.add(dialog_result[0])
        print(f"\n {datetime.now()} - Set of results dialogs  {results_set}")
        dialogs_is_done = db.db_conn(
            f"SELECT count(id) from dialog where id > {last_dialog_id} and agent_id = {agent_id} and result = 'done' "
        )
        print(
            f"\n {datetime.now()} - Dialogs were done {dialogs_is_done[0][0]} of {dialogs_count}"
        )

        time.sleep(2)
        if len(results_set) == 1 and "done" in results_set:
            break

    # получаем результаты распознавания
    all_asr_results = db.db_conn(
        f"SELECT name, data FROM dialog_stats WHERE name like 'test_asr%'\
          and id >{last_id_dialog_stats} ORDER BY id DESC")

    actual_results = {result[0]: result[1] for result in all_asr_results}

    asr_helper = AsrResultHelper()
    path_to_expected_result = f"{os.path.abspath(os.path.dirname(__file__))}/asr_results.json"
    list_ver_cer = []

    with open(path_to_expected_result) as file:
        asr_result: dict = json.load(file)
        for file_name, utterance in asr_result.items():
            wer, cer = asr_helper.get_wer_cer(utterance, actual_results[file_name])
            list_ver_cer.append({"file_name": file_name, "wer": wer, "cer": cer})
            if wer > 0.30 or cer > 0.20:
                print(f"{file_name} , wer = {wer}, cer = {cer}")
                print(f"\nActual_result - {actual_results[file_name]} \nExpected result - {utterance}")

    avg_wer = sum([i["wer"] for i in list_ver_cer]) / len(list_ver_cer)
    avg_cer = sum([i["cer"] for i in list_ver_cer]) / len(list_ver_cer)
    print(f"avg_wer = {avg_wer}  avg_cer = {avg_cer}")

