import time
import datetime
import allure
import pytest


@allure.epic('UI Regression')
@allure.feature('Queue Dialogs')
class TestDialogsQueue:

    @allure.title('Фильтрация списка диалогов по Dialog, валидное значение')
    def test_dialogs_queue_filter_by_dialog_valid(self, creation_queue_dialog, queue_page, cancel_filter_queue):
        msisdn = queue_page.get_queue_info(number='3')['msisdn']
        queue_page.filter_dialogs_calls_queue_list(param='dialog', text=msisdn)
        assert int(queue_page.get_count_list_dialogs_and_calls()) == 1
        assert queue_page.get_queue_info()['1']['msisdn'] == msisdn

    @allure.title('Фильтрация списка диалогов по Dialog, невалидное значение')
    def test_dialogs_queue_filter_by_dialog_no_valid(self, creation_queue_dialog, queue_page, random_str_generator,
                                                     cancel_filter_queue):
        msisdn = random_str_generator
        queue_page.filter_dialogs_calls_queue_list(param='dialog', text=msisdn)
        assert queue_page.get_count_list_dialogs_and_calls() == 0

    # @pytest.mark.skip(reason='https://neuronet.atlassian.net/browse/NP-1803')
    @allure.title('Фильтрация списка диалогов по Status, валидное значение')
    def test_dialogs_queue_filter_by_status_valid(self, creation_queue_dialog, queue_page, cancel_filter_queue):
        status = queue_page.get_queue_info(number='1')['status']
        if 'queue' in status.lower():
            status = 'queued'
        queue_page.filter_dialogs_calls_queue_list(param='status', text=status.lower())
        if 'created' in status.lower():
            assert queue_page.get_count_list_dialogs_and_calls() >= 0
        else:
            assert queue_page.get_count_list_dialogs_and_calls() > 0
        stats = queue_page.get_queue_info()
        for item in stats.values():
            assert item['status'].lower() == status.lower()

    # @pytest.mark.skip(reason='https://neuronet.atlassian.net/browse/NP-1803')
    @allure.title('Фильтрация списка диалогов по Status, невалидное значение')
    def test_dialogs_queue_filter_by_status_no_valid(self, creation_queue_dialog, queue_page, random_str_generator,
                                                     cancel_filter_queue):
        status = random_str_generator
        queue_page.filter_dialogs_calls_queue_list(param='status', text=status)
        assert queue_page.get_count_list_dialogs_and_calls() == 0

    @allure.title('Удалить один диалог из списка')
    def test_dialogs_queue_remove_one_dialog(self, creation_queue_dialog, queue_page):
        dialogs_count = queue_page.get_count_list_dialogs_and_calls()
        queue_page.action_n_dialog_or_call('dialogs', '1', 'remove')
        queue_page.get_dialogs_queue_list()
        dialogs_count_new = queue_page.get_count_list_dialogs_and_calls()
        assert int(dialogs_count) == int(dialogs_count_new) + 1

    @allure.title('Сортировка диалогов по Status')
    def test_dialogs_queue_sorting_status(self, creation_queue_dialog, queue_page):
        queue_page.action_n_dialog_or_call('dialog', '1', 'pause')
        queue_page.sorting_queue_list(page='dialogs', column='status')
        first_before = queue_page.get_queue_info(number='1')['status']
        queue_page.sorting_queue_list(page='dialogs', column='status')
        first_after = queue_page.get_queue_info(number='1')['status']

        stat_dialog = queue_page.get_queue_info_for_msisdn_status(status='stopped')
        number = stat_dialog['number']
        queue_page.action_n_dialog_or_call('dialog', number, action='return')
        assert first_before != first_after

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
        count_dialogs = queue_page.get_count_list_dialogs_and_calls()
        assert count_dialogs == 0


