import os
import time
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException, \
    StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    time_element_Wait = 30

    window_scroll_X = 70
    window_scroll_Y = 320

    def __init__(self, app_3):
        self.driver = app_3.wd

    def go_to_project(self, uuid):
        self.driver.get("https://cms-test-v3.neuro.net/agent-settings/settings?lng=en&agent_uuid=%s" % uuid)

    @allure.step('Клик по элементу')
    def click_by_xpath(self, locator):
        try:
            self.waiting_element_to_be_clickable(locator)
            self.scroll_to_element(locator)
            self.driver.find_element_by_xpath(locator).click()
        except ElementNotVisibleException as e:
            self.allure_ElementNotVisibleException(e)
        except NoSuchElementException as e:
            self.allure_NoSuchElementException(e)
        except StaleElementReferenceException as e:
            self.allure_StaleElementReferenceException(e)

    @allure.step("Навести на элемент")
    def move_to_element(self, locator):
        actions = ActionChains(self.driver)
        element = self.driver.find_element_by_xpath(locator)
        actions.move_to_element(element)
        actions.perform()

    @allure.step('Ввод текста')
    def send_keys_by_xpath(self, locator, text):
        try:
            self.scroll_to_element(locator)
            self.driver.find_element_by_xpath(locator).send_keys(text)
        except ElementNotVisibleException as e:
            self.allure_ElementNotVisibleException(e)
        except NoSuchElementException as e:
            self.allure_NoSuchElementException(e)
        except StaleElementReferenceException as e:
            self.allure_StaleElementReferenceException(e)

    @allure.step('Очистка текстовго поля и ввод текста')
    def clear_and_send_keys_by_xpath(self, locator, text):
        self.scroll_to_element(locator)
        self.clear_by_xpath(locator)
        self.driver.find_element_by_xpath(locator).send_keys(text)
        try:
            self.scroll_to_element(locator)
            self.clear_by_xpath(locator)
            self.driver.find_element_by_xpath(locator).send_keys(text)
        except ElementNotVisibleException as e:
            self.allure_ElementNotVisibleException(e)
        except NoSuchElementException as e:
            self.allure_NoSuchElementException(e)
        except StaleElementReferenceException as e:
            self.allure_StaleElementReferenceException(e)

    @allure.step('Получение текста из тега')
    def get_tag_text(self, locator):
        try:
            text = self.driver.find_element_by_xpath(locator).text
            return text
        except ElementNotVisibleException as e:
            self.allure_ElementNotVisibleException(e)
        except NoSuchElementException as e:
            self.allure_NoSuchElementException(e)

    def scroll_to_element(self, locator):
        try:
            temp = self.driver.find_element_by_xpath(locator).location_once_scrolled_into_view
            text = "window.scrollBy(" + str(temp['x'] - self.window_scroll_X) + ", " + str(
                temp['y'] - self.window_scroll_Y) + ")"
            self.driver.execute_script(text)
        except StaleElementReferenceException as e:
            self.allure_ElementNotVisibleException(e)

    @allure.step('Очистка текстового поля')
    def clear_by_xpath(self, locator):
        try:
            self.driver.find_element_by_xpath(locator).clear()
        except ElementNotVisibleException as e:
            self.allure_ElementNotVisibleException(e)
        except NoSuchElementException as e:
            self.allure_NoSuchElementException(e)

    def get_current_url(self):
        return self.driver.current_url

    @allure.step('Нажатие правой кнопкой мыши')
    def right_click_dy_xpath(self, locator):
        try:
            action_chains = ActionChains(self.driver)
            action_chains.context_click(self.driver.find_element_by_xpath(locator)).perform()
        except ElementNotVisibleException as e:
            self.allure_ElementNotVisibleException(e)
        except NoSuchElementException as e:
            self.allure_NoSuchElementException(e)

    @allure.step('Обновление страницы')
    def refresh_the_page(self):
        try:
            self.driver.refresh()
        except StaleElementReferenceException as e:
            pass

    @allure.step('Ввод текста (медленный)')
    def send_keys_by_xpath_slow(self, locator, text, delay):
        waiting_time = (1 / 1000) * float(delay)
        # Костыль, при вводе пропускает первый символ
        text = " " + text
        try:
            self.scroll_to_element(locator)
            for symbol in text:
                time.sleep(waiting_time)
                self.driver.find_element_by_xpath(locator).send_keys(symbol)
        except ElementNotVisibleException as e:
            self.allure_ElementNotVisibleException(e)
        except NoSuchElementException as e:
            self.allure_NoSuchElementException(e)

    def waiting_element_to_be_clickable(self, locator):
        try:
            WebDriverWait(self.driver, self.time_element_Wait).until(EC.element_to_be_clickable((By.XPATH, locator)))
        except TimeoutException as e:
            self.allure_screenshot()

    @allure.step('Проверка наличия элемента на странице')
    def check_element_on_page(self, locator):
        try:
            self.driver.find_element_by_xpath(locator)
            return True
        except NoSuchElementException as e:
            self.allure_NoSuchElementException(e)
            return False

    @allure.step('screenshot')
    def allure_screenshot(self):
        try:
            allure.attach(self.driver.get_screenshot_as_png(), name="Screenshot",
                          attachment_type=AttachmentType.PNG)
        except Exception as e:
            print(str(e))

    @allure.step("select_element_by_visible_text:")
    def select_element_by_visible_text(self, select_locator, text):
        select = Select(self.driver.find_element_by_xpath(select_locator))
        select.select_by_visible_text(text)

    @allure.step('ElementNotVisibleException')
    def allure_ElementNotVisibleException(self):
        self.allure_screenshot()
        assert True is False

    @allure.step('NoSuchElementException')
    def allure_NoSuchElementException(self):
        self.allure_screenshot()
        assert True is False

    @allure.step('StaleElementReferenceException')
    def allure_StaleElementReferenceException(self):
        assert True is False

    @allure.step('Получение количества элементов')
    def get_count_elements(self, locator):
        result = len(self.driver.find_elements_by_xpath(locator))
        return result

    # TODO доработать методы, как понять какое по счету окно браузера по индексу?

    @allure.step('Переключение между вкладками в браузере')
    def switch_to_window_in_browser(self, i):
        windows_list = self.driver.window_handles
        self.driver.switch_to.window(windows_list[i])

    @allure.step('Количество открытых окон браузера')
    def count_windows_browser_open(self):
        len_windows = (len(self.driver.window_handles))
        return len_windows

    @allure.step('Закрыть открытое окно браузера')
    def closed_windows_in_browser(self):
        self.driver.close()
