# from random import randint
# import time
# import pytest
# import paramiko
# from test_3.fixture.api import APIClientV3
#
#
# def test_001(ssh_helper):
#     logic_pool_4 = ["10.129.2.71", "10.131.2.58", "10.129.2.83", "10.131.2.78", "10.129.2.55", "10.131.2.64",
#                     "10.129.2.77", "10.131.2.59", "10.129.2.6", "10.131.2.61", "10.129.2.43", "10.131.2.88",
#                     "10.129.2.78", "10.131.2.62", "10.129.2.62", "10.131.2.69", "10.129.2.85", "10.131.2.29",
#                     "10.129.2.68", "10.131.2.80", "10.129.2.81", "10.131.2.55", "10.129.2.95", "10.131.2.82",
#                     "10.129.2.15", "10.131.2.86", "10.129.2.75", "10.131.2.95", "10.129.2.66", "10.131.2.22",
#                     "10.129.2.65", "10.131.2.17", "10.129.2.63", "10.131.2.65", "10.129.2.41", "10.131.2.66",
#                     "10.129.2.20", "10.131.2.47", "10.129.2.69", "10.131.2.83", "10.129.2.57", "10.131.2.57",
#                     "10.129.2.28", "10.131.2.90", "10.129.2.31", "10.131.2.85", "10.129.2.73", "10.131.2.67",
#                     "10.129.2.86"]
#     # "10.131.2.77"
#
#     media_server_pool_4 = ["10.131.1.34", "10.129.1.93", "10.131.1.50", "10.129.1.73", "10.131.1.14", "10.129.1.48",
#                            "10.129.1.27", "10.131.1.72", "10.129.1.85", "10.131.1.83", "10.129.1.47", "10.131.1.56",
#                            "10.129.1.92", "10.131.1.80", "10.129.1.10", "10.131.1.39", "10.129.1.15", "10.131.1.41",
#                            "10.129.1.91", "10.131.1.28", "10.129.1.63", "10.131.1.70", "10.129.1.97", "10.131.1.53",
#                            "10.129.1.54", "10.131.1.87", "10.129.1.77", "10.131.1.18", "10.129.1.71", "10.131.1.81",
#                            "10.129.1.13", "10.131.1.94", "10.129.1.32", "10.129.1.7", "10.131.1.54", "10.129.1.75",
#                            "10.131.1.74", "10.129.1.59", "10.131.1.76", "10.131.1.19", "10.129.1.4", "10.131.1.63",
#                            "10.129.1.64", "10.131.1.92", "10.129.1.82", "10.131.1.69", "10.129.1.83", "10.131.1.15",
#                            "10.129.1.26", "10.131.1.52"]
#     # print(len(media_server_pool_4))
#     for hots in logic_pool_4:
#         client = ssh_helper.client(host=hots)
#         # res = client.exec_command("sudo systemctl stop logic-executor-online.service")
#         res = client.exec_command("sudo systemctl restart logic-executor-online.service")
#         # res = client.exec_command("sudo docker ps")
#         # res = client.exec_command(
#         #     "cat /var/log/ivr/media-server.log | grep '818ea0e4-a0d5-480e-b1d9-e3e0d32180b8'")
#         res_end = str((res[1].read() + res[2].read()), encoding="utf-8")
#         print('*' * 100)
#         print(hots)
#         print(res_end)
#
#         client.close()
#
#
# def test_load_le_online(api_v3, db):
#     params = api_v3.test_data['data_release_run']['agent_uuid']
#     change_default_logic(api_v3, params, "online")
#     response = api_v3.init_dialog(
#         msisdn="55555",
#         agent="release",
#         api=api_v3,
#         default_logic=False
#     )
#     dialog_uuid = response.json()['dialog_uuid']
#     print(dialog_uuid)
#     # dialog_uuid = "61e1431b-8c9a-4178-9476-2766ea3e1fc6"
#
#     command = f"SELECT result FROM dialog WHERE uuid = '{dialog_uuid}'"
#     timeout = time.time() + 30000
#     while True:
#         res = db.db_conn(command)
#         if len(res) > 0 and res[0][0] == 'done':
#             break
#         if time.time() >= timeout:
#             raise TimeoutError
#
#     dialog_id = db.select_data(table='dialog', column='uuid', sdata='id', data=str(dialog_uuid))[0][0]
#
#     result = db.db_conn(
#         f"select action, name, data  from dialog_stats where dialog_id = '{dialog_id}' and data is not null")
#     for i in result:
#
#         if 'log' in i[0]:
#             print('\n', i)
#
#
# def test_load_le_online_count(api_v3, db, clear_queue_new):
#     params = api_v3.test_data['data_release_run']['agent_uuid']
#     # change_default_logic(api_v3, params, "count")
#
#     api_v3.request_send(
#         method="PUT",
#         path=api_v3.path_end_point["put_change_agent_settings"],
#         json={"total_channel_limit": 23},
#         params={"agent_uuid": params},
#     )
#
#     data = []
#     for i in range(60):
#         data.append(
#             {'msisdn': "55555",
#              "script_entry_point": "main",
#              "script_name": "test_release"})
#     response = api_v3.request_send(method='POST',
#                                    path=api_v3.path_end_point['upload_group_dialogs'],
#                                    params={'agent_uuid': params},
#                                    json=data,
#                                    status_code=409)
#     print(response.text)
#     if response.status_code not in [200, 201, 202, 203, 204]:
#         raise Exception('Upload group dialog error')
#
#     agent_id = api_v3.test_data['data_release_run']['agent_id']
#     timeout = time.time() + 900
#     while True:
#         result = db.db_conn(f"SELECT count(id) from call where agent_id ='{agent_id}' and result = 'pending' ")
#         print(time.time(), ' Активных звонков - ', result[0][0])
#
#         time.sleep(1)
#         if time.time() >= timeout:
#             break
#
#
# @pytest.fixture()
# def clear_queue_new(request, api_v3, pool_api_v3):
#     def clear():
#         params_agent_uuid = {"agent_uuid": api_v3.test_data['data_release_run']['agent_uuid']}
#         api_v3.request_send(
#             method="PUT",
#             path=api_v3.path_end_point["put_change_agent_settings"],
#             json={"total_channel_limit": 8},
#             params=params_agent_uuid,
#         )
#
#         api_v3.request_send(method='POST',
#                             path=api_v3.path_end_point['return_queue_dialogs'],
#                             params=params_agent_uuid,
#                             json={},
#                             status_code=409)
#         api_v3.request_send(method='POST',
#                             path=api_v3.path_end_point['remove_queue_dialogs'],
#                             params=params_agent_uuid,
#                             status_code=409)
#
#         pool_api_v3.request_send(method='POST',
#                                  path=pool_api_v3.path_end_point['return_calls'],
#                                  params=params_agent_uuid,
#                                  json={})
#         pool_api_v3.request_send(method='DELETE',
#                                  path=pool_api_v3.path_end_point['get_list_queue_calls'],
#                                  params=params_agent_uuid,
#                                  json={})
#
#     request.addfinalizer(clear)
#
#
# def change_default_logic(api: APIClientV3, params, logic_name):
#     logic_uuid = ""
#     if "online" in logic_name:
#         logic_uuid = "7bb2898a-84e8-4605-aa5a-06e030fc24a3"
#     elif "count" in logic_name:
#         logic_uuid = "26e93c40-a143-4084-9b82-26bbe64002a7"
#
#     body = {"uuid": logic_uuid, "agent_uuid": api.test_data["agent_uuid"]}
#     resp = api.request_send(
#         method="POST",
#         path="/api/v2/logic/logic_unit/default",
#         params=params,
#         json=body,
#     )
#     if resp.status_code != 200:
#         print(resp.status_code)
#         raise Exception("Change logic error")


