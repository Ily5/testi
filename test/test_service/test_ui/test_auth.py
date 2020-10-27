import allure 


@allure.feature("Авторизация в цмс")
@allure.story("Проверка наличия элементов на странице")


def test_auth_cms(app):
    app.page.check_navigate_elements()
