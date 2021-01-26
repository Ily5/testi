import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# class PageHelper:
#
#     def __init__(self, app_3):
#         self.app = app_3
#
#     def go_to_project(self, uuid):
#         wd = self.app.wd
#         wd.get("https://cms-v3.neuro.net/agent-settings/settings?lng=en&agent_uuid=%s" % uuid)
#
#     def return_to_main(self):
#         wd = self.app.wd
#         wd.find_element_by_xpath("//div/span").click()

