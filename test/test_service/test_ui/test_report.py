import allure


@allure.feature("Проверка системы отчётов")
@allure.story("Выгружаем offline и online report")


def test_report(app):
    app.page.get_report()