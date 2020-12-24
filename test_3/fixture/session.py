import time


class SessionHelper:

    def __init__(self, app3):
        self.app = app3

    def login(self):
        wd = self.app.wd
        self.app.open_login_page()
        wd.find_element_by_id("mat-input-0").send_keys("ikoshkin@neuro.net")
        wd.find_element_by_id("mat-input-1").send_keys("123456")
        wd.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(5)

    def logout(self):
        wd = self.app.wd
        self.app.page.return_to_main()
        wd.get("https://cms-v3.neuro.net/agents?lng=en")
        wd.find_element_by_css_selector(
            "span.mat-button-wrapper > div > mat-icon.mat-icon.notranslate.mat-icon-no-color > svg").click()
        wd.find_element_by_xpath("//div[@id='mat-menu-panel-0']/div/div/button/div/div").click()

