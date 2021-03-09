import time
import pytest
import paramiko
from test_3.fixture.api import APIClientV3


def test_001(ssh_helper):
    # client = paramiko.SSHClient()
    # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # client.connect(hostname=ssh_helper.hosts['id_2'], username=ssh_helper.username)
    # result_1 = client.exec_command('tail -n 20 /var/log/ivr/logic-executor-offline.log')
    # res_1_end = result_1[1].read() + result_1[2].read()
    # print(res_1_end)
    # print(type(res_1_end))
    #
    # print(type(str(res_1_end)))
    # client.close()
    # result = ssh_helper.get_last_n_line_log(host=ssh_helper.hosts['id_2'], log_name='offline', n=5)
    #
    # print(result)
    #
    # result = ssh_helper.get_count_lines_in_log(host=ssh_helper.hosts['id_2'], log_name='offline', grep_text='INFO')
    # print(result)
    client = ssh_helper.client(host="10.129.0.108")
    res = client.exec_command("sudo systemctl restart caller.service")
    res_end = str((res[1].read() + res[2].read()), encoding="utf-8")
    print(res_end)
    client.close()


""""Сценарий нагрузочного тестирования LE Online
I Максимальное количество звонков обрабатываемое лоджиком
 (изменеие конфига фрисвича https://neuronet.atlassian.net/browse/NP-1955)
    1. Устанавливаем дефолтной нужную логику с бесконечным циклом в LE online ++++++
    2. Устанавливаем TCL = 0
    3. Загружаем диалоги, ждем пока они встанут в очередь
    4. Меняем TCL на 1000
    5. Ждем пока звонки начнуться, считаем в раел тайм сколько звонков обрабатывается в данный момент
        - как это сделать? через лог/ через БД ?
    6. Подчищаем все после теста (удаляем звонки)
    
II. Сколько раз был обработан каждый метод за 1 минуту
    0. В логике запускаем бесконечный вызов какого-то метода
    1. Устанавливаем дефолтной нужную логику ++++++++++++++
    2. Загружаем звонок 
    3. Чекаем логи пока звонок не начнется 
    4. Засекаем 60 секунд
    5. Считаем количество вызовов функции через декоратор в логике
    6. Ищем в БД статистику по кажому параметру и выводим их на печать
    
"""


def test_load_le_online(api_v3, db):
    params = api_v3.test_data['data_release_run']['agent_uuid']
    change_default_logic(api_v3, params, "online")
    response = api_v3.init_dialog(
        msisdn="55555",
        agent="release",
        api=api_v3,
        params_agent_uuid=params,
        default_logic=False
    )
    dialog_uuid = response.json()['dialog_uuid']
    print(dialog_uuid)
    # dialog_uuid = "61e1431b-8c9a-4178-9476-2766ea3e1fc6"

    command = f"SELECT result FROM dialog WHERE uuid = '{dialog_uuid}'"
    timeout = time.time() + 30000
    while True:
        res = db.db_conn(command)
        if len(res) > 0 and res[0][0] == 'done':
            break
        if time.time() >= timeout:
            raise TimeoutError

    dialog_id = db.select_data(table='dialog', column='uuid', sdata='id', data=str(dialog_uuid))[0][0]

    result = db.db_conn(
        f"select action, name, data  from dialog_stats where dialog_id = '{dialog_id}' and data is not null")
    for i in result:

        if 'log' in i[0]:
            print('\n', i)


def test_load_le_online_count(api_v3, db, clear_queue_new):
    params = api_v3.test_data['data_release_run']['agent_uuid']
    change_default_logic(api_v3, params, "count")

    api_v3.request_send(
        method="PUT",
        path=api_v3.path_end_point["put_change_agent_settings"],
        json={"total_channel_limit": 10000},
        params={"agent_uuid": params},
    )

    data = [{'msisdn': '55555', "script_entry_point": "main", "script_name": "test_release"}]
    for i in range(500):
        data.append(data[0])
    response = api_v3.request_send(method='POST',
                                   path=api_v3.path_end_point['upload_group_dialogs'],
                                   params={'agent_uuid': params},
                                   json=data,
                                   status_code=409)

    timeout = time.time() + 3000
    while True:
        result = db.db_conn(f"SELECT count(id) from call where agent_id =117 and result in ('pending', 'queued', null)")
        print('Активных звонков - ', result[0][0])
        time.sleep(0.1)
        if time.time() >= timeout:
            break


@pytest.fixture()
def clear_queue_new(request, api_v3, pool_api_v3):
    def clear():
        params_agent_uuid = {"agent_uuid": api_v3.test_data['data_release_run']['agent_uuid']}
        api_v3.request_send(
            method="PUT",
            path=api_v3.path_end_point["put_change_agent_settings"],
            json={"total_channel_limit": 8},
            params=params_agent_uuid,
        )

        api_v3.request_send(method='POST',
                            path=api_v3.path_end_point['return_queue_dialogs'],
                            params=params_agent_uuid,
                            json={},
                            status_code=409)
        api_v3.request_send(method='POST',
                            path=api_v3.path_end_point['remove_queue_dialogs'],
                            params=params_agent_uuid,
                            status_code=409)

        pool_api_v3.request_send(method='POST',
                                 path=pool_api_v3.path_end_point['return_calls'],
                                 params=params_agent_uuid,
                                 json={})
        pool_api_v3.request_send(method='DELETE',
                                 path=pool_api_v3.path_end_point['get_list_queue_calls'],
                                 params=params_agent_uuid,
                                 json={})

    request.addfinalizer(clear)


def change_default_logic(api: APIClientV3, params, logic_name):
    logic_uuid = ""
    if "online" in logic_name:
        logic_uuid = "7bb2898a-84e8-4605-aa5a-06e030fc24a3"
    elif "count" in logic_name:
        logic_uuid = "26e93c40-a143-4084-9b82-26bbe64002a7"

    body = {"uuid": logic_uuid, "agent_uuid": api.test_data["agent_uuid"]}
    resp = api.request_send(
        method="POST",
        path="/api/v2/logic/logic_unit/default",
        params=params,
        json=body,
    )
    if resp.status_code != 200:
        print(resp.status_code)
        raise Exception("Change logic error")
