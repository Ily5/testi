import allure
from test_3.fixture.WebFW.AnyPage import AnyPage


# todo переписать локаторы на нормальные
class LoginPage(AnyPage):
    __set_username = '//*[@id="mat-input-0"]'
    __set_password = '//*[@id="mat-input-1"]'
    __show_password_button = ''
    __remember_me_button = ''
    __login_button = '/html/body/app-root/app-login/div/mat-card/form/div/button'

    @allure.step('Логин в систему')
    def login_in_cms(self, username, password):
        self._send_text_login(username)
        self._send_text_password(password)
        self._click_login_button()

    @allure.step('Ввод текста в поле логин')
    def _send_text_login(self, username):
        self.send_keys_by_xpath(self.__set_username, username)
        return self

    @allure.step('Ввод текста в поле пароль')
    def _send_text_password(self, password):
        self.send_keys_by_xpath(self.__set_password, password)
        return self

    @allure.step('Клик по кнопке "Log in"')
    def _click_login_button(self):
        self.click_by_xpath(self.__login_button)
        return self
