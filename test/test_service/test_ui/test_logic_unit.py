import pytest
import allure
from model.logic_unit import Logic
from fixture.page import generate


# def get_value(db):
#     db.db_conn

lu = Logic(generate("logic_"))


@allure.feature("Проверка работы логикой")
@allure.story("Создание создание logic unit")
def test_create_logic_unit(app):
    app.page.create_logic_unit(lu)


@allure.feature("Проверка работы логикой")
@allure.story("Создание actions")
def test_fill_logic_unit(app):
    app.page.open_logic_unit(lu.name)
    app.page.fill_logic_unit(lu.actions)

# TODO:this


# @allure.feature("Проверка работы логикой")
# @allure.story("Заполнение данными")
# def test_send_data_logic_unit(app):
#     app.page.send_data_lu()
#
#
# @allure.feature("Проверка работы логикой")
# @allure.story("Удаление созданных actions")
# def test_delete_logic_actions(app):
#     app.page.delete_actions()
#
#
# @allure.feature("Проверка работы логикой")
# @allure.story("Проверка работы с xml")
# def test_xml(app):
#     pass