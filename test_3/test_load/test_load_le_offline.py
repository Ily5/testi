import time


def test_load_logic_offline(api_v3, pool_api_v3, creation_queue_dialog, params_agent_uuid):
    path = pool_api_v3.path_end_point['get_all_dialog_queue']
    params = {**{"page": "1",
                 "by_count": "10000"}, **params_agent_uuid}
    response_before = pool_api_v3.request_send(path=path, params=params)
    print('\n--(Before)--', response_before.json())
    print('\n--(Количество диалогов до)-- ', response_before.json()['total'])

    path_agent_setting = api_v3.path_end_point['put_change_agent_settings']
    api_v3.request_send(method="PUT", path=path_agent_setting, json={'total_channel_limit': 1000000},
                        params=params_agent_uuid)
    time_out = time.time() + 60

    calls_uuid_set = set()
    while True:
        response_calls = pool_api_v3.request_send(path=pool_api_v3.path_end_point['get_list_queue_calls'],
                                                  params=params).json()['calls']
        for call in response_calls:
            if call['uuid'] not in calls_uuid_set:
                calls_uuid_set.add(call['uuid'])

        if time.time() >= time_out:
            response_after = pool_api_v3.request_send(path=path, params=params)
            print('\n--(After)--', response_after.json())

            print('\n--(Количество диалогов после)-- ', response_after.json()['total'])

            response_1 = pool_api_v3.request_send(path=pool_api_v3.path_end_point['get_list_queue_calls'],
                                                  params=params)
            print('\n --(calls)--', response_1.json())
            for call in response_1.json()['calls']:
                if call['uuid'] not in calls_uuid_set:
                    calls_uuid_set.add(call['uuid'])

            break
    print('\n--(Len calls)--', len(calls_uuid_set))


def test_01(params_agent_uuid, pool_api_v3, api_v3):
    while True:
        time.sleep(50)
        path = pool_api_v3.path_end_point['get_all_dialog_queue']
        params = {**{"page": "1",
                     "by_count": "100"}, **params_agent_uuid}
        response = pool_api_v3.request_send(path=path, params=params)
        print('\n--(2)--', response.json()['total'])
        # response_1 = pool_api_v3.request_send(path=pool_api_v3.path_end_point['get_list_queue_calls'],
        #                                       params=params)
        # print('\n --(calls)--', response_1.json())
        if response.json()['total'] > 5000:
            api_v3.request_send(method='POST', path=api_v3.path_end_point['remove_queue_dialogs'],
                                params=params_agent_uuid,
                                status_code=409)

