# -*- coding: utf-8 -*-
import pytest
from application import Application


@pytest.fixture
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.cancel)
    return fixture


def test_auth_cms(app):
    # go to cms
    app.open_cms()
    # для работы с полем  есть методы click(), clear()\
    app.login("ikoshkin", "123456")
    app.check()
    app.wd.find_element_by_xpath("//button[@type='submit']").click()


if __name__ == "__main__":
    pytest.main()
