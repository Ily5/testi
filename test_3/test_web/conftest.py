import pytest


@pytest.fixture(scope='class')
def agent_settings_page(app_3_web):
    agent_setting_url = app_3_web.test_data['agent_setting_url'] + app_3_web.test_data['test_data']['agent_uuid']
    app_3_web.BasePage.goto_page(agent_setting_url)
    return app_3_web


@pytest.fixture()
def go_to_agent_settings(request, agent_settings_page):
    def fin():
        agent_settings_page.AnyAgentPage.open_agent_settings_page()

    request.addfinalizer(fin)


@pytest.fixture()
def data_uploading(agent_settings_page, go_to_agent_settings):
    agent_settings_page.AnyAgentPage.open_data_uploading_page()
    return agent_settings_page


@pytest.fixture(scope='class')
def queue_page(agent_settings_page):
    agent_settings_page.AnyAgentPage.open_queue_page()
    return agent_settings_page.QueuePage


@pytest.fixture(scope='function')
def cancel_filter_queue(queue_page):
    yield
    queue_page.cancel_queue_page_filter()
