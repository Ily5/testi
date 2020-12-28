import time


class TestWebDataUploading:

    def test_2(self, agent_settings_page):
        time.sleep(3)
        time.sleep(3)

    def test_3(self, agent_settings_page):
        time.sleep(3)
        agent_settings_page.AnyAgentPage.open_data_uploading_page()
        path_no_valid_file = agent_settings_page.test_data['path_to_uploading_file']['no_valid_file']
        agent_settings_page.DataUploadingPage.uploading_file(path_no_valid_file)
