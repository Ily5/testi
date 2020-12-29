import time
import allure


class TestWebDataUploading:

    @allure.feature('Загрузка валидного файла')
    def test_data_uploading_valid_file(self, agent_settings_page, remove_queue_dialogs_and_calls):
        agent_settings_page.AnyAgentPage.open_data_uploading_page()

        valid_file_path = agent_settings_page.test_data['path_to_uploading_file']['valid_file']
        data_now = agent_settings_page.BasePage.return_data_time_now()
        agent_settings_page.DataUploadingPage.uploading_file(valid_file_path)

        result = agent_settings_page.DataUploadingPage.get_info_n_file(1)
        assert result['status'] == 'SUCCESS'
        assert result['name'] == agent_settings_page.test_data['name_uploading_file']['valid_file']
        assert data_now in result['time_uploading']

    @allure.feature('Загрузка невалидного файла')
    def test_data_uploading_no_valid_file(self, agent_settings_page):
        agent_settings_page.AnyAgentPage.open_data_uploading_page()

        no_valid_file_path = agent_settings_page.test_data['path_to_uploading_file']['no_valid_file']
        data_now = agent_settings_page.BasePage.return_data_time_now()
        agent_settings_page.DataUploadingPage.uploading_file(no_valid_file_path)

        result = agent_settings_page.DataUploadingPage.get_info_n_file(1)
        assert result['status'] == 'FAILED'
        assert result['name'] == agent_settings_page.test_data['name_uploading_file']['no_valid_file']
        assert data_now in result['time_uploading']


