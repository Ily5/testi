import time
import pytest
import json
from test_3.fixture.application_3 import ApplicationNewVersion


@pytest.fixture(scope='class')
def app_3_web(request):
    fixture = None
    if fixture is None:
        browser = request.config.getoption("--browser")
        with open(request.config.getoption("--config")) as cfg:
            config = json.load(cfg)
        fixture = ApplicationNewVersion(browser='chrome', cms_url=config["CmsUrl3"], test_data=config['v3'],
                                        database=None)
        fixture.wd.get(fixture.cms_url)
        time.sleep(3)

    def done():
        fixture.cancel()

    request.addfinalizer(done)
    return fixture


@pytest.fixture()
def app_v3(request, app_3_web):
    app_3_web.LoginPage.login_in_cms(username=app_3_web.test_data['auth']['login'],
                                     password=app_3_web.test_data['auth']['pass'])

    def fin():
        app_3_web.AnyPage.logout()

    request.addfinalizer(fin)
    return app_3_web
