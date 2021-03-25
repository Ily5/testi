import time
from datetime import datetime

from fixture.database import Connector
from test_3.fixture.Helper import CreateReportAsr

""""
2 Скрипта для двух проектов: with_ans, no_ans
"""
database = {
    "database": "pbx_refactor",
    "user": "postgres",
    "password": "",
    "host": "10.131.0.80",
    "port": 5006,
}

db_conn = Connector(data=database)


def test_asr_no_ans(api_v3, get_asr_engine):
    agent_uuid = "b2ebe88e-6c7b-4e86-919a-3eeb248f8035"
    agent_id = "408"
    agent_name = "test_asr_no_ans"
    yandex_asr_uuid = "40a9e26c-06c0-4c0b-b8fd-73827013d6b2"
    google_asr_uuid = "e3e9a0bd-73ce-4ae2-833c-6f667238f0d0"
    count_audio_files = 5670
    # count_audio_files = 30

    print(f"\n {datetime.now()} - ASR engine must be set - {get_asr_engine}")

    final_results = get_final_result_asr(
        agent_id,
        agent_name,
        agent_uuid,
        api_v3,
        count_audio_files,
        get_asr_engine,
        google_asr_uuid,
        yandex_asr_uuid,
    )

    create_final_report = CreateReportAsr()
    create_final_report.create_asr_result_to_csv(
        final_results, f"{get_asr_engine}_no_ans"
    )


def get_final_result_asr(
        agent_id,
        agent_name,
        agent_uuid,
        api_v3,
        count_audio_files,
        asr_engine,
        google_asr_key_uuid,
        yandex_asr_key_uuid,
):
    change_asr_engine(
        agent_name,
        agent_uuid,
        api_v3,
        asr_engine,
        google_asr_key_uuid,
        yandex_asr_key_uuid,
    )
    last_dialog = db_conn.db_conn(
        f"SELECT id FROM dialog where agent_id = {agent_id} ORDER BY id DESC limit 1"
    )
    if len(last_dialog) > 0:
        last_dialog_id = last_dialog[0][0]
    else:
        last_dialog_id = db_conn.db_conn(
            "SELECT id FROM dialog ORDER BY id DESC limit 1"
        )[0][0]
    print(f"\n {datetime.now()} - last dialog id = {last_dialog_id}")
    upload_dialogs(agent_uuid, api_v3, count_audio_files)
    timeout_upload_dialogs = time.time() + 30000
    while True:
        if time.time() >= timeout_upload_dialogs:
            raise TimeoutError("Timeout upload dialogs")
        count_upload_dialogs = db_conn.db_conn(
            f"SELECT count(id) FROM dialog where id > {last_dialog_id}"
        )
        print(
            f"\n {datetime.now()} - Dialogs were loaded {count_upload_dialogs[0][0]} of {count_audio_files}"
        )
        if count_upload_dialogs[0][0] == count_audio_files:
            break
        time.sleep(1)

    uploaded_dialogs = db_conn.db_conn(
        f"SELECT id FROM dialog where agent_id = {agent_id} and id > {last_dialog_id}"
    )
    list_dialog_id = []
    for dialog in uploaded_dialogs:
        list_dialog_id.append(dialog[0])
    print(f"\n {datetime.now()} - id of all dialogs  {list_dialog_id}")

    tuple_dialog_id = tuple(list_dialog_id)

    timeout_pending_dialogs = time.time() + 30000
    while True:
        if time.time() >= timeout_pending_dialogs:
            raise TimeoutError("Timeout execute dialogs")
        results_all_dialogs = db_conn.db_conn(
            f"SELECT result FROM dialog where id > {last_dialog_id} and agent_id = {agent_id}"
        )
        results_set = set()
        for dialog_result in results_all_dialogs:
            results_set.add(dialog_result[0])
        print(f"\n {datetime.now()} - Set of results dialogs  {results_set}")
        dialogs_is_done = db_conn.db_conn(
            f"SELECT count(id) from dialog where id > {last_dialog_id} and agent_id = {agent_id} and result = 'done' "
        )
        print(
            f"\n {datetime.now()} - Dialogs were done {dialogs_is_done[0][0]} of {count_audio_files}"
        )

        time.sleep(2)
        if len(results_set) == 1 and "done" in results_set:
            break
    final_results = db_conn.db_conn(
        f"SELECT name, data from dialog_stats where action = 'nn.log' and dialog_id in {tuple_dialog_id}"
    )
    return final_results


def upload_dialogs(agent_uuid, api_v3, dialogs_count: int):
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
    print(
        f"\n {datetime.now()} - status code upload dialogs {response_upload_dialogs.status_code}"
    )
    if "2" in str(response_upload_dialogs.text)[0]:
        print("\n", response_upload_dialogs.status_code)
        print("\n", response_upload_dialogs.text)
        raise Exception("Upload group dialog error")
    print(
        f"\n {datetime.now()} - task_uuid upload dialogs  {response_upload_dialogs.json()['task_uuid']}"
    )
    print(
        f"\n {datetime.now()} - bulk_uuid upload dialogs  {response_upload_dialogs.json()['bulk_uuid']}"
    )


def change_asr_engine(
        agent_name, agent_uuid, api_v3, asr_engine, google_asr_uuid, yandex_asr_uuid
):
    data_change_asr_engine = {
        "speed": 1,
        "pitch": 1,
        "name": agent_name,
    }
    if asr_engine in "yandex":
        data_change_asr_engine["asr_key_uuid"] = yandex_asr_uuid
        data_change_asr_engine["reserved_asr_key_uuid"] = google_asr_uuid
    if asr_engine in "google":
        data_change_asr_engine["asr_key_uuid"] = google_asr_uuid
        data_change_asr_engine["reserved_asr_key_uuid"] = yandex_asr_uuid
    response_change_asr_engine = api_v3.request_send(
        method="PUT",
        path=api_v3.path_end_point["set_media_params"] + agent_uuid,
        json=data_change_asr_engine,
    )
    if response_change_asr_engine.status_code != 200:
        print(response_change_asr_engine.status_code)
        print(response_change_asr_engine.text)
        raise Exception("Change asr engine error")
    print(
        f"\n {datetime.now()} - status code change asr engine {response_change_asr_engine.status_code}"
    )


