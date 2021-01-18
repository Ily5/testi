import time
import allure
from test_3.fixture.WebFW.AgentPage import AnyAgentPage


class QueuePage(AnyAgentPage):
    __dialogs_queue = '//div[text()="dialogs"]'
    __remove_all_dialogs_button = '//span[text()=" remove all dialogs "]/..'
    __refresh_dialogs_queue_button = '//span[text()=" remove all dialogs "]/../../button[3]'
    __popup_menu_dialogs_queue_button = '//span[text()=" remove all dialogs "]/../../button[2]'
    __stop_all_dialogs_button = '//div[contains(text(),"stop all dialogs ")]'
    __run_all_dialogs_button = '//div[contains(text(),"run all dialogs ")]'
    __all_dialogs_list = '//div[@class="ag-center-cols-container"]'

    __base_sorting_menu = '//div[@class="ag-header-row"]/div'
    __dialog_sorting_button = __base_sorting_menu + '//span[text()="dialog"]'
    __status_sorting_button = __base_sorting_menu + '//span[text()="status"]'
    __adding_time_sorting_button = __base_sorting_menu + '//span[text()="adding time"]'
    __processing_time_sorting_button = __base_sorting_menu + '//span[text()="processing time"]'
    __action_sorting_button = __base_sorting_menu + '//span[text()="action"]'

    __calls_queue = '//div[text()="calls"]'
    __refresh_calls_queue_button = '//div[@fxlayoutalign="end center"]/button'

    __contact_sorting_button_calls = __base_sorting_menu + '//span[text()="contact"]'

    @allure.step('Открытие вкладики Dialogs')
    def open_dialogs_queue(self):
        self.click_by_xpath(self.__dialogs_queue)

    @allure.step('Удалить все диалоги')
    def remove_all_dialogs(self):
        self.open_dialogs_queue()
        self.click_by_xpath(self.__remove_all_dialogs_button)

    @allure.step('Удалить/поставить на паузу/вернуть с паузы n-ый по счету диалог')
    def action_n_dialog(self, number, action: str):
        self.open_dialogs_queue()
        _n_dialog = self.__all_dialogs_list + '/div[@row-id="{}"]'.format(number)
        if action.lower() == 'remove':
            _locator = _n_dialog + '//app-queue-cell-actions/button[2]'
            self.click_by_xpath(_locator)
        if action.lower() == 'pause':
            _locator = _n_dialog + '//app-queue-cell-actions/button[1]'
            self.click_by_xpath(_locator)
        if action.lower() == 'return':
            _locator = _n_dialog + '//app-queue-cell-actions/button[1]'
            self.click_by_xpath(_locator)
        self.refresh_dialogs_queue_list()

    @allure.step('Получить данные n-ого по счету диалогу')
    def get_n_dialog_info(self, number):
        self.open_dialogs_queue()
        _n_dialog = self.__all_dialogs_list + '/div[@row-id="{}"]'.format(number)
        _msisdn = _n_dialog + '/div[@col-id="msisdn"]//div[contains(@class, "app-full")]/span'
        _status = _n_dialog + '/div[@col-id="0"]//div[contains(@class, "app-status")]'
        msisdn = self.get_tag_text(_msisdn)
        status = self.get_tag_text(_status)
        return {"msisdn": msisdn, "status": status}

    @allure.step('Обновить список диалогов в очереди')
    def refresh_dialogs_queue_list(self):
        self.open_dialogs_queue()
        self.click_by_xpath(self.__refresh_dialogs_queue_button)

    @allure.step('Открытие меню действий с очередью диалогов')
    def open_popup_menu_dialogs_queue(self):
        self.open_dialogs_queue()
        self.click_by_xpath(self.__popup_menu_dialogs_queue_button)

    @allure.step('Поставить все диалоги на паузу')
    def stop_all_dialogs(self):
        self.open_dialogs_queue()
        self.open_popup_menu_dialogs_queue()
        self.click_by_xpath(self.__stop_all_dialogs_button)

    @allure.step('Вернуть все диалоги с паузы')
    def run_all_dialogs(self):
        self.open_dialogs_queue()
        self.open_popup_menu_dialogs_queue()
        self.click_by_xpath(self.__run_all_dialogs_button)

    @allure.step('Сортировка списка диалогов в очереди')
    def sorting_dialogs_queue_list(self, column: str):
        self.open_dialogs_queue()
        if column.lower() in 'dialogs':
            self.click_by_xpath(self.__dialog_sorting_button)
        if column.lower() in 'status':
            self.click_by_xpath(self.__status_sorting_button)
        if column.lower() in 'adding_time':
            self.click_by_xpath(self.__adding_time_sorting_button)
        if column.lower() in 'processing_time':
            self.click_by_xpath(self.__processing_time_sorting_button)
        if column.lower() in 'action':
            self.click_by_xpath(self.__action_sorting_button)

    @allure.step('Изменение количеста строк на странице очереди диалогов')
    def change_items_per_page_dialogs_queue(self):
        self.open_dialogs_queue()
        pass

    @allure.step('Открытие вкладики Calls')
    def open_calls_queue(self):
        self.click_by_xpath(self.__calls_queue)

    @allure.step('Обновить список звонок в очереди')
    def refresh_calls_queue_list(self):
        self.open_calls_queue()
        self.click_by_xpath(self.__refresh_calls_queue_button)

    @allure.step('Сортировка списка звонок в очереди')
    def sorting_calls_queue_list(self, column: str):
        self.open_dialogs_queue()
        if column.lower() == 'contact':
            self.click_by_xpath(self.__contact_sorting_button_calls)
        if column.lower() == 'dialogs':
            self.click_by_xpath(self.__dialog_sorting_button)
        if column.lower() == 'status':
            self.click_by_xpath(self.__status_sorting_button)
        if column.lower() == 'adding_time':
            self.click_by_xpath(self.__adding_time_sorting_button)
        if column.lower() == 'processing_time':
            self.click_by_xpath(self.__processing_time_sorting_button)
        if column.lower() == 'action':
            self.click_by_xpath(self.__action_sorting_button)

    @allure.step('Удалить/поставить на паузу/вернуть n-ый по списку звонок')
    def action_n_call(self, number, action: str):
        self.open_calls_queue()
        _n_call = self.__all_dialogs_list + '/div[@row-id="{}"]'.format(number)
        if action.lower() == 'remove':
            _locator = _n_call + '//app-queue-cell-actions/button[2]'
            self.click_by_xpath(_locator)
        if action.lower() == 'pause':
            _locator = _n_call + '//app-queue-cell-actions/button[1]'
            self.click_by_xpath(_locator)
        if action.lower() == 'return':
            _locator = _n_call + '//app-queue-cell-actions/button[1]'
            self.click_by_xpath(_locator)

    @allure.step('Получить данные n-ого по счету звонку')
    def get_n_dialog_info(self, number):
        self.open_dialogs_queue()
        _n_dialog = self.__all_dialogs_list + '/div[@row-id="{}"]'.format(number)
        _msisdn = _n_dialog + '/div[@col-id="msisdn"]//div[contains(@class, "app-full")]/span'
        _status = _n_dialog + '/div[@col-id="result"]//div[contains(@class, "app-status")]'
        _adding_time = _n_dialog + '/div[@col-id="date_added"]//div[contains(@class, "app-full")]/span'
        msisdn = self.get_tag_text(_msisdn)
        status = self.get_tag_text(_status)
        adding_time = self.get_tag_text(_adding_time)
        return {"msisdn": msisdn, "status": status, "adding_time": adding_time}
