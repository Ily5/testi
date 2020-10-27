from model.project import Project
from fixture.page import generate
import allure


@allure.feature("Проверка работы с проектами")
@allure.story("Создание проекта")
def test_add_project(app):
    name = generate("project_name_")
    app.page.add_project(
        Project(name, "desc_edit", "00:00", "00:01", "00:01", "0", "sip-client-local", "pytest_project",
                "api-test.neuro.net", "test_hello_main", "{msisdn}_{uuid}", "1", "set_data_before_call", "1",
                "2", "3", "jane@yandex"
                ))


@allure.feature("Проверка работы с проектами")
@allure.story("Изменение проекта")
def test_edit_project(app):
    name = generate("project_name_")
    app.page.edit_project(
        Project(name, "desc_edit", "00:00", "00:01", "00:01", "0", "sip-client-local", "pytest_project",
                "api-test.neuro.net", "test_hello_main", "{msisdn}_{uuid}", "1", "set_data_before_call", "1",
                "2", "3", "jane@yandex", "yandex"
                ))
    # app.page.edit(Project())


@allure.feature("Проверка работы с проектами")
@allure.story("Изменение параметров распознавания")

def test_change_voice_params(app):
    app.page.edit_voice_param(Project(tts="ru-RU-Wavenet-A@google", asr="google"))
