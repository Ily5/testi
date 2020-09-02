import allure


@allure.feature("Работа с record prompts")
@allure.story("Создание prompt")
def test_add_prompt(app):
    app.page.add_prompt("py_test_run_prompt", "desc")


@allure.feature("Работа с record prompts")
@allure.story("Изменение prompt")
def test_edit_prompt(app):
    # app.page.add_prompt("py_test_run_prompt", "desc")
    app.page.recordprompt()
