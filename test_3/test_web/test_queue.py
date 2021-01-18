import time
import allure
import pytest


# todo попробовать промаркировать класс для отчета алюр, мб не надо каждый метод?
class TestDialogsQueue:

    @pytest.mark.skip(reason='https://neuronet.atlassian.net/browse/NP-1615')
    @allure.epic('UI Regression')
    @allure.feature('Queue page')
    @allure.title('Сортировка списка диалогов по колонке Dialog')
    def test_dialogs_queue_sort_dialog(self, agent_settings_page, creation_queue_dialog):
        agent_settings_page.AnyAgentPage.open_queue_page()
        msisdn_1 = agent_settings_page.QueuePage.get_queue_info(number='1')
        agent_settings_page.QueuePage.sorting_dialogs_queue_list(column='dialog')
        msisdn_2 = agent_settings_page.QueuePage.get_queue_info(number='1')
        agent_settings_page.QueuePage.sorting_dialogs_queue_list(column='dialog')
        msisdn_3 = agent_settings_page.QueuePage.get_queue_info(number='1')
        assert msisdn_3 != msisdn_2 != msisdn_1

    @pytest.mark.skip(reason='https://neuronet.atlassian.net/browse/NP-1615')
    @allure.epic('UI Regression')
    @allure.feature('Queue page')
    @allure.title('Сортировка списка диалогов по колонке Action')
    def test_dialogs_queue_sort_action(self, agent_settings_page, creation_queue_dialog):
        pass

    @allure.epic('UI Regression')
    @allure.feature('Queue page')
    @allure.title('Удалить один диалог из списка')
    def test_dialogs_queue_remove_one_dialog(self, creation_queue_dialog, queue_page):
        dialogs_count = queue_page.get_count_list_dialogs_and_calls()['dialogs']
        queue_page.action_n_dialog_or_call('dialogs', '1', 'remove')
        queue_page.refresh_dialogs_queue_list()
        dialogs_count_new = queue_page.get_count_list_dialogs_and_calls()['dialogs']
        assert int(dialogs_count) == int(dialogs_count_new) + 1

    @allure.epic('UI Regression')
    @allure.feature('Queue page')
    @allure.title('Поставить на паузу один диалог')
    def test_dialogs_queue_pause_one_dialog(self, creation_queue_dialog, queue_page):
        status_dialog = queue_page.get_queue_info(number='2')
        queue_page.action_n_dialog_or_call('dialog', '2', 'pause')
        queue_page.refresh_dialogs_queue_list()
        status_dialog_new = queue_page.get_queue_info_for_msisdn(msisdn=status_dialog['msisdn'])
        assert status_dialog['status'] != status_dialog_new['status']
        assert str(status_dialog_new['status']).lower() == 'stopped'

    @allure.epic('UI Regression')
    @allure.feature('Queue page')
    @allure.title('Вернуть с паузы один диалог')
    def test_dialogs_queue_return_one_dialog(self, creation_queue_dialog, queue_page):

        status_dialog = queue_page.get_queue_info(number='2')
        queue_page.action_n_dialog_or_call('dialog', '1', 'pause')
        queue_page.action_n_dialog_or_call('dialog', '1', 'return')
        status_dialog_new = queue_page.get_queue_info_for_msisdn(msisdn=status_dialog['msisdn'])
        assert status_dialog['msisdn'] == status_dialog_new['msisdn']
        assert str(status_dialog_new['status']).lower() == str(status_dialog_new['status']).lower()
