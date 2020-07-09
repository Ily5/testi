def test_add_prompt(app):
    app.page.add_prompt("py_test_run_prompt", "desc")


def test_edit_prompt(app):
    app.page.add_prompt("py_test_run_prompt", "desc")
    app.page.edit_prompt()
