import time
import datetime
import allure


@allure.epic('UI Regression')
@allure.feature('Data uploading')
class TestWebDataUploading:

    @allure.title('Загрузка валидного файла')
    def test_data_uploading_valid_file(self, data_uploading, remove_queue_dialogs_and_calls):

        count = data_uploading.DataUploading.count_list_files()

        valid_file_path = data_uploading.test_data['path_to_uploading_file']['valid_file']
        data_uploading.DataUploading.uploading_file(valid_file_path)

        count_new = data_uploading.DataUploading.count_list_files()

        result = data_uploading.DataUploading.get_info_n_file(1)
        assert result['status'] == 'SUCCESS'
        assert result['name'] == data_uploading.test_data['name_uploading_file']['valid_file']
        assert result['count_contact'] is not None
        assert count_new == count + 1

    @allure.title('Загрузка невалидного файла')
    def test_data_uploading_no_valid_file(self, data_uploading):

        count = data_uploading.DataUploading.count_list_files()

        no_valid_file_path = data_uploading.test_data['path_to_uploading_file']['no_valid_file']
        data_uploading.DataUploading.uploading_file(no_valid_file_path)

        count_new = data_uploading.DataUploading.count_list_files()

        result = data_uploading.DataUploading.get_info_n_file(1)
        assert result['status'] == 'FAILED'
        assert result['name'] == data_uploading.test_data['name_uploading_file']['no_valid_file']
        assert result['error_message'] is not None
        assert count_new == count + 1

    @allure.title('Изменение сортировки списка загруженных файлов')
    def test_edit_sorted(self, data_uploading):
        before = data_uploading.DataUploading.get_info_n_file(1)
        before_time = datetime.datetime.strptime(before['time_uploading'][0:-4], "%d.%m.%Y %H:%M:%S")

        data_uploading.DataUploading.click_button_sorting_list()
        after = data_uploading.DataUploading.get_info_n_file(1)
        after_time = datetime.datetime.strptime(after['time_uploading'][0:-4], "%d.%m.%Y %H:%M:%S")

        data_uploading.DataUploading.click_button_sorting_list()
        before_new = data_uploading.DataUploading.get_info_n_file(1)
        before_time_new = datetime.datetime.strptime(before_new['time_uploading'][0:-4], "%d.%m.%Y %H:%M:%S")

        assert before['time_uploading'] != after['time_uploading']
        assert before['time_uploading'] == before_new['time_uploading']
        assert before_time > after_time
        assert after_time < before_time_new
        assert before_time == before_time_new

    @allure.title('Фильтрация по статусу - All statuses')
    def test_filters_all_statuses(self, data_uploading):

        count_elements = data_uploading.DataUploading.count_list_files()
        count = 10
        if count > count_elements: count = count_elements
        result = [data_uploading.DataUploading.get_info_n_file(i)['status'] for i in range(1, count + 1)]

        assert "SUCCESS" in result
        assert "FAILED" in result

    @allure.title('Фильтрация по статусу - Success')
    def test_filters_success(self, data_uploading):
        data_uploading.DataUploading.set_filer_status(status='success')

        count_elements = data_uploading.DataUploading.count_list_files()
        count = 10
        if count > count_elements: count = count_elements
        result = [data_uploading.DataUploading.get_info_n_file(i)['status'] for i in range(1, count + 1)]

        for res in result:
            assert res == "SUCCESS"

    @allure.title('Фильтрация по статусу - Failed')
    def test_filters_failed(self, data_uploading):
        data_uploading.DataUploading.set_filer_status(status='failed')

        count_elements = data_uploading.DataUploading.count_list_files()
        count = 10
        if count > count_elements: count = count_elements
        result = [data_uploading.DataUploading.get_info_n_file(i)['status'] for i in range(1, count + 1)]

        for res in result:
            assert res == "FAILED"

    @allure.title('Фильтрация по статусу - Loading')
    def test_filters_loading(self, data_uploading):
        data_uploading.DataUploading.set_filer_status(status='loading')

        count_elements = data_uploading.DataUploading.count_list_files()

        assert count_elements == 0

    @allure.title('Фильтрация по статусу - Warning')
    def test_filters_warning(self, data_uploading):
        data_uploading.DataUploading.set_filer_status(status='warning')

        count_elements = data_uploading.DataUploading.count_list_files()

        assert count_elements == 0

    @allure.title('Удаление одного успшено загруженного файла со статсус success из списка')
    def test_delete_one_valid_file(self, data_uploading):
        data_uploading.DataUploading.set_filer_status(status='success')
        count = data_uploading.DataUploading.count_list_files()
        data_uploading.DataUploading.delete_n_file(1)
        count_new = data_uploading.DataUploading.count_list_files()

        assert count == count_new + 1

    @allure.title('Удаление одного успешно загруженного файла со статусом failed из списка')
    def test_delete_one_no_valid_file(self, data_uploading):
        data_uploading.DataUploading.set_filer_status(status='failed')

        no_valid_file_path = data_uploading.test_data['path_to_uploading_file']['no_valid_file']
        data_uploading.DataUploading.uploading_file(no_valid_file_path)
        before = data_uploading.DataUploading.get_info_n_file(1)

        data_uploading.DataUploading.delete_n_file(1)
        after = data_uploading.DataUploading.get_info_n_file(1)

        assert before['time_uploading'] != after['time_uploading']

    @allure.title('Скачивание образца загрузочного файла')
    def test_download_example(self, data_uploading):

        locator = data_uploading.DataUploading._DataUploading__download_example
        flag = data_uploading.BasePage.check_element_on_page(locator)
        assert flag
        # todo добавить скачивание файла и проверку, что он скачался
        # data_uploading.DataUploading.download_example()

    @allure.title('Скачивание валидного успешно загруженного файла')
    def test_download_valid_file(self, data_uploading):

        valid_file_path = data_uploading.test_data['path_to_uploading_file']['valid_file']
        data_uploading.DataUploading.uploading_file(valid_file_path)

        data_uploading.DataUploading.set_filer_status(status='success')

        locator = data_uploading.DataUploading._DataUploading__all_uploading_file_list + '/div[1]'
        locator_1 = data_uploading.DataUploading._DataUploading__download_valid_file
        locator += locator_1

        flag = data_uploading.BasePage.check_element_on_page(locator)
        assert flag

        # todo добавить скачивание файла и проверку, что он скачался
        # data_uploading.DataUploading.download_valid_n_file(1)

    @allure.title('Удаление всех успешно загруженных файлов')
    def test_delete_all_completed_file(self, data_uploading):
        data_uploading.DataUploading.delete_all_completed_uploading()
        time.sleep(1)

        count_elements = data_uploading.DataUploading.count_list_files()

        assert count_elements == 0
