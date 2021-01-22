import time
import datetime
import allure
import pytest


@allure.epic('UI Regression')
@allure.feature('Queue Dialogs')
class TestDialogsQueue:

    @allure.title('Сортировка списка диалогов по Status')
    def test_dialogs_queue_sort_status(self, creation_queue_dialog, queue_page):
        pass

    @pytest.mark.skip(reason='Реализуется в https://neuronet.atlassian.net/browse/NP-688')
    @allure.title('Фильтрация списка диалогов по Dialog')
    def test_dialogs_queue_filter_by_dialog(self, creation_queue_dialog, queue_page):
        msisdn = queue_page.get_queue_info(number='1')['msisdn']
        queue_page.filter_dialogs_queue_list(param='dialog', text=msisdn)
        assert int(queue_page.get_count_list_dialogs_and_calls()['dialogs']) == 1
        assert queue_page.get_queue_info()['1']['msisdn'] == msisdn

    @pytest.mark.skip(reason='Реализуется в https://neuronet.atlassian.net/browse/NP-688')
    @allure.title('Фильтрация списка диалогов по Status')
    def test_dialogs_queue_filter_by_status(self, creation_queue_dialog, queue_page):
        status = queue_page.get_queue_info(number='1')['status']
        queue_page.filter_dialogs_queue_list(param='dialog', text=status)
        stats = queue_page.get_queue_info()
        for item in stats.values():
            assert item['status'].lower() == status.lower()

    @allure.title('Удалить один диалог из списка')
    def test_dialogs_queue_remove_one_dialog(self, creation_queue_dialog, queue_page):
        dialogs_count = queue_page.get_count_list_dialogs_and_calls()['dialogs']
        queue_page.action_n_dialog_or_call('dialogs', '1', 'remove')
        queue_page.get_dialogs_queue_list()
        dialogs_count_new = queue_page.get_count_list_dialogs_and_calls()['dialogs']
        assert int(dialogs_count) == int(dialogs_count_new) + 1

    @allure.title('Поставить на паузу один диалог')
    def test_dialogs_queue_pause_one_dialog(self, creation_queue_dialog, queue_page):
        status_dialog = queue_page.get_queue_info(number='1')
        queue_page.action_n_dialog_or_call('dialog', '1', 'pause')
        # status_dialog = queue_page.get_queue_info_for_msisdn_status(status='stopped')
        status_dialog_new = queue_page.get_queue_info_for_msisdn_status(msisdn=status_dialog['msisdn'])
        assert status_dialog['status'] != status_dialog_new['status']
        assert str(status_dialog_new['status']).lower() == 'stopped'

    @allure.title('Вернуть с паузы один диалог')
    def test_dialogs_queue_return_one_dialog(self, creation_queue_dialog, queue_page):

        stat_dialog = queue_page.get_queue_info_for_msisdn_status(status='stopped')
        if stat_dialog is None:
            queue_page.action_n_dialog_or_call('dialog', '1', 'pause')

        stat_dialog = queue_page.get_queue_info_for_msisdn_status(status='stopped')
        number = stat_dialog['number']
        queue_page.action_n_dialog_or_call('dialog', number, action='return')
        status_dialog_new = queue_page.get_queue_info_for_msisdn_status(msisdn=stat_dialog['msisdn'])
        assert status_dialog_new['msisdn'] == stat_dialog['msisdn']
        assert status_dialog_new['status'].lower() != 'stopped'

    @allure.title('Поставить на паузу все диалоги')
    def test_dialogs_queue_pause_all_dialog(self, creation_queue_dialog, queue_page):
        queue_page.stop_all_dialogs_or_calls()
        status_dialogs_after = queue_page.get_queue_info()
        for i in range(len(status_dialogs_after)):
            assert str(status_dialogs_after[str(i + 1)]['status']).lower() == 'stopped'

    @allure.title('Вернуть все диалоги с паузы')
    def test_dialogs_queue_return_all_dialog(self, creation_queue_dialog, queue_page):
        queue_page.stop_all_dialogs_or_calls()
        queue_page.get_dialogs_queue_list()
        queue_page.run_all_dialogs_or_calls()
        status_dialogs = queue_page.get_queue_info()
        for i in range(len(status_dialogs)):
            assert str(status_dialogs[str(i + 1)]['status']).lower() != 'stopped'

    @allure.title('Удалить все диалоги')
    def test_dialogs_queue_remove_all_dialogs(self, creation_queue_dialog, queue_page):
        queue_page.remove_all_dialogs_or_calls()
        count_dialogs = queue_page.get_count_list_dialogs_and_calls()['dialogs']
        assert count_dialogs == 0