@allure.epic('UI Regression')
@allure.feature('Queue Calls')
class TestCallsQueue:

    @allure.title('Сортировка списка звонков по Adding time')
    def test_calls_queue_sort_adding_time(self, creation_queue_calls, queue_page):
        queue_page.sorting_queue_list(page='calls', column='adding_time')
        stats_list = queue_page.get_queue_info(page='calls')
        msisdn_1 = stats_list['1']['msisdn']
        msisdn_2 = stats_list['4']['msisdn']
        assert msisdn_2 != msisdn_1

        queue_page.sorting_queue_list(page='calls', column='adding_time')
        stats_list_new = queue_page.get_queue_info(page='calls')
        msisdn_3 = stats_list_new['1']['msisdn']
        msisdn_4 = stats_list_new['4']['msisdn']
        assert msisdn_4 != msisdn_3

    # @pytest.mark.skip(reason='https://neuronet.atlassian.net/browse/NP-1781')
    @allure.title('Сортировка списка звонков по Status')
    def test_calls_queue_sort_status(self, creation_queue_calls, queue_page):
        queue_page.action_n_dialog_or_call('calls', '1', 'pause')
        queue_page.sorting_queue_list(page='calls', column='status')
        first_before = queue_page.get_queue_info(page='calls', number='1')['status']
        queue_page.sorting_queue_list(page='calls', column='status')
        first_after = queue_page.get_queue_info(page='calls', number='1')['status']

        stat_dialog = queue_page.get_queue_info_for_msisdn_status(page='calls', status='stopped')
        number = stat_dialog['number']
        queue_page.action_n_dialog_or_call('calls', number, action='return')
        assert first_before != first_after

    @allure.title('Фильтрация списка звонов по валидному Contact')
    def test_calls_queue_filter_by_contact_valid(self, creation_queue_calls, queue_page, cancel_filter_queue):
        msisdn = queue_page.get_queue_info(page='calls', number='3')['msisdn']
        queue_page.filter_dialogs_calls_queue_list(page='calls', param='contact', text=msisdn)
        assert int(queue_page.get_count_list_dialogs_and_calls(page='calls')) == 1
        assert queue_page.get_queue_info(page='calls')['1']['msisdn'] == msisdn

    @allure.title('Фильтрация списка звонов по невалидному Contact')
    def test_calls_queue_filter_by_contact_no_valid(self, creation_queue_calls, queue_page, cancel_filter_queue,
                                                    random_str_generator):
        msisdn = random_str_generator
        queue_page.filter_dialogs_calls_queue_list(page='calls', param='contact', text=msisdn)
        assert int(queue_page.get_count_list_dialogs_and_calls(page='calls')) == 0

    # @pytest.mark.skip(reason='https://neuronet.atlassian.net/browse/NP-1803')
    @allure.title('Фильтрация списка звонков по валидному Status')
    def test_calls_queue_filter_by_status_valid(self, creation_queue_calls, queue_page, cancel_filter_queue):
        status = queue_page.get_queue_info(page='calls', number='1')['status']
        queue_page.filter_dialogs_calls_queue_list(page='calls', param='status', text=status.lower())
        stats = queue_page.get_queue_info(page='calls')
        for item in stats.values():
            assert item['status'].lower() == status.lower()

    # @pytest.mark.skip(reason='https://neuronet.atlassian.net/browse/NP-1781')
    @allure.title('Фильтрация списка звонков по невалидному Status')
    def test_calls_queue_filter_by_status_no_valid(self, creation_queue_calls, queue_page, cancel_filter_queue,
                                                   random_str_generator):
        status = random_str_generator
        queue_page.filter_dialogs_calls_queue_list(page='calls', param='status', text=status)
        assert queue_page.get_count_list_dialogs_and_calls(page='calls') == 0

    # @pytest.mark.skip(reason='https://neuronet.atlassian.net/browse/NP-1781')
    @allure.title('Поставить на паузу один звонок')
    def test_calls_queue_pause_one_call(self, creation_queue_calls, queue_page):
        status_call = queue_page.get_queue_info(page='calls', number=3)
        queue_page.action_n_dialog_or_call(page='calls', number=3, action='pause')
        queue_page.get_call_queue_list()
        status_call_new = queue_page.get_queue_info_for_msisdn_status(page='calls', msisdn=status_call['msisdn'])
        assert status_call['status'] != status_call_new['status']
        assert str(status_call_new['status']).lower() == 'stopped'

    # @pytest.mark.skip(reason='https://neuronet.atlassian.net/browse/NP-1781')
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

    # @pytest.mark.skip(reason='https://neuronet.atlassian.net/browse/NP-1781')
    @allure.title('Удалить один звонок')
    def test_calls_queue_remove_one_call(self, creation_queue_calls, queue_page):
        count_calls_before = queue_page.get_count_list_dialogs_and_calls(page='calls')
        queue_page.action_n_dialog_or_call(page='calls', number=1, action='remove')
        count_calls_after = queue_page.get_count_list_dialogs_and_calls(page='calls')
        assert int(count_calls_before) > int(count_calls_after)

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
            assert status_calls[str(i + 1)]['status'].lower() != 'stopped'

    @allure.title('Удалить все звонки')
    def test_dialogs_queue_remove_all_dialogs(self, creation_queue_calls, queue_page):
        count_calls = queue_page.get_count_list_dialogs_and_calls(page='calls')
        queue_page.remove_all_dialogs_or_calls(page='calls')
        count_calls_after = queue_page.get_count_list_dialogs_and_calls(page='calls')
        assert count_calls > count_calls_after
        assert count_calls_after == 0
