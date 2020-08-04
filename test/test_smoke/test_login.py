import allure


@allure.feature("Проверка логина через cms")
def test_auth_cms(app):
    with allure.step("Проверяем наличие элементов на странице"):
        app.page.check_navigate_elements()

