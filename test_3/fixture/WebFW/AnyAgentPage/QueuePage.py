import time
import allure
from test_3.fixture.WebFW.AgentPage import AnyAgentPage


class QueuePage(AnyAgentPage):
    __dialogs_queue = '//div[text()="dialogs"]'
    __refresh_dialogs_queue_button = '//span[text()=" Get data "]/..'
    __popup_menu_dialogs_queue_button = __refresh_dialogs_queue_button + '/../button[2]'

    __remove_all_dialogs_button = '//div[contains(text(),"remove all dialogs")]'
    __stop_all_dialogs_button = '//div[contains(text(),"stop all dialogs")]'
    __run_all_dialogs_button = '//div[contains(text(),"run all dialogs")]'

    __all_dialogs_or_call_list = '//div[@class="ag-center-cols-container"]'
    __msisdn = '//div[@col-id="msisdn"]//div[contains(@class, "app-full")]/span'
    __status_dialog = '//div[@col-id="0"]//div[contains(@class, "app-status")]'
    __status_call = '//div[@col-id="result"]//div[contains(@class, "app-status")]'
    __adding_time = '//div[@col-id="date_added"]//div[contains(@class, "app-full")]/span'

    __base_sorting_menu = '//div[@class="ag-header-row"]/div'
    __status_sorting_button = __base_sorting_menu + '//span[text()="status"]'
    __adding_time_sorting_button = __base_sorting_menu + '//span[text()="adding time"]'

    __base_filter_menu = '//app-universal-filter[@class="app-universal-filter"]'
    __value_filter_input = __base_filter_menu + '//input'
    __param_filter_button = __base_filter_menu + '//span[contains(text(),"a")]'
    __param_filter_dialog = ''
    __param_filter_status = ''

    __action_remove = '//app-queue-cell-actions/button[2]'
    __action_pause = '//app-queue-cell-actions/button[1]'
    __action_return = '//app-queue-cell-actions/button[1]'

    __calls_queue = '//div[text()="calls"]'
    __refresh_calls_queue_button = '//div[@fxlayoutalign="end center"]/button'

    __yes_button = '//span[contains(text(),"yes")]/..'
    __confirm_button = '//span[contains(text(),"confirm")]/..'

    @allure.step('Открытие вкладики Dialogs')
    def open_dialogs_queue(self):
        self.click_by_xpath(self.__dialogs_queue)

    @allure.step('Открытие вкладики Calls')
    def open_calls_queue(self):
        self.click_by_xpath(self.__calls_queue)

    @allure.step('Удалить/поставить на паузу/вернуть n-ый по списку диалог или звонок')
    def action_n_dialog_or_call(self, page: str, number, action: str):
        if page in 'dialogs':
            self.open_dialogs_queue()
        if page in 'calls':
            self.open_calls_queue()
        _n_line = self.__all_dialogs_or_call_list + '/div[{}]'.format(str(number))
        if action.lower() == 'remove':
            _locator = _n_line + self.__action_remove
            self.click_by_xpath(_locator)
            self.click_by_xpath(self.__yes_button)
        if action.lower() == 'pause':
            _locator = _n_line + self.__action_pause
            self.click_by_xpath(_locator)
        if action.lower() == 'return':
            _locator = _n_line + self.__action_return
            self.click_by_xpath(_locator)

    @allure.step('Получить размер очереди диалогов и звонков')
    def get_count_list_dialogs_and_calls(self):
        self.open_dialogs_queue()
        dialogs = self.__all_dialogs_or_call_list + '/div'
        dialogs_count = len(self.find_elements(dialogs))
        self.open_dialogs_queue()
        calls = self.__all_dialogs_or_call_list + '/div'
        calls_count = len(self.find_elements(calls))
        return {"dialogs": dialogs_count, "calls": calls_count}

    @allure.step('Получить информацию о звонке/диалоге в очереди')
    def get_queue_info(self, page='dialogs', number='all'):
        if page in 'dialogs':
            self.open_dialogs_queue()
            self.get_dialogs_queue_list()
        if page in 'calls':
            self.open_calls_queue()
            self.refresh_calls_queue_list()

        _n_item = self.__all_dialogs_or_call_list + '/div'
        count = len(self.find_elements(_n_item))
        stats_list = {}
        for i in range(count):
            _n_item = self.__all_dialogs_or_call_list + '/div[{}]'.format(str(i + 1))
            adding_time = None
            if page in 'dialogs':
                _status = _n_item + self.__status_dialog
            else:
                _status = _n_item + self.__status_call
                _adding_time = _n_item + self.__adding_time
                adding_time = self.get_tag_text(_adding_time)

            _msisdn = _n_item + self.__msisdn
            msisdn = self.get_tag_text(_msisdn)
            status = self.get_tag_text(_status)

            stats_list[str(i + 1)] = {"status": status, "msisdn": msisdn, "adding_time": adding_time}

        if number == 'all':
            return stats_list
        else:
            return stats_list[str(number)]

    @allure.step('Получить информация о диалоге/звонки по msisdn')
    def get_queue_info_for_msisdn(self, page='dialogs', msisdn=None):
        dict_stats = self.get_queue_info(page=page)
        for item in range(len(dict_stats)):
            if dict_stats[str(item + 1)]['msisdn'] == str(msisdn):
                return dict_stats[str(item + 1)]

    @allure.step('Сортировка списка звонков/диалогов в очереди')
    def sorting_queue_list(self, page: str, column: str):
        if page.lower() in 'dialogs':
            self.open_dialogs_queue()
        elif page.lower() in 'calls':
            self.open_calls_queue()
        else:
            raise print('Param page must be "dialogs" or "calls"')
        if column.lower() == 'status':
            self.click_by_xpath(self.__status_sorting_button)
        if column.lower() == 'adding_time':
            self.click_by_xpath(self.__adding_time_sorting_button)

    @allure.step('Открытие меню действий с очередью диалогов')
    def open_popup_menu_dialogs_queue(self):
        self.open_dialogs_queue()
        self.click_by_xpath(self.__popup_menu_dialogs_queue_button)

    @allure.step('Удалить все диалоги')
    def remove_all_dialogs(self):
        self.open_dialogs_queue()
        self.click_by_xpath(self.__popup_menu_dialogs_queue_button)
        self.click_by_xpath(self.__remove_all_dialogs_button)
        self.click_by_xpath(self.__confirm_button)
        self.get_dialogs_queue_list()

    @allure.step('Получить список диалогов в очереди')
    def get_dialogs_queue_list(self):
        self.open_dialogs_queue()
        self.click_by_xpath(self.__refresh_dialogs_queue_button)

    @allure.step('Вернуть все диалоги с паузы')
    def run_all_dialogs(self):
        self.open_dialogs_queue()
        self.open_popup_menu_dialogs_queue()
        self.click_by_xpath(self.__run_all_dialogs_button)

    @allure.step('Поставить все диалоги на паузу')
    def stop_all_dialogs(self):
        self.open_dialogs_queue()
        self.open_popup_menu_dialogs_queue()
        self.click_by_xpath(self.__stop_all_dialogs_button)

    @allure.step('Фильтрация списка диалогов')
    def filter_dialogs_queue_list(self, param: str, text: str):
        self.open_dialogs_queue()
        self.click_by_xpath(self.__param_filter_button)
        if param.lower() in 'dialog':
            self.click_by_xpath(self.__param_filter_dialog)
        if param.lower() in 'status':
            self.click_by_xpath(self.__param_filter_status)
        self.send_keys_by_xpath(self.__value_filter_input, text)
        self.get_dialogs_queue_list()

    @allure.step('Изменение количеста строк на странице очереди диалогов')
    def change_items_per_page_dialogs_queue(self):
        self.open_dialogs_queue()
        pass

    @allure.step('Обновить список звонков в очереди')
    def refresh_calls_queue_list(self):
        self.open_calls_queue()
        self.click_by_xpath(self.__refresh_calls_queue_button)
