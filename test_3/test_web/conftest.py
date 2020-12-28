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
        fixture.LoginPage.login_in_cms(username=fixture.test_data['auth']['login'],
                                       password=fixture.test_data['auth']['pass'])
        time.sleep(3)

    def done():
        fixture.cancel()

    request.addfinalizer(done)
    return fixture


@pytest.fixture()
def app_v3(request, app_3_web):
    def fin():
        main_page_url = app_3_web.test_data['main_page_url']
        app_3_web.BasePage.goto_page(main_page_url)

    request.addfinalizer(fin)
    return app_3_web


@pytest.fixture()
def agent_settings_page(app_v3):
    agent_setting_url = app_v3.test_data['agent_setting_url'] + app_v3.test_data['test_data']['agent_uuid']
    app_v3.BasePage.goto_page(agent_setting_url)
    return app_v3
