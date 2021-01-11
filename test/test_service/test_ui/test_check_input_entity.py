import allure
import time


@allure.feature("Работа с entities")
@allure.story("Создание сущности")
def test_create_in_entity(app):
    time.sleep(60)
    app.page.create_in_entity("py_test_entity", "run_entity")


@allure.feature("Работа с entities")
@allure.story("Удаление сущности")
def test_delete_in_entity(app):
    app.page.delete_in_entity()