@allure.epic('UI Regression')
@allure.feature('Queue Calls')
class TestCallsQueue:

    @allure.title('Сортировка списка звонков по Adding time')
    def test_calls_queue_sort_adding_time(self, creation_queue_calls, queue_page):
        queue_page.sorting_queue_list(page='calls', column='adding_time')
        stats_list = queue_page.get_queue_info(page='calls')
        time_1 = datetime.datetime.strptime(stats_list['1']['adding_time'], "%d.%m.%Y %H:%M:%S.%f")
        time_2 = datetime.datetime.strptime(stats_list['6']['adding_time'], "%d.%m.%Y %H:%M:%S.%f")

        queue_page.sorting_queue_list(page='calls', column='adding_time')
        stats_list_new = queue_page.get_queue_info(page='calls')
        time_3 = datetime.datetime.strptime(stats_list_new['1']['adding_time'], "%d.%m.%Y %H:%M:%S.%f")
        time_4 = datetime.datetime.strptime(stats_list_new['6']['adding_time'], "%d.%m.%Y %H:%M:%S.%f")

        assert time_1 < time_2
        assert time_3 > time_4

    @allure.title('Сортировка списка звонков по Status')
    def test_calls_queue_sort_status(self, creation_queue_calls, queue_page):
        pass

    @pytest.mark.skip(reason='Реализуется в https://neuronet.atlassian.net/browse/NP-688')
    @allure.title('Фильтрация списка звонов по Dialog')
    def test_calls_queue_filter_by_dialog(self, creation_queue_calls, queue_page):
        msisdn = queue_page.get_queue_info(number='1')['msisdn']
        queue_page.filter_dialogs_queue_list(param='dialog', text=msisdn)
        assert int(queue_page.get_count_list_dialogs_and_calls()['dialogs']) == 1
        assert queue_page.get_queue_info()['1']['msisdn'] == msisdn

    @pytest.mark.skip(reason='Реализуется в https://neuronet.atlassian.net/browse/NP-688')
    @allure.title('Фильтрация списка зковнов по Status')
    def test_calls_queue_filter_by_status(self, creation_queue_dialog, queue_page):
        status = queue_page.get_queue_info(number='1')['status']
        queue_page.filter_dialogs_queue_list(param='dialog', text=status)
        stats = queue_page.get_queue_info()
        for item in stats.values():
            assert item['status'].lower() == status.lower()

    @allure.title('Поставить на паузу один звонок')
    def test_calls_queue_pause_one_call(self, creation_queue_calls, queue_page):
        status_call = queue_page.get_queue_info(page='calls', number=3)
        queue_page.action_n_dialog_or_call(page='calls', number=3, action='pause')
        queue_page.get_call_queue_list()
        status_call_new = queue_page.get_queue_info_for_msisdn_status(page='calls', msisdn=status_call['msisdn'])
        assert status_call['status'] != status_call_new['status']
        assert str(status_call_new['status']).lower() == 'stopped'

    @allure.title('Вернуть с паузы один звонок')
    def test_calls_queue_return_one_call(self, creation_queue_calls, queue_page):
        stat_call = queue_page.get_queue_info_for_msisdn_status(page='calls', status='stopped')
        if stat_call is None:
            queue_page.action_n_dialog_or_call('calls', '1', 'pause')

        stat_call = queue_page.get_queue_info_for_msisdn_status(status='stopped', page='calls')
        number = stat_call['number']
        queue_page.action_n_dialog_or_call('calls', number, action='return')
        status_dialog_new = queue_page.get_queue_info_for_msisdn_status(msisdn=stat_call['msisdn'], page='calls')
        assert status_dialog_new['msisdn'] == stat_call['msisdn']
        assert status_dialog_new['status'].lower() != 'stopped'

    @allure.title('Удалить один звонок')
    def test_calls_queue_remove_one_call(self, creation_queue_calls, queue_page):
        count_calls_before = queue_page.get_count_list_dialogs_and_calls()['calls']
        queue_page.action_n_dialog_or_call(page='calls', number=1, action='remove')
        count_calls_after = queue_page.get_count_list_dialogs_and_calls()['calls']
        assert int(count_calls_before) < int(count_calls_after)

    @allure.title('Поставить на паузу все звонки')
    def test_calls_queue_pause_all_calls(self, creation_queue_calls, queue_page):
        queue_page.stop_all_dialogs_or_calls(page='calls')
        status_calls_after = queue_page.get_queue_info(page='calls')
        for i in range(len(status_calls_after)):
            assert str(status_calls_after[str(i + 1)]['status']).lower() == 'stopped'

    @allure.title('Вернуть все звонки с паузы')
    def test_calls_queue_return_all_calls(self, creation_queue_calls, queue_page):
        queue_page.stop_all_dialogs_or_calls(page='calls')
        # queue_page.get_dialogs_queue_list()
        queue_page.run_all_dialogs_or_calls(page='calls')
        status_calls = queue_page.get_queue_info(page='calls')
        for i in range(len(status_calls)):
            assert str(status_calls[str(i + 1)]['status']).lower() != 'stopped'

    @allure.title('Удалить все звонки')
    def test_dialogs_queue_remove_all_dialogs(self, creation_queue_calls, queue_page):
        count_calls = queue_page.get_count_list_dialogs_and_calls()['calls']
        queue_page.remove_all_dialogs_or_calls(page='calls')
        count_calls_after = queue_page.get_count_list_dialogs_and_calls()['calls']
        assert count_calls > count_calls_after
        assert count_calls_after == 0
