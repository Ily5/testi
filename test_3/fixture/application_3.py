from selenium import webdriver
import sys
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from fixture.session import SessionHelper
from fixture.page import PageHelper
from fixture.asr import AsrHelper
from fixture.api import ApiHelper, PoolApiHelper


class ApplicationNewVersion:

    def __init__(self, browser, cms_url, api_url, api_headers, api_methods, pool_api, p_api_headers,
                 project, rwdb, cms_db, mdb):
        if browser == 'firefox':
            # self.wd = webdriver.Firefox()
            self.wd = webdriver.Firefox(executable_path=r'/home/ilya/PycharmProjects/geckodriver')

        elif browser == 'chrome':
            self.wd = webdriver.Chrome()
            # self.wd = webdriver.Chrome(executable_path=r'/home/ilya/PycharmProjects/chromedriver')

        else:
            capabilities = {
                "browserName": "chrome",
                "version": "83.0",
                "platform": "LINUX",
                "enableVNC": True
            }

            self.wd = webdriver.Remote(
                command_executor='http://10.129.0.112:4444/wd/hub',
                desired_capabilities=capabilities
            )

        self.verificationErrors = []

        self.session = SessionHelper(self)
        self.page = PageHelper(self)

        logging.basicConfig(filename=sys.path[1] + "/log/test_asr.log", level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info("Fixture created")


    def open_login_page(self):
        wd = self.wd
        wd.get(self.cms_url + "login")

    def edit_logic_unit(self):
        wd = self.wd
        wd.find_element_by_xpath("//*[@id='add_action']").click()

    def cancel(self):
        self.wd.quit()
