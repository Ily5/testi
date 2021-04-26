from selenium import webdriver
import sys
import logging

from test_3.fixture.BasePage import BasePage
from test_3.fixture.WebFW.AnyPage import AnyPage
from test_3.fixture.WebFW.LoginPage import LoginPage
from test_3.fixture.WebFW.MainPage import MainPage
from test_3.fixture.WebFW.AgentPage import AnyAgentPage
from test_3.fixture.WebFW.AnyAgentPage.DataUploading import DataUploading
from test_3.fixture.WebFW.AnyAgentPage.QueuePage import QueuePage


class ApplicationNewVersion:

    def __init__(self, browser, cms_url, database, test_data=None):

        if browser == 'firefox':
            self.wd = webdriver.Firefox()

        elif browser == 'chrome':
            self.wd = webdriver.Chrome()

        else:
            capabilities = {
                "browserName": "chrome",
                "version": "88.0",
                "platform": "LINUX",
                "enableVNC": True,
                "sessionTimeout": "3m"
            }

            self.wd = webdriver.Remote(
                command_executor='http://10.129.0.112:4444/wd/hub',
                desired_capabilities=capabilities
            )

        self.wd.maximize_window()
        self.verificationErrors = []
        self.wd.implicitly_wait(10)
        self.cms_url = cms_url
        self.database = database
        self.test_data = test_data

        self.BasePage = BasePage(self)
        self.LoginPage = LoginPage(self)
        self.AnyPage = AnyPage(self)
        self.MainPage = MainPage(self)
        self.AnyAgentPage = AnyAgentPage(self)
        self.DataUploading = DataUploading(self)
        self.QueuePage = QueuePage(self)

        logging.basicConfig(filename=sys.path[1] + "/log/test_asr.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info("Fixture created")

    def open_login_page(self):
        wd = self.wd
        wd.get(self.cms_url)

    def cancel(self):
        self.wd.quit()
