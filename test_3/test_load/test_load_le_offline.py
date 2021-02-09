import time
import paramiko

count_before = ''


class TestLeOfflineLoad:

    def test_load_logic_offline(self, api_v3, pool_api_v3, creation_queue_dialog, params_agent_uuid):
        path = pool_api_v3.path_end_point['get_all_dialog_queue']
        params = {**{"page": "1",
                     "by_count": "10000"}, **params_agent_uuid}
        response_before = pool_api_v3.request_send(path=path, params=params)
        # print('\n--(Before)--', response_before.json())
        print('\n--(Количество диалогов до)-- ', response_before.json()['total'])

        path_agent_setting = api_v3.path_end_point['put_change_agent_settings']
        res = api_v3.request_send(method="PUT", path=path_agent_setting, json={'total_channel_limit': 100000},
                                  params=params_agent_uuid)
        print('Поменяли TCL на ', res.json()['total_channel_limit'])

        set_dialogs_status = set()
        print('Ждем пока диалоги начнут вставтаь в очередь')
        while True:
            resp = pool_api_v3.request_send(path=path, params=params)
            for dialog in resp.json()['dialogs']:
                set_dialogs_status.add(dialog['result'])
            # print('\nСтатусы диалогов в очереди', set_dialogs_status)
            if 'queued' in set_dialogs_status:
                print('Диалоги начали вставать в очередь')
                break

        global count_before
        count_before = check_log(when='before', server_id='1', user='rdevetiarov',
                                 log_name='logic-executor-offline.log')

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


def test_le_offline_result():
    global count_before
    count_after = check_log(when='after', server_id='1', user='rdevetiarov', log_name='logic-executor-offline.log')
    print('\n', count_before)
    print('\n', count_after)
    print('\n Диалогов выполнено', count_after - int(count_before))


def check_log(when: str, user: str, **kwargs):
    # host = None
    if kwargs['server_id'] == '1':
        host = '10.129.0.108'
    elif kwargs['server_id'] == '2':
        host = '10.131.0.60'
    else:
        raise Exception('server id must be 1 or 2')
    # host = '10.131.0.60'
    # user = 'rdevetiarov'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user)

    result = client.exec_command(
        f"cat /var/log/ivr/{kwargs['log_name']} |  grep 'NluDialogOffline.main_logic] end' | wc -l")
    count_result = int(str(result[1].read())[2:-3])
    if when.lower() in 'before':
        print('Ждем активности в логах LE Offline')
        try:
            while True:
                result = client.exec_command(f'tail -n 2  /var/log/ivr/{kwargs["log_name"]}')
                data = result[1].read() + result[2].read()
                result_new = client.exec_command(f'tail -n 2  /var/log/ivr/{kwargs["log_name"]}')
                data_new = result_new[1].read() + result_new[2].read()
                if data != data_new:
                    print('LE Offline начал обработку диалогов')
                    break
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        finally:
            client.close()
    else:
        client.close()
    return count_result


