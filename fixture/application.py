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

        self.wd.implicitly_wait(30)
        self.verificationErrors = []
        self.session = SessionHelper(self)
        self.page = PageHelper(self)

    def create_project(self):
        wd = self.wd
        wd.find_element_by_id("name_add").send_keys("name")
        wd.find_element_by_id("description_add").send_keys("desc")
        wd.find_element_by_name("not_before").send_keys("00:00")
        wd.find_element_by_name("not_after").send_keys("00:01")
        wd.find_element_by_name("delay").send_keys("00:01")
        wd.find_element_by_id("count_add").send_keys("0")
        wd.find_element_by_id("channel_add").send_keys("mtt_sbc")
        wd.find_element_by_id("flag_add").send_keys("pytest_project")
        wd.find_element_by_id("api_url_add").send_keys("api-test.neuro.net")
        wd.find_element_by_id("start_unit_add").send_keys("hello_main")
        wd.find_element_by_id("log_verbose").click()
        wd.find_element_by_id("record_path").send_keys("{msisdn}_{uuid}")
        wd.find_element_by_id("caller_id").send_keys("1")
        wd.find_element_by_id("before_call_unit").send_keys("set_data_before_call")
        wd.find_element_by_id("after_call_unit").send_keys("1")
        wd.find_element_by_id("routing_channel_limit").send_keys("2")
        wd.find_element_by_id("total_channel_limit").send_keys("3")
        wd.find_element_by_xpath("//form[@id='project_add_form']/div[18]").click()
        wd.find_element_by_id("company_id").click()
        Select(wd.find_element_by_id("company_id")).select_by_visible_text("Neuro.net")
        wd.find_element_by_xpath("//option[@value='1']").click()
        wd.find_element_by_id("pool_id").click()
        Select(wd.find_element_by_id("pool_id")).select_by_visible_text("test_pool")
        wd.find_element_by_xpath("(//option[@value='1'])[3]").click()
        wd.find_element_by_id("language").click()
        Select(wd.find_element_by_id("language")).select_by_visible_text("Russian (Russia)-ru-RU")
        wd.find_element_by_xpath("//option[@value='ru-RU']").click()
        wd.find_element_by_id("asr").click()
        Select(wd.find_element_by_id("asr")).select_by_visible_text("yandex")
        wd.find_element_by_xpath("//option[@value='yandex']").click()
        wd.find_element_by_id("tts").send_keys("jane@yandex")
        wd.find_element_by_id("btn_edit_project_save").click()
        # btn_add_project_save

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

    def edit_project(self):
        wd = self.wd
        wd.find_element_by_id("name_edit").clear()
        wd.find_element_by_id("name_edit").send_keys("name_edit")
        wd.find_element_by_id("description_edit").clear()
        wd.find_element_by_id("description_edit").send_keys("desc_edit")
        wd.find_element_by_id("not_before_edit").send_keys("00:00")
        wd.find_element_by_id("not_after_edit").send_keys("00:01")
        wd.find_element_by_id("delay_edit").send_keys("00:01")
        wd.find_element_by_id("count_edit").send_keys("0")
        wd.find_element_by_id("channel_edit").clear()
        wd.find_element_by_id("channel_edit").send_keys("sip-client-local")
        wd.find_element_by_id("flag_edit").clear()
        wd.find_element_by_id("flag_edit").send_keys("pytest_project")
        wd.find_element_by_id("api_url_edit").clear()
        wd.find_element_by_id("api_url_edit").send_keys("api-test.neuro.net")
        wd.find_element_by_id("start_unit_edit").clear()
        wd.find_element_by_id("start_unit_edit").send_keys("hello_name")
        wd.find_element_by_id("log_verbose").click()
        wd.find_element_by_id("record_path").clear()
        wd.find_element_by_id("record_path").send_keys("{msisdn}_{uuid}")
        wd.find_element_by_id("caller_id").clear()
        wd.find_element_by_id("caller_id").send_keys("1")
        wd.find_element_by_id("before_call_unit").clear()
        wd.find_element_by_id("before_call_unit").send_keys("set_data_before_call")
        wd.find_element_by_id("after_call_unit").clear()
        wd.find_element_by_id("after_call_unit").send_keys("1")
        wd.find_element_by_id("routing_channel_limit").clear()
        wd.find_element_by_id("routing_channel_limit").send_keys("2")
        wd.find_element_by_id("total_channel_limit").clear()
        wd.find_element_by_id("total_channel_limit").send_keys("3")
        # wd.find_element_by_xpath("//form[@id='project_add_form']/div[18]").click()
        wd.find_element_by_id("company_id").click()
        Select(wd.find_element_by_id("company_id")).select_by_visible_text("Neuro.net")
        wd.find_element_by_xpath("//option[@value='1']").click()
        wd.find_element_by_id("pool_id").click()
        Select(wd.find_element_by_id("pool_id")).select_by_visible_text("test_pool")
        wd.find_element_by_xpath("(//option[@value='1'])[3]").click()
        wd.find_element_by_id("language").click()
        Select(wd.find_element_by_id("language")).select_by_visible_text("Russian (Russia)")
        wd.find_element_by_xpath("//option[@value='ru-RU']").click()
        wd.find_element_by_id("asr").click()
        Select(wd.find_element_by_id("asr")).select_by_visible_text("yandex")
        wd.find_element_by_xpath("//option[@value='yandex']").click()
        wd.find_element_by_id("tts").clear()
        wd.find_element_by_id("tts").send_keys("jane@yandex")
        wd.find_element_by_id("btn_edit_project_save").click()

    def create_in_entity(self):
        wd = self.wd
        wd.find_element_by_id("btn_add_recobj").click()
        wd.find_element_by_id("input_name").send_keys("py_test_entity")
        wd.find_element_by_id("input_json").send_keys("run_entity")
        wd.find_element_by_id("input_entype").click()
        Select(wd.find_element_by_id("input_entype")).select_by_visible_text("str")
        wd.find_element_by_xpath("//option[@value='str']").click()
        wd.find_element_by_id("input_language").click()
        Select(wd.find_element_by_id("input_language")).select_by_visible_text("Russian (Russia)-ru-RU")
        wd.find_element_by_xpath("//option[@value='ru-RU']").click()
        wd.find_element_by_id("btn-add-form-subm").click()
        wd.find_element_by_xpath("//table[@id='recobjs_table']/tbody/tr/td[5]/a/i").click()

    def delete_input_entity(self):
        wd = self.wd
        wd.find_element_by_link_text("Entities").click()
        try:
            assert "py_test_entity" in wd.find_element_by_xpath("//table[@id='recobjs_table']/tbody/tr/td").text
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        wd.find_element_by_xpath("(//button[@type='button'])[5]").click()

    def open_login_page(self):
        wd = self.wd
        wd.get("https://cms-test.neuro.net/login")

    def edit_logic_unit(self):
        wd = self.wd
        wd.find_element_by_xpath("//*[@id='add_action']").click()

    def cancel(self):
        self.wd.quit()
