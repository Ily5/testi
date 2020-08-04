from model.project import Project
import allure


@allure.feature("Проверка работы с проектами")
@allure.story("Создание проекта")
def test_add_project(app):
    app.page.add_project(
        Project("name_new", "desc_edit", "00:00", "00:01", "00:01", "0", "sip-client-local", "pytest_project",
                "api-test.neuro.net", "test_hello_main", "{msisdn}_{uuid}", "1", "set_data_before_call", "1",
                "2", "3", "jane@yandex"
                ))


@allure.feature("Проверка работы с проектами")
@allure.story("Изменение проекта")
def test_edit_project(app):
    app.page.edit(
        Project("name_edit", "desc_edit", "00:00", "00:01", "00:01", "0", "sip-client-local", "pytest_project",
                "api-test.neuro.net", "test_hello_main", "{msisdn}_{uuid}", "1", "set_data_before_call", "1",
                "2", "3", "jane@yandex"
                ))




    """
    project - create 
    project - edit 
    """
