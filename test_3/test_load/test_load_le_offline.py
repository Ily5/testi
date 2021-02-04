import time
import paramiko


def test_load_logic_offline(api_v3, pool_api_v3, creation_queue_dialog, params_agent_uuid):
    path = pool_api_v3.path_end_point['get_all_dialog_queue']
    params = {**{"page": "1",
                 "by_count": "10000"}, **params_agent_uuid}
    response_before = pool_api_v3.request_send(path=path, params=params)
    print('\n--(Before)--', response_before.json())
    print('\n--(Количество диалогов до)-- ', response_before.json()['total'])

    path_agent_setting = api_v3.path_end_point['put_change_agent_settings']
    res = api_v3.request_send(method="PUT", path=path_agent_setting, json={'total_channel_limit': 100000},
                              params=params_agent_uuid)
    print('Поменяли TCL на ', res.json()['total_channel_limit'])

    # total = api_v3.request_send(path=api_v3.path_end_point['get_agent_settings'], params=params_agent_uuid).json()
    # print(total['total_channel_limit'])

    set_dialogs_status = set()
    while True:
        resp = pool_api_v3.request_send(path=path, params=params)
        for dialog in resp.json()['dialogs']:
            set_dialogs_status.add(dialog['result'])
        if 'queued' in set_dialogs_status:
            break

    count = 0
    time_out = time.time() + 60
    print('Отчет времени старт')
    while True:
        count += 1
        print(count, '  --- ', time.time(), '  --- ', time_out)
        time.sleep(1)

        if time.time() >= time_out:
            print('Отчет времени стоп')
            break


def check_log():
    host = '10.131.0.60'
    user = 'rdevetiarov'
    my_key = '/home/renat/.ssh/id_rsa.pub'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user)
    result = client.exec_command("cat /var/log/ivr/logic-executor-offline.log | grep 'creating outbound call' | wc -l")
    before = result[1].read()
    print(before)

    result = client.exec_command('tail -n 10  /var/log/ivr/logic-executor-offline.log')
    data = result[1].read() + result[2].read()
    print(data)
    client.close()


check_log()
