from selenium import webdriver
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from fixture.session import SessionHelper
from fixture.page import PageHelper


class Application:

    def __init__(self):
        # self.wd = webdriver.Firefox(executable_path=r'C:\Jenkins\workspace\geckodriver.exe')

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


    def prompt_edit(self):
        wd = self.wd
        WebDriverWait(wd, 2).until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[@class='ivu-modal-wrap vertical-center-modal circuit-loading-modal']")))
        mySelectElement = WebDriverWait(wd, 2).until(EC.element_to_be_clickable(
            (By.XPATH, "// *[ @ id = 'promts_table'] / tbody / tr[1] / td[3] / a")))
        mySelectElement.click()
        wd.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div[2]/button").click()
        wd.find_element_by_id("text").send_keys("text_prompt")
        wd.find_element_by_id("flag-feild").send_keys("pytest_project")
        Select(wd.find_element_by_id("language-feild")).select_by_visible_text("Russian (Russia)-ru-RU")

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
