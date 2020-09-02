import allure

@allure.feature("Работа с call_logs")
@allure.story("получение call_log")
def test_report(app):
    app.page.get_log()