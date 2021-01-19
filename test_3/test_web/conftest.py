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
        fixture = ApplicationNewVersion(browser=browser, cms_url=config["CmsUrl3"], test_data=config['v3'],
                                        database=None)
        fixture.wd.get(fixture.cms_url)
        fixture.LoginPage.login_in_cms(username=fixture.test_data['auth']['login'],
                                       password=fixture.test_data['auth']['pass'])
        time.sleep(3)

    def done():
        fixture.cancel()

    request.addfinalizer(done)
    return fixture


@pytest.fixture(scope='class')
def agent_settings_page(request, app_3_web):
    agent_setting_url = app_3_web.test_data['agent_setting_url'] + app_3_web.test_data['test_data']['agent_uuid']
    app_3_web.BasePage.goto_page(agent_setting_url)

    def fin():
        main_page_url = app_3_web.test_data['main_page_url']
        app_3_web.BasePage.goto_page(main_page_url)

    request.addfinalizer(fin)
    return app_3_web


@pytest.fixture(scope='class')
def data_uploading(agent_settings_page):
    agent_settings_page.AnyAgentPage.open_data_uploading_page()
    return agent_settings_page


@pytest.fixture(scope='class')
def queue_page(agent_settings_page):
    agent_settings_page.AnyAgentPage.open_queue_page()
    return agent_settings_page.QueuePage
