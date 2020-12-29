import allure
from test_3.fixture.BasePage import BasePage


class AnyPage(BasePage):
    __account_button = '//app-user-menu[@class="app-user-menu"]'
    __sing_out_button = '//*[@id="mat-menu-panel-0"]//button'

    @allure.step('Логаут из системы')
    def logout(self):
        self._click_by_account_button()
        self.click_by_xpath(self.__sing_out_button)

    @allure.step('Клик по кнопке аккаунт верхний правый угол')
    def _click_by_account_button(self):
        self.click_by_xpath(self.__account_button)
        return self
