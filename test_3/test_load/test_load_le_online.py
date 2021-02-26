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
    client = ssh_helper.client(host='10.129.0.108')
    res = client.exec_command('sudo systemctl restart caller.service')
    res_end = str((res[1].read() + res[2].read()), encoding='utf-8')
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
    5. Считаем количество вызовов функции (через логи или через декоратор в логике?) 
    
"""


def test_load_le_online(api_v3, params_agent_uuid):
    change_default_logic(api_v3, params_agent_uuid, 'online_max')
    api_v3.init_dialog(msisdn='55555', agent='release', api_v3=api_v3, params_agent_uuid=params_agent_uuid)


def change_default_logic(api_v3, params_agent_uuid, logic_name):
    logic_uuid = ''
    if 'online' in logic_name:
        logic_uuid = "85ddbc06-89c9-4b06-a5b2-359dfa950c61"
    elif 'count' in logic_name:
        logic_uuid = '2eef5758-1097-4b9c-85d8-f531e992b097'

    api_v3: APIClientV3
    body = {"uuid": logic_uuid, "agent_uuid": api_v3.test_data['agent_uuid']}
    resp = api_v3.request_send(method='POST', path="/api/v2/logic/logic_unit/default", params=params_agent_uuid,
                               json=body)
    if resp.status_code != 200:
        print(resp.status_code)
        raise Exception('Change logic error')
