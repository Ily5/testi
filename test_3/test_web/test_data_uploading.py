import time
import datetime
import allure


class TestWebDataUploading:

    @allure.feature('Загрузка валидного файла')
    def test_data_uploading_valid_file(self, agent_settings_page, remove_queue_dialogs_and_calls):
        agent_settings_page.AnyAgentPage.open_data_uploading_page()

        count = agent_settings_page.BasePage.get_count_elements()

        valid_file_path = agent_settings_page.test_data['path_to_uploading_file']['valid_file']
        agent_settings_page.DataUploadingPage.uploading_file(valid_file_path)

        count_new = agent_settings_page.BasePage.get_count_elements()

        result = agent_settings_page.DataUploadingPage.get_info_n_file(1)
        assert result['status'] == 'SUCCESS'
        assert result['name'] == agent_settings_page.test_data['name_uploading_file']['valid_file']
        assert result['count_contact'] is not None
        assert count_new == count + 1

    @allure.feature('Загрузка невалидного файла')
    def test_data_uploading_no_valid_file(self, agent_settings_page):
        agent_settings_page.AnyAgentPage.open_data_uploading_page()

        count = agent_settings_page.BasePage.get_count_elements()

        no_valid_file_path = agent_settings_page.test_data['path_to_uploading_file']['no_valid_file']
        agent_settings_page.DataUploadingPage.uploading_file(no_valid_file_path)

        count_new = agent_settings_page.BasePage.get_count_elements()

        result = agent_settings_page.DataUploadingPage.get_info_n_file(1)
        assert result['status'] == 'FAILED'
        assert result['name'] == agent_settings_page.test_data['name_uploading_file']['no_valid_file']
        assert result['error_message'] is not None
        assert count_new == count + 1

    @allure.feature('Изменение сортировки списка загруженных файлов')
    def test_edit_sorted(self, agent_settings_page):
        agent_settings_page.AnyAgentPage.open_data_uploading_page()
        before = agent_settings_page.DataUploadingPage.get_info_n_file(1)
        before_time = datetime.datetime.strptime(before['time_uploading'][0:-4], "%d.%m.%Y %H:%M:%S")

        agent_settings_page.DataUploadingPage.click_button_sorting_list()
        after = agent_settings_page.DataUploadingPage.get_info_n_file(1)
        after_time = datetime.datetime.strptime(after['time_uploading'][0:-4], "%d.%m.%Y %H:%M:%S")

        agent_settings_page.DataUploadingPage.click_button_sorting_list()
        before_new = agent_settings_page.DataUploadingPage.get_info_n_file(1)
        before_time_new = datetime.datetime.strptime(before_new['time_uploading'][0:-4], "%d.%m.%Y %H:%M:%S")

        assert before['time_uploading'] != after['time_uploading']
        assert before['time_uploading'] == before_new['time_uploading']
        assert before_time > after_time
        assert after_time < before_time_new
        assert before_time == before_time_new

    @allure.feature('Фильтрация по статусу - All statuses')
    def test_filters_all_statuses(self, agent_settings_page):
        agent_settings_page.DataUploadingPage.open_data_uploading_page()

        count_elements = agent_settings_page.DataUploadingPage.count_list_files()
        count = 10
        if count > count_elements: count = count_elements
        result = [agent_settings_page.DataUploadingPage.get_info_n_file(i)['status'] for i in range(1, count + 1)]

        assert "SUCCESS" in result
        assert "FAILED" in result

    @allure.feature('Фильтрация по статусу - Success')
    def test_filters_success(self, agent_settings_page):
        agent_settings_page.DataUploadingPage.open_data_uploading_page()
        agent_settings_page.DataUploadingPage.set_filer_status(status='success')

        count_elements = agent_settings_page.DataUploadingPage.count_list_files()
        count = 10
        if count > count_elements: count = count_elements
        result = [agent_settings_page.DataUploadingPage.get_info_n_file(i)['status'] for i in range(1, count + 1)]

        for res in result:
            assert res == "SUCCESS"

    @allure.feature('Фильтрация по статусу - Failed')
    def test_filters_failed(self, agent_settings_page):
        agent_settings_page.DataUploadingPage.open_data_uploading_page()
        agent_settings_page.DataUploadingPage.set_filer_status(status='failed')

        count_elements = agent_settings_page.DataUploadingPage.count_list_files()
        count = 10
        if count > count_elements: count = count_elements
        result = [agent_settings_page.DataUploadingPage.get_info_n_file(i)['status'] for i in range(1, count + 1)]

        for res in result:
            assert res == "FAILED"

    @allure.feature('Фильтрация по статусу - Loading')
    def test_filters_loading(self, agent_settings_page):
        agent_settings_page.DataUploadingPage.open_data_uploading_page()
        agent_settings_page.DataUploadingPage.set_filer_status(status='loading')

        count_elements = agent_settings_page.DataUploadingPage.count_list_files()

        assert count_elements == 0

    @allure.feature('Фильтрация по статусу - Warning')
    def test_filters_warning(self, agent_settings_page):
        agent_settings_page.DataUploadingPage.open_data_uploading_page()
        agent_settings_page.DataUploadingPage.set_filer_status(status='warning')

        count_elements = agent_settings_page.DataUploadingPage.count_list_files()

        assert count_elements == 0

    @allure.feature('Удаление одного успшено загруженного файла со статсус success из списка')
    def test_delete_one_valid_file(self, agent_settings_page):
        agent_settings_page.DataUploadingPage.open_data_uploading_page()
        agent_settings_page.DataUploadingPage.set_filer_status(status='success')
        before = agent_settings_page.DataUploadingPage.get_info_n_file(1)
        agent_settings_page.DataUploadingPage.delete_n_file(1)
        after = agent_settings_page.DataUploadingPage.get_info_n_file(1)

        assert before['time_uploading'] != after['time_uploading']

    @allure.feature('Удаление одного успешно загруженного файла со статусом failed из списка')
    def test_delete_one_no_valid_file(self, agent_settings_page):
        agent_settings_page.DataUploadingPage.open_data_uploading_page()
        agent_settings_page.DataUploadingPage.set_filer_status(status='failed')

        no_valid_file_path = agent_settings_page.test_data['path_to_uploading_file']['no_valid_file']
        agent_settings_page.DataUploadingPage.uploading_file(no_valid_file_path)
        before = agent_settings_page.DataUploadingPage.get_info_n_file(1)

        agent_settings_page.DataUploadingPage.delete_n_file(1)
        after = agent_settings_page.DataUploadingPage.get_info_n_file(1)

        assert before['time_uploading'] != after['time_uploading']

    @allure.feature('Скачивание образца загрузочного файла')
    def test_download_example(self, agent_settings_page):
        agent_settings_page.DataUploadingPage.open_data_uploading_page()

        locator = agent_settings_page.DataUploadingPage._DataUploadingPage__download_example
        flag = agent_settings_page.BasePage.check_element_on_page(locator)
        assert flag
        # todo добавить скачивание файла и проверку, что он скачался
        # agent_settings_page.DataUploadingPage.download_example()

    @allure.feature('Скачивание валидного успешно загруженного файла')
    def test_download_valid_file(self, agent_settings_page):
        agent_settings_page.AnyAgentPage.open_data_uploading_page()
        agent_settings_page.DataUploadingPage.set_filer_status(status='success')

        locator = agent_settings_page.DataUploadingPage._DataUploadingPage__all_uploading_file_list + '/div[1]'
        locator_1 = agent_settings_page.DataUploadingPage._DataUploadingPage__download_valid_file
        locator += locator_1

        flag = agent_settings_page.BasePage.check_element_on_page(locator)
        assert flag

        # todo добавить скачивание файла и проверку, что он скачался
        # agent_settings_page.DataUploadingPage.download_valid_n_file(1)

    @allure.feature('Удаление всех успешно загруженных файлов')
    def test_delete_all_completed_file(self, agent_settings_page):
        agent_settings_page.AnyAgentPage.open_data_uploading_page()
        agent_settings_page.DataUploadingPage.delete_all_completed_uploading()
        time.sleep(1)

        count_elements = agent_settings_page.DataUploadingPage.count_list_files()

        assert count_elements == 0
