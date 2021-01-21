import os
import datetime
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

    @allure.step('Прямой переход по ссылке)')
    def goto_page(self, page):
        title = self.driver.title
        if page != title:
            self.driver.get(page)

    @allure.step('Клик по элементу')
    def click_by_xpath(self, locator):
        try:
            self.waiting_element_to_be_clickable(locator)
            # self.scroll_to_element(locator)
            self.driver.find_element_by_xpath(locator).click()
        except ElementNotVisibleException as e:
            self.allure_ElementNotVisibleException()
        except NoSuchElementException as e:
            self.allure_NoSuchElementException()
        except StaleElementReferenceException as e:
            self.allure_StaleElementReferenceException()

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
            self.allure_ElementNotVisibleException()
        except NoSuchElementException as e:
            self.allure_NoSuchElementException()
        except StaleElementReferenceException as e:
            self.allure_StaleElementReferenceException()

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
            self.allure_ElementNotVisibleException()
        except NoSuchElementException as e:
            self.allure_NoSuchElementException()
        except StaleElementReferenceException as e:
            self.allure_StaleElementReferenceException()

    @allure.step('Получение текста из тега')
    def get_tag_text(self, locator):
        try:
            WebDriverWait(self.driver, self.time_element_Wait).until(
                EC.presence_of_element_located((By.XPATH, locator)))
            text = self.driver.find_element_by_xpath(locator).text
            return text
        except ElementNotVisibleException as e:
            self.allure_ElementNotVisibleException()
        except NoSuchElementException as e:
            self.allure_NoSuchElementException()
        except StaleElementReferenceException as e:
            pass

    @allure.step('Получение текста из атрибута тега')
    def get_attribute_text(self, locator, attribute):
        try:
            element = self.driver.find_element_by_xpath(locator)
            test = element.get_attribute(attribute)
            return test
        except:
            pass

    def scroll_to_element(self, locator):
        try:
            temp = self.driver.find_element_by_xpath(locator).location_once_scrolled_into_view
            text = "window.scrollBy(" + str(temp['x'] - self.window_scroll_X) + ", " + str(
                temp['y'] - self.window_scroll_Y) + ")"
            self.driver.execute_script(text)
        except StaleElementReferenceException as e:
            self.allure_ElementNotVisibleException()

    @allure.step('Получаем список элементов с заданным локатором')
    def find_elements(self, locator):
        elements_list = self.driver.find_elements_by_xpath(locator)
        return elements_list

    @allure.step('Очистка текстового поля')
    def clear_by_xpath(self, locator):
        try:
            self.driver.find_element_by_xpath(locator).clear()
        except ElementNotVisibleException as e:
            self.allure_ElementNotVisibleException()
        except NoSuchElementException as e:
            self.allure_NoSuchElementException()

    @allure.step('Получение URL текущей старинцы')
    def get_current_url(self):
        return self.driver.current_url

    @allure.step('Нажатие правой кнопкой мыши')
    def right_click_dy_xpath(self, locator):
        try:
            action_chains = ActionChains(self.driver)
            action_chains.context_click(self.driver.find_element_by_xpath(locator)).perform()
        except ElementNotVisibleException as e:
            self.allure_ElementNotVisibleException()
        except NoSuchElementException as e:
            self.allure_NoSuchElementException()

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
            self.allure_ElementNotVisibleException()
        except NoSuchElementException as e:
            self.allure_NoSuchElementException()

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
            self.allure_NoSuchElementException()
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

    @staticmethod
    def return_data_time_now_utc():
        return datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M")

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
