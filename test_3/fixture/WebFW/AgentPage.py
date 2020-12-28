import allure
from test_3.fixture.WebFW.AnyPage import AnyPage
import time


# todo поменять локаторы на нормальые
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


class DataUploadingPage(AnyAgentPage):
    __input_select_file = '//input[@type="file"]'
    __select_file_button = '//span[contains(text(),"select file")]/..'
    __upload_file_button = '//span[text()="upload "]'
    __download_example = ''
    __select_another_file = ''
    __sorting_time_uploading = ''
    __filer_status_button = ''
    __delete_all_menu_button = ''
    __delete_all_completed = ''

    def uploading_file(self, file_path):
        self.send_keys_by_xpath(self.__input_select_file, file_path)
        self.click_by_xpath(self.__upload_file_button)
        # todo добавить ожидание окончания загрузки файла без тайм слип
        time.sleep(10)
