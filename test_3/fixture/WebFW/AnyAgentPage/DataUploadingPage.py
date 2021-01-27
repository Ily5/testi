import time
import allure
from test_3.fixture.WebFW.AgentPage import AnyAgentPage


class DataUploadingPage(AnyAgentPage):
    __input_select_file = '//input[@type="file"]'
    __select_file_button = '//span[contains(text(),"select file")]/..'
    __upload_file_button = '//span[text()="upload "]/..'
    __download_example = '//div[contains(text(),"download example")]'

    __menu_all_uploading_file = '//div[@class="app-initial-data__container__info ng-star-inserted"]'
    __all_uploading_file_list = __menu_all_uploading_file + '/../div[3]'
    __delete_download_menu = '//div[@class="ng-star-inserted"]'
    __delete_valid_file = __delete_download_menu + '/button[2]'
    __delete_no_valid_file = __delete_download_menu + '/button'
    __sure_delete_file = '//span[contains(text(), "delete")]/..'
    __download_valid_file = __delete_download_menu + '/button[1]'

    __status_file = '/*[1]//div[contains(@class, "status")]'
    __name_file = '/div/div[1]'
    __time_uploading_file = '/div/div[2]/div'
    __error_message_file = '/div/div[2]/div[3]/div'
    __count_contact = '/div/div[2]/div[3]'

    __sorting_time_uploading_button = __menu_all_uploading_file + '/div/div/button'

    __filer_status_button = __menu_all_uploading_file + '//mat-form-field/div'
    __filter_all_statuses = '//span[contains(text(),"All statuses")]'
    __filer_success = '//span[text()=" Success "]'
    __filter_failed = '//span[contains(text(),"Failed")]'
    __filer_warning = '//span[contains(text(),"Warning")]'
    __filter_loading = '//span[contains(text(),"Loading")]'

    __select_another_file = ''

    __delete_all_menu_button = __menu_all_uploading_file + '/div/button'
    __delete_all_completed_button = '//div[contains(@class, "overlay-connected")]//button'

    @allure.step('Загрузка файла')
    def uploading_file(self, file_path):
        self.send_keys_by_xpath(self.__input_select_file, file_path)
        self.waiting_element_to_be_clickable(self.__upload_file_button)
        self.click_by_xpath(self.__upload_file_button)
        self.waiting_element_to_be_clickable(self.__upload_file_button)
        self.waiting_element_to_be_clickable(self.__filter_all_statuses)
        self.refresh_the_page()
        while True:
            result = self.get_info_n_file(1)
            if result['status'] in [None, "STARTED"]:
                time.sleep(0.5)
            break

    @allure.step('Скачивание образца загрузочного файла')
    def download_example(self):
        self.click_by_xpath(self.__download_example)
        self.waiting_element_to_be_clickable(self.__filter_all_statuses)

    @allure.step('Удаление всех успешно загруженных файлов')
    def delete_all_completed_uploading(self):
        self.click_by_xpath(self.__delete_all_menu_button)
        self.click_by_xpath(self.__delete_all_completed_button)
        self.click_by_xpath(self.__sure_delete_file)

    @allure.step('Измениение сортировки по времени загрузки файла')
    def click_button_sorting_list(self):
        self.click_by_xpath(self.__sorting_time_uploading_button)

    @allure.step('Изменение фильтра по статусам')
    def set_filer_status(self, status):
        if self.count_list_files() == 0: raise Exception('Пустой список загруженных файлов')
        if self.count_list_files() > 0:
            self.click_by_xpath(self.__filer_status_button)
            locator = None
            if status == 'all_statuses':
                locator = self.__filter_all_statuses
            if status == 'success':
                locator = self.__filer_success
            if status == 'failed':
                locator = self.__filter_failed
            if status == 'warning':
                locator = self.__filer_warning
            if status == 'loading':
                locator = self.__filter_loading
            self.click_by_xpath(locator)

    @allure.step('Удаление n-ого сверху файла из списка')
    def delete_n_file(self, number):
        base_locator = self.__all_uploading_file_list + '/div[{}]'.format(number)
        delete_file_locator = None
        if self.get_info_n_file(number)['status'] == 'SUCCESS':
            delete_file_locator = base_locator + self.__delete_valid_file
        if self.get_info_n_file(number)['status'] == 'FAILED':
            delete_file_locator = base_locator + self.__delete_no_valid_file

        count = self.count_list_files()
        self.click_by_xpath(delete_file_locator)
        self.click_by_xpath(self.__sure_delete_file)
        while True:
            if self.count_list_files() < count:
                break
            time.sleep(0.5)

    @allure.step('Скачивание n-ого сверху валидного файла из списка')
    def download_valid_n_file(self, number):
        if self.count_list_files() == 0: raise Exception('Пустой список загруженных файлов')
        if self.count_list_files() > 0:
            base_locator = self.__all_uploading_file_list + '/div[{}]'.format(number)
            if self.get_info_n_file(number)['status'] == 'SUCCESS':
                download_file_locator = base_locator + self.__download_valid_file
                self.click_by_xpath(download_file_locator)
                self.waiting_element_to_be_clickable(self.__filter_all_statuses)
            else:
                raise Exception('Возможно скачать только файлы со статусом загрузки success')

    @allure.step('Получение информации из n-ого сверху файла из списка')
    def get_info_n_file(self, number):
        error_message = None
        count_contact = None

        base_locator = self.__all_uploading_file_list + '/div[{}]'.format(number)

        status_locator = base_locator + self.__status_file
        status = self.get_attribute_text(locator=status_locator, attribute='class')
        if 'success' in status.lower():
            status = 'SUCCESS'
        if 'danger' in status.lower():
            status = 'FAILED'
        if 'warning' in status.lower():
            status = 'WARNING'
        else:
            status = 'LOADING'

        name_locator = base_locator + self.__name_file
        name = self.get_tag_text(name_locator)

        time_uploading_locator = base_locator + self.__time_uploading_file
        time_uploading = self.get_tag_text(time_uploading_locator)

        if status == "FAILED":
            try:
                error_message_locator = base_locator + self.__error_message_file
                error_message = self.get_tag_text(error_message_locator)
            except:
                pass

        if status == "SUCCESS":
            try:
                count_contact_locator = base_locator + self.__count_contact
                count_contact = self.get_tag_text(count_contact_locator)
            except:
                pass

        dict_info = {"name": name,
                     "status": status,
                     "time_uploading": time_uploading,
                     "count_contact": count_contact,
                     "error_message": error_message}

        return dict_info

    @allure.step('Получение количества загруженных файлов в списке ')
    def count_list_files(self):
        locator = self.__all_uploading_file_list + '/div'
        return len(self.find_elements(locator))
