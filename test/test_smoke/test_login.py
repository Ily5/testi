import allure


@allure.feature("go to cms page")
@allure.story("Тестовый отчёт проверяем работу cms")
def test_auth_cms(app):
    app.page.check_navigate_elements()
