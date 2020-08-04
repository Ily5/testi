from selenium import webdriver
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from fixture.session import SessionHelper
from fixture.page import PageHelper
from fixture.asr import AsrHelper
from fixture.api import ApiHelper


class Application:

    def __init__(self):
        # self.wd = webdriver.Firefox(executable_path=r'/home/ilya/PycharmProjects/geckodriver')

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

        self.wd.implicitly_wait(10)
        self.verificationErrors = []
        self.session = SessionHelper(self)
        self.page = PageHelper(self)
        self.asr = AsrHelper(self)
        self.api = ApiHelper(self)

    def click_buttons_by_class_name(self, s):
        wd = self.wd
        elements = wd.find_elements(By.CLASS_NAME, s)
        # app.wd.find_elements_by_class_name("btn btn-danger btn-del-file")
        print(elements)
        for e in elements:
            e.click()

    def open_login_page(self):
        wd = self.wd
        wd.get("https://cms-test.neuro.net/login")

    def edit_logic_unit(self):
        wd = self.wd
        wd.find_element_by_xpath("//*[@id='add_action']").click()

    def cancel(self):
        self.wd.quit()
