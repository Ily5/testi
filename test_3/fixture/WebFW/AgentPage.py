import time
import allure
from test_3.fixture.WebFW.AnyPage import AnyPage


class AnyAgentPage(AnyPage):
    __main_page_button = ''
    __dashboard_button = ''
    __conversation_flow_button = ''
    __nlu_engine_button = ''
    __records_button = ''
    __logs_button = ''
    __contacts_button = ''
    __analytics_button = ''
    __data_uploading_button = '//span[contains(text(),"data uploading")]'
    __queue_button = ''
    __test_nlu_button = ''

    @allure.step('')
    def open_data_uploading_page(self):
        self.click_by_xpath(self.__data_uploading_button)
