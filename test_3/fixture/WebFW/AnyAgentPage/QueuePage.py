import time
import allure
from test_3.fixture.WebFW.AgentPage import AnyAgentPage


class QueuePage(AnyAgentPage):
    __dialogs_queue = ''
    __remove_all_dialogs_button = ''
    __refresh_dialogs_queue_button = ''
    __popup_menu_dialogs_queue_button = ''
    __stop_all_dialogs_button = ''
    __run_all_dialogs_button = ''

    __base_sorting_menu_dialogs = ''
    __dialog_sorting_button_dialogs = __base_sorting_menu_dialogs + ''
    __status_sorting_button_dialogs = __base_sorting_menu_dialogs + ''
    __adding_time_sorting_button_dialogs = __base_sorting_menu_dialogs + ''
    __processing_time_sorting_button_dialogs = __base_sorting_menu_dialogs + ''
    __action_sorting_button_dialogs = __base_sorting_menu_dialogs + ''

    __calls_queue = ''
    __refresh_calls_queue_button = ''

    __base_sorting_menu_calls = ''
    __dialog_sorting_button_calls = __base_sorting_menu_calls + ''
    __status_sorting_button_calls = __base_sorting_menu_calls + ''
    __adding_time_sorting_button_calls = __base_sorting_menu_calls + ''
    __processing_time_sorting_button_calls = __base_sorting_menu_calls + ''
    __action_sorting_button_calls = __base_sorting_menu_calls + ''
    __contact_sorting_button_calls = __base_sorting_menu_calls + ''

    @allure.step('Открытие вкладики Dialogs')
    def open_dialogs_queue(self):
        self.click_by_xpath(self.__dialogs_queue)

    @allure.step('Удалить все диалоги')
    def remove_all_dialogs(self):
        self.open_dialogs_queue()
        self.click_by_xpath(self.__remove_all_dialogs_button)

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
        if column.lower() == 'dialogs':
            self.click_by_xpath(self.__dialog_sorting_button_dialogs)
        if column.lower() == 'status':
            self.click_by_xpath(self.__status_sorting_button_dialogs)
        if column.lower() == 'adding_time':
            self.click_by_xpath(self.__adding_time_sorting_button_dialogs)
        if column.lower() == 'processing_time':
            self.click_by_xpath(self.__processing_time_sorting_button_dialogs)
        if column.lower() == 'action':
            self.click_by_xpath(self.__action_sorting_button_dialogs)

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
            self.click_by_xpath(self.__dialog_sorting_button_calls)
        # todo завести баг, что не правильно назван столбец
        if column.lower() == 'status':
            self.click_by_xpath(self.__status_sorting_button_calls)
        if column.lower() == 'adding_time':
            self.click_by_xpath(self.__adding_time_sorting_button_calls)
        if column.lower() == 'processing_time':
            self.click_by_xpath(self.__processing_time_sorting_button_calls)
        if column.lower() == 'action':
            self.click_by_xpath(self.__action_sorting_button_calls)
