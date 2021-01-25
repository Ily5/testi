import time
import allure
from test_3.fixture.WebFW.AnyPage import AnyPage


class AnyAgentPage(AnyPage):
    __main_page_button = ''
    __dashboard_button = '//span[contains(text(),"dashboard")]'
    __conversation_flow_button = '//span[contains(text(),"conversation flow")]'
    __nlu_engine_button = '//span[contains(text(),"nlu engine")]'
    __records_button = '//span[contains(text(),"records")]'
    __logs_button = ''
    __contacts_button = ''
    __analytics_button = ''
    __data_uploading_button = '//span[contains(text(),"data uploading")]'
    __queue_button = '//span[contains(text(),"queue")]'
    __test_nlu_button = ''
    __agent_settings_button = '//span[contains(text(),"agent settings")]'

    @allure.step('Открытие страницы "Data uploading"')
    def open_data_uploading_page(self):
        self.click_by_xpath(self.__data_uploading_button)

    @allure.step('Открытие страницы "Queue"')
    def open_queue_page(self):
        self.click_by_xpath(self.__queue_button)

    @allure.step('Открытие страницы Agent Settings')
    def open_agent_settings_page(self):
        self.click_by_xpath(self.__agent_settings_button)
