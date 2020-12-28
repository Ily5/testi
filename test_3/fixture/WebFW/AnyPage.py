from test_3.fixture.BasePage import BasePage


class AnyPage(BasePage):
    __account_button = '//app-user-menu[@class="app-user-menu"]'
    __sing_out_button = '//*[@id="mat-menu-panel-0"]//button'

    def logout(self):
        self._click_by_account_button()
        self.click_by_xpath(self.__sing_out_button)

    def _click_by_account_button(self):
        self.click_by_xpath(self.__account_button)
        return self
