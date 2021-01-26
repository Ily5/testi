import time
import allure
from test_3.fixture.WebFW.AnyPage import AnyPage


class AnyAgentPage(AnyPage):
    __main_page_button = '//span[contains(text(),"main page")]'
    __dashboard_button = '//span[contains(text(),"dashboard")]'
    __conversation_flow_button = '//span[contains(text(),"conversation flow")]'
    __nlu_engine_button = '//span[contains(text(),"NLU Engine")]'
    __records_button = '//span[contains(text(),"records")]'
    __logs_button = '//span[contains(text(),"logs")]'
    __contacts_button = '//span[contains(text(),"logs")]'
    __analytics_button = '//span[contains(text(),"analytics")]'
    __data_uploading_button = '//span[contains(text(),"data uploading")]'
    __queue_button = '//span[contains(text(),"queue")]'
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

    @allure.step('Поочередное открытие всех разделов аггента')
    def opening_all_page_agent(self):
        self.click_by_xpath(self.__dashboard_button)
        self.click_by_xpath(self.__conversation_flow_button)
        self.click_by_xpath(self.__nlu_engine_button)
        self.click_by_xpath(self.__records_button)
        self.click_by_xpath(self.__logs_button)
        self.click_by_xpath(self.__contacts_button)
        self.click_by_xpath(self.__analytics_button)
        self.click_by_xpath(self.__data_uploading_button)
        self.click_by_xpath(self.__queue_button)
        self.click_by_xpath(self.__agent_settings_button)
        self.click_by_xpath(self.__main_page_button)
