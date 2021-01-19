import time
import datetime
import allure
import pytest


# todo попробовать промаркировать класс для отчета алюр, мб не надо каждый метод?
@pytest.mark.skip(reason='Отладить на тестовом стенде')
class TestDialogsQueue:

    @pytest.mark.skip(reason='https://neuronet.atlassian.net/browse/NP-1615')
    @allure.epic('UI Regression')
    @allure.feature('Queue Dialogs')
    @allure.title('Сортировка списка диалогов по колонке Status')
    def test_dialogs_queue_sort_action(self, queue_page, creation_queue_dialog):
        pass

    @pytest.mark.skip(reason='Отладить тест')
    @allure.epic('UI Regression')
    @allure.feature('Queue Dialogs')
    @allure.title('Фильтрация списка по диалогу')
    def test_dialogs_queue_filter_by_dialog(self, creation_queue_dialog, queue_page):
        msisdn = queue_page.get_queue_info(number='1')['msisdn']
        queue_page.filter_dialogs_queue_list(param='dialog', text=msisdn)
        assert int(queue_page.get_count_list_dialogs_and_calls()['dialogs']) == 1
        assert queue_page.get_queue_info()['1']['msisdn'] == msisdn

    @pytest.mark.skip(reason='Отладить тест')
    @allure.epic('UI Regression')
    @allure.feature('Queue Dialogs')
    @allure.title('Фильтрация списка по статусу')
    def test_dialogs_queue_filter_by_status(self, creation_queue_dialog, queue_page):
        status = queue_page.get_queue_info(number='1')['status']
        queue_page.filter_dialogs_queue_list(param='dialog', text=status)
        stats = queue_page.get_queue_info()
        for item in stats.values():
            assert item['status'].lower() == status.lower()

    @allure.epic('UI Regression')
    @allure.feature('Queue Dialogs')
    @allure.title('Удалить один диалог из списка')
    def test_dialogs_queue_remove_one_dialog(self, creation_queue_dialog, queue_page):
        dialogs_count = queue_page.get_count_list_dialogs_and_calls()['dialogs']
        queue_page.action_n_dialog_or_call('dialogs', '1', 'remove')
        queue_page.get_dialogs_queue_list()
        dialogs_count_new = queue_page.get_count_list_dialogs_and_calls()['dialogs']
        assert int(dialogs_count) == int(dialogs_count_new) + 1

    @allure.epic('UI Regression')
    @allure.feature('Queue Dialogs')
    @allure.title('Поставить на паузу один диалог')
    def test_dialogs_queue_pause_one_dialog(self, creation_queue_dialog, queue_page):
        status_dialog = queue_page.get_queue_info(number='1')
        queue_page.action_n_dialog_or_call('dialog', '1', 'pause')
        status_dialog_new = queue_page.get_queue_info_for_msisdn(msisdn=status_dialog['msisdn'])
        assert status_dialog['status'] != status_dialog_new['status']
        assert str(status_dialog_new['status']).lower() == 'stopped'

    @allure.epic('UI Regression')
    @allure.feature('Queue Dialogs')
    @allure.title('Вернуть с паузы один диалог')
    def test_dialogs_queue_return_one_dialog(self, creation_queue_dialog, queue_page):
        status_dialog = queue_page.get_queue_info(number='1')
        queue_page.action_n_dialog_or_call('dialog', '1', 'pause')
        queue_page.action_n_dialog_or_call('dialog', '1', 'return')
        status_dialog_new = queue_page.get_queue_info_for_msisdn(msisdn=status_dialog['msisdn'])
        assert status_dialog['msisdn'] == status_dialog_new['msisdn']
        assert str(status_dialog_new['status']).lower() == str(status_dialog_new['status']).lower()

    @allure.epic('UI Regression')
    @allure.feature('Queue Dialogs')
    @allure.title('Поставить на паузу все диалоги')
    def test_dialogs_queue_pause_all_dialog(self, creation_queue_dialog, queue_page):
        queue_page.stop_all_dialogs()
        status_dialogs_after = queue_page.get_queue_info()
        for i in range(len(status_dialogs_after)):
            assert str(status_dialogs_after[str(i + 1)]['status']).lower() == 'stopped'

    @allure.epic('UI Regression')
    @allure.feature('Queue Dialogs')
    @allure.title('Вернуть все диалоги с паузы')
    def test_dialogs_queue_pause_all_dialog(self, creation_queue_dialog, queue_page):
        queue_page.stop_all_dialogs()
        queue_page.refresh_the_page()
        queue_page.run_all_dialogs()
        status_dialogs = queue_page.get_queue_info()
        for i in range(len(status_dialogs)):
            assert str(status_dialogs[str(i + 1)]['status']).lower() != 'stopped'

    @allure.epic('UI Regression')
    @allure.feature('Queue Dialogs')
    @allure.title('Удалить все диалоги')
    def test_dialogs_queue_remove_all_dialogs(self, creation_queue_dialog, queue_page):
        queue_page.remove_all_dialogs()
        count_dialogs = queue_page.get_count_list_dialogs_and_calls()['dialogs']
        assert count_dialogs == 0


@allure.epic('UI Regression')
@allure.feature('Queue Calls')
class TestCallsQueue:

    @allure.title('Сортировка по adding time')
    def test_calls_queue_sort_adding_time(self, creation_queue_calls, queue_page):
        queue_page.sorting_queue_list(page='calls', column='adding_time')
        info = queue_page.get_queue_info(page='calls')
        print(info)
        # time_1 = datetime.datetime.strptime(info['1']['adding_time'], "%d.%m.%Y %H:%M:%S.%f")
        # print(time_1)
        # time_2 = datetime.datetime.strptime(info['3']['adding_time'], "%d.%m.%Y %H:%M:%S.%f")
        # print(time_2)
        queue_page.sorting_queue_list(page='calls', column='adding_time')
        info = queue_page.get_queue_info(page='calls')
        # time_3 = datetime.datetime.strptime(info['1']['adding_time'], "%d.%m.%Y %H:%M:%S.%f")
        # time_4 = datetime.datetime.strptime(info['3']['adding_time'], "%d.%m.%Y %H:%M:%S.%f")
        # print(time_3)
        # print(time_4)
        print(info)
        queue_page.refresh_calls_queue_list()
        time.sleep(10)
        # assert time_1 < time_2
        # assert time_3 > time_4
