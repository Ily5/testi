import time


def test_data_uploading(app):

    time.sleep(10)
    app.page.upload_call()
    """
    driver.find_element_by_id("file").click()
    driver.find_element_by_id("file").clear()
    driver.find_element_by_id("file").send_keys("C:\\fakepath\\init_numb2.xlsx")
    driver.find_element_by_id("btn_add_file").click()
    driver.find_element_by_xpath("//div[@id='table_waiting_calls_wrapper']/div/button[2]/span").click()
    driver.find_element_by_xpath("//div[@id='table_waiting_calls_wrapper']/div/button[3]/span").click()
    driver.find_element_by_xpath("//div[@id='table_waiting_calls_wrapper']/div/button/span").click()
    driver.find_element_by_xpath("//table[@id='table_waiting_calls']/tbody/tr/td").click()
    driver.find_element_by_xpath("//table[@id='table_waiting_calls']/tbody/tr/td").click()
    # ERROR: Caught exception [ERROR: Unsupported command [doubleClick | //table[@id='table_waiting_calls']/tbody/tr/td | ]]
    # Warning: waitForTextPresent may require manual changes
    for i in range(60):
        try:
            if re.search(r"^[\s\S]*//table\[@id='table_waiting_calls'\]/tbody/tr/td[\s\S]*$",
                         driver.find_element_by_css_selector("BODY").text): break
        except:
            pass
        time.sleep(1)
    else:
        self.fail("time out")
    driver.find_element_by_xpath("//div[@id='table_waiting_calls_wrapper']/div/button[2]/span").click()
    driver.find_element_by_xpath("//table[@id='table_waiting_calls']/tbody/tr/td").click()
    driver.find_element_by_xpath("//table[@id='table_waiting_calls']/tbody/tr/td").click()
    # ERROR: Caught exception [ERROR: Unsupported command [doubleClick | //table[@id='table_waiting_calls']/tbody/tr/td | ]]
    driver.find_element_by_xpath("//table[@id='table_waiting_calls']/tbody/tr/td").click()
    # Warning: waitForTextPresent may require manual changes
    for i in range(60):
        try:
            if re.search(r"^[\s\S]*//table\[@id='table_waiting_calls'\]/tbody/tr/td[\s\S]*$",
                         driver.find_element_by_css_selector("BODY").text): break
        except:
            pass
        time.sleep(1)
    else:
        self.fail("time out")
    driver.find_element_by_xpath("//div[@id='table_waiting_calls_wrapper']/div/button[3]/span").click()
    driver.find_element_by_xpath("//table[@id='table_waiting_calls']/tbody/tr/td").click()
    driver.find_element_by_xpath("//table[@id='table_waiting_calls']/tbody/tr/td").click()
    # ERROR: Caught exception [ERROR: Unsupported command [doubleClick | //table[@id='table_waiting_calls']/tbody/tr/td | ]]
    # Warning: waitForTextPresent may require manual changes
    for i in range(60):
        try:
            if re.search(r"^[\s\S]*//table\[@id='table_waiting_calls'\]/tbody/tr/td[\s\S]*$",
                         driver.find_element_by_css_selector("BODY").text): break
        except:
            pass
        time.sleep(1)
    else:
        self.fail("time out")
    driver.find_element_by_xpath("//div[@id='table_waiting_calls_wrapper']/div/button/span").click()
    driver.find_element_by_xpath("//table[@id='table_waiting_calls']/tbody/tr/td").click()
    driver.find_element_by_xpath("//table[@id='table_waiting_calls']/tbody/tr/td").click()
    # ERROR: Caught exception [ERROR: Unsupported command [doubleClick | //table[@id='table_waiting_calls']/tbody/tr/td | ]]
    driver.find_element_by_xpath("//table[@id='table_waiting_calls']/tbody/tr/td").click()
    # Warning: waitForTextPresent may require manual changes
    for i in range(60):
        try:
            if re.search(r"^[\s\S]*//table\[@id='table_waiting_calls'\]/tbody/tr/td[\s\S]*$",
                         driver.find_element_by_css_selector("BODY").text): break
        except:
            pass
        time.sleep(1)
    else:
        self.fail("time out")
    driver.find_element_by_id("table_waiting_calls_wrapper").click()
    """