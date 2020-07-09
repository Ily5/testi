from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class PageHelper:

    def __init__(self, app):
        self.app = app

    def check_navigate_elements(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Logic").click()
        wd.find_element_by_link_text("Entities").click()
        wd.find_element_by_link_text("Records").click()
        wd.find_element_by_link_text("Prompts").click()
        wd.find_element_by_link_text("Data uploading").click()
        wd.find_element_by_link_text("Call Logs").click()
        wd.find_element_by_link_text("Analytics").click()
        wd.find_element_by_link_text("Accounts").click()

    def open_projects_menu(self):
        wd = self.app.wd
        wd.find_element_by_id("a_project").click()

    def add(self, project):
        wd = self.app.wd
        self.open_projects_menu()
        wd.find_element_by_link_text("Create New Agent").click()
        wd.find_element_by_id("name_add").send_keys(project.name)
        wd.find_element_by_id("description_add").send_keys(project.description)
        wd.find_element_by_name("not_before").send_keys(project.not_before)
        wd.find_element_by_name("not_after").send_keys(project.not_after)
        wd.find_element_by_name("delay").send_keys(project.delay)
        wd.find_element_by_id("count_add").send_keys(project.count)
        wd.find_element_by_id("channel_add").send_keys(project.channel)
        wd.find_element_by_id("flag_add").send_keys(project.flag)
        wd.find_element_by_id("api_url_add").send_keys(project.api_url)
        wd.find_element_by_id("start_unit_add").send_keys(project.start_unit)
        wd.find_element_by_id("log_verbose").click()
        wd.find_element_by_id("record_path").send_keys(project.record_path)
        wd.find_element_by_id("caller_id").send_keys(project.caller_id)
        wd.find_element_by_id("before_call_unit").send_keys(project.before_call_unit)
        wd.find_element_by_id("after_call_unit").send_keys(project.after_call_unit)
        wd.find_element_by_id("routing_channel_limit").send_keys(project.routing_channel_limit)
        wd.find_element_by_id("total_channel_limit").send_keys(project.total_channel_limit)
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
        wd.find_element_by_id("tts").send_keys(project.tts)
        wd.find_element_by_id("btn_add_project_save").click()

    def edit(self, project):
        wd = self.app.wd
        self.open_projects_menu()
        wd.find_element_by_link_text("Settings").click()
        wd.find_element_by_id("name_edit").clear()
        wd.find_element_by_id("name_edit").send_keys(project.name)
        wd.find_element_by_id("description_edit").clear()
        wd.find_element_by_id("description_edit").send_keys(project.description)
        wd.find_element_by_id("not_before_edit").send_keys(project.not_before)
        wd.find_element_by_id("not_after_edit").send_keys(project.not_after)
        wd.find_element_by_id("delay_edit").send_keys(project.delay)
        wd.find_element_by_id("count_edit").send_keys(project.count)
        wd.find_element_by_id("channel_edit").clear()
        wd.find_element_by_id("channel_edit").send_keys(project.channel)
        wd.find_element_by_id("flag_edit").clear()
        wd.find_element_by_id("flag_edit").send_keys(project.flag)
        wd.find_element_by_id("api_url_edit").clear()
        wd.find_element_by_id("api_url_edit").send_keys(project.api_url)
        wd.find_element_by_id("start_unit_edit").clear()
        wd.find_element_by_id("start_unit_edit").send_keys(project.start_unit)
        wd.find_element_by_id("log_verbose").click()
        wd.find_element_by_id("record_path").clear()
        wd.find_element_by_id("record_path").send_keys(project.record_path)
        wd.find_element_by_id("caller_id").clear()
        wd.find_element_by_id("caller_id").send_keys(project.caller_id)
        wd.find_element_by_id("before_call_unit").clear()
        wd.find_element_by_id("before_call_unit").send_keys(project.before_call_unit)
        wd.find_element_by_id("after_call_unit").clear()
        wd.find_element_by_id("after_call_unit").send_keys(project.after_call_unit)
        wd.find_element_by_id("routing_channel_limit").clear()
        wd.find_element_by_id("routing_channel_limit").send_keys(project.routing_channel_limit)
        wd.find_element_by_id("total_channel_limit").clear()
        wd.find_element_by_id("total_channel_limit").send_keys(project.total_channel_limit)
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
        wd.find_element_by_id("tts").send_keys(project.tts)
        wd.find_element_by_id("btn_edit_project_save").click()

    def go_to_entities_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Entities").click()

    def create_in_entity(self, name, json):
        wd = self.app.wd
        self.go_to_entities_page()
        wd.find_element_by_id("btn_add_recobj").click()
        wd.find_element_by_id("input_name").send_keys(name)
        wd.find_element_by_id("input_json").send_keys(json)
        wd.find_element_by_id("input_entype").click()
        Select(wd.find_element_by_id("input_entype")).select_by_visible_text("str")
        wd.find_element_by_xpath("//option[@value='str']").click()
        wd.find_element_by_id("input_language").click()
        Select(wd.find_element_by_id("input_language")).select_by_visible_text("Russian (Russia)-ru-RU")
        wd.find_element_by_xpath("//option[@value='ru-RU']").click()
        wd.find_element_by_id("btn-add-form-subm").click()
        wd.find_element_by_xpath("//table[@id='recobjs_table']/tbody/tr/td[5]/a/i").click()

    def delete_in_entity(self):
        wd = self.app.wd
        self.go_to_entities_page()
        try:
            assert "py_test_entity" in wd.find_element_by_xpath("//table[@id='recobjs_table']/tbody/tr/td").text
        except AssertionError as e:
            self.app.verificationErrors.append(str(e))
        wd.find_element_by_xpath("(//button[@type='button'])[5]").click()

    def edit_prompt(self):
        wd = self.app.wd
        self.open_prompts_page()
        WebDriverWait(wd, 2).until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[@class='ivu-modal-wrap vertical-center-modal circuit-loading-modal']")))
        mySelectElement = WebDriverWait(wd, 2).until(EC.element_to_be_clickable(
            (By.XPATH, "// *[ @ id = 'promts_table'] / tbody / tr[1] / td[3] / a")))
        mySelectElement.click()
        wd.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div[2]/button").click()
        wd.find_element_by_id("text").send_keys("text_prompt")
        wd.find_element_by_id("flag-feild").send_keys("pytest_project")
        Select(wd.find_element_by_id("language-feild")).select_by_visible_text("Russian (Russia)-ru-RU")
        wd.find_element_by_xpath("//option[@value='ru-RU']").click()
        wd.find_element_by_id("file").send_keys(r"/tmp/audio.wav")
        wd.find_element_by_id("btn-add-form-subm").click()
        #wd.find_element_by_id("btn-edit-file-form-subm").click()
        # app.wd.find_element_by_xpath("// div[ @ id = 'file_add_modal'] / div").click()
        # if app.wd.is_element_present(app.wd.By.XPATH, "//table[@id='promt_files_table']/tbody/tr/td[4]/button/i"):
        # app.click_buttons_by_class_name(s="btn btn-danger btn-del-file")
        # // *[ @ id = "promt_files_table"] / tbody / tr[1] / td[8] / button
        self.open_prompts_page()
        wd.find_element_by_xpath('// *[ @ id = "promts_table"] / tbody / tr[1] / td[4] / button').click()

    def add_prompt(self, name, desc):
        wd = self.app.wd
        self.open_prompts_page()
        wd.find_element_by_id("add_promt").click()
        wd.find_element_by_id("name").send_keys(name)
        wd.find_element_by_id("description").send_keys(desc)
        wd.find_element_by_id("btn-add-form-subm").submit()


    def open_prompts_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Records").click()
        wd.find_element_by_link_text("Prompts").click()


