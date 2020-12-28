from test_3.fixture.BasePage import BasePage


class AnyPage(BasePage):
    __account_button = '/html/body/app-root/app-base-layout/mat-drawer-container/mat-drawer-content/div/mat-toolbar/mat-toolbar-row/div[2]/app-user-menu/button/span[1]/div'
    __sing_out_button = '//*[@id="mat-menu-panel-0"]/div/div/button'

    def logout(self):
        self._click_by_account_button()
        self.click_by_xpath(self.__sing_out_button)

    def _click_by_account_button(self):
        self.click_by_xpath(self.__account_button)
        return self
