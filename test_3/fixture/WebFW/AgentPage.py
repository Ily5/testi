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
    __download_example = '//div[contains(text(),"download example")]'

    __container_all_uploading_file = '//div[@class="app-initial-data__container__info ng-star-inserted"]'
    __sorting_time_uploading_button = __container_all_uploading_file + '/div/div/button'
    __delete_all_menu_button = __container_all_uploading_file + '/div/button'

    #__filer_status_button = __container_all_uploading_file + '//div[@class="mat-form-field-wrapper ng-tns-c161-85"]'
    __filer_status_button = '/html/body/app-root/app-base-layout/mat-drawer-container/mat-drawer-content/div/div/main/app-tabs-layout/div/app-data-uploading/app-initial-data/app-content/div/div/div[2]/div[1]/div/div/div[2]/div/div/mat-form-field/div'
    __filter_all_statuses = '//span[contains(text(),"All statuses")]'
    __filer_success = '//span[text()=" Success "]'
    __filter_failed = '//span[contains(text(),"Failed")]'
    __filer_warning = '//span[contains(text(),"Warning")]'
    __filter_loading = '//span[contains(text(),"Loading")]'

    __select_another_file = ''
    __delete_all_completed_button = '//div[contains(@class, "overlay-connected")]//button'

    def uploading_file(self, file_path):
        self.send_keys_by_xpath(self.__input_select_file, file_path)
        self.click_by_xpath(self.__upload_file_button)
        # todo добавить ожидание окончания загрузки файла без тайм слип
        time.sleep(10)

    def download_example(self):
        self.click_by_xpath(self.__download_example)

    def delete_all_completed_uploading(self):
        self.click_by_xpath(self.__delete_all_menu_button)
        self.click_by_xpath(self.__delete_all_completed_button)

    def click_button_sorting_list(self):
        self.click_by_xpath(self.__sorting_time_uploading_button)

    def set_filer_status(self, status):
        self.click_by_xpath(self.__filer_status_button)
        locator = None
        if status == 'all_statuses':
            locator = self.__filter_all_statuses
            print(locator)
        if status == 'success':
            locator = self.__filer_success
            print(locator)
        if status == 'failed':
            locator = self.__filter_failed
            print(locator)
        if status == 'warning':
            locator = self.__filer_warning
            print(locator)
        if status == 'loading':
            locator = self.__filter_loading
            print(locator)
        self.click_by_xpath(locator)
        print(locator)

