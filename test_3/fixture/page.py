import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class PageHelper:

    def __init__(self, app_3):
        self.app = app_3

    def go_to_project(self, uuid):
        wd = self.app.wd
        wd.get("https://cms-test-v3.neuro.net/agent-settings/settings?lng=en&agent_uuid=%s" % uuid)

    def return_to_main(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//div/span").click()

    def check_menu(self):
        wd = self.app.wd
        # ---prod
        # wd.find_element_by_xpath("//a[3]/div/span").click()
        # wd.find_element_by_xpath("//a[4]/div/span").click()
        # wd.find_element_by_xpath("//a[5]/div/span").click()
        # wd.find_element_by_xpath("//a[6]/div").click()
        # wd.find_element_by_xpath("//a[7]/div/span").click()
        # wd.find_element_by_xpath("//a[8]/div/span").click()
        # wd.find_element_by_xpath("//a[9]/div/span").click()
        # wd.find_element_by_xpath("//a[10]/div").click()
        # ---test
        wd.find_element_by_xpath("//a[2]/div/span").click()
        wd.find_element_by_xpath("//a[3]/div/span").click()
        wd.find_element_by_xpath("//a[4]/div/span").click()
        wd.find_element_by_xpath("//a[5]/div").click()
        wd.find_element_by_xpath("//a[6]/div/span").click()
        wd.find_element_by_xpath("//a[7]/div").click()
        wd.find_element_by_xpath("//a[8]/div").click()
        wd.find_element_by_xpath("//a[9]/div").click()
        wd.find_element_by_xpath("//a[10]/div/span").click()
        wd.find_element_by_xpath("//a[11]/div").click()
        # wd.find_element_by_xpath("//div/span").click()
