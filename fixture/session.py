class SessionHelper:

    def __init__(self, app):
        self.app = app

    def login(self, username, password):
        wd = self.app.wd
        self.app.open_login_page()
        wd.find_element_by_id("username").send_keys(username)
        wd.find_element_by_id("password_field").send_keys(password)
        wd.find_element_by_xpath("//button[@type='submit']").click()

    def logout(self, username):
        wd = self.app.wd
        wd.find_element_by_link_text(username).click()
        wd.find_element_by_link_text("Log out").click()
