def test_create_in_entity(app):
    app.page.create_in_entity("py_test_entity", "run_entity")


def test_delete_in_entity(app):
    app.page.delete_in_entity()
