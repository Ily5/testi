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
    __data_uploading_button = '/html/body/app-root/app-base-layout/mat-drawer-container/mat-drawer[1]/div/div[2]/div/mat-nav-list/a[10]'
    __queue_button = ''
    __test_nlu_button = ''

    @allure.step('')
    def open_data_uploading_page(self):
        self.click_by_xpath(self.__data_uploading_button)


class DataUploadingPage(AnyAgentPage):
    __input_select_file = '/html/body/app-root/app-base-layout/mat-drawer-container/mat-drawer-content/div/div/main/app-tabs-layout/div/app-data-uploading/app-initial-data/app-content/div/div/div[2]/div[1]/div/div/div[1]/app-dnd-file-uploader/input'
    __select_file_button = '/html/body/app-root/app-base-layout/mat-drawer-container/mat-drawer-content/div/div/main/app-tabs-layout/div/app-data-uploading/app-initial-data/app-content/div/div/div[2]/div[1]/div/div/div[1]/app-dnd-file-uploader/div/button'
    __download_example = ''
    __select_another_file = ''
    __sorting_time_uploading = ''
    __filer_status_button = ''
    __delete_all_menu_button = ''
    __delete_all_completed = ''

    def uploading_file(self, file_path):
        self.send_keys_by_xpath(self.__input_select_file, file_path)
        self.click_by_xpath(self.__select_file_button)
        # todo дожидаться окончания загрузки файла
        time.sleep(10)
