from fixture.application import Application
from fixture.database import Connector, MongoConnector
from test_3.fixture.application_3 import ApplicationNewVersion
import pytest
import json
import sys
import os
import random
import string

fixture = None

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session")
def app(request):
    global fixture
    if fixture is None:
        browser = request.config.getoption("--browser")
        with open(request.config.getoption("--config")) as cfg:
            config = json.load(cfg)
            fixture = Application(browser=browser, cms_url=config["CmsUrl"], api_url=config["ApiEndpoint"],
                                  api_headers=config["ApiHeaders"], api_methods=config["ApiMethods"],
                                  pool_api=config["PoolApiUrl"], p_api_headers=config["PoolApiHeaders"],
                                  project=config["ProjectId"], rwdb=config["Postgres"]["RW"],
                                  cms_db=config["Postgres"]["CMS"], mdb=config["Mongo_client"], speech_engine=config["speech_engine"],
                                  database=config["database"])
            fixture.session.login(username=config["UsernameCms"], password=config["PasswordCms"])

    def done():
        try:
            fixture.session.logout(username=config["UsernameCms"])
            fixture.cancel()
        except:
            pass

    request.addfinalizer(done)
    return fixture


@pytest.fixture(scope="session")
# @pytest.fixture()
def app_3(request):
    global fixture
    if fixture is None:
        browser = request.config.getoption("--browser")
        with open(request.config.getoption("--config")) as cfg:
            config = json.load(cfg)
            fixture = ApplicationNewVersion(browser=browser, cms_url=config["CmsUrl3"], database=config["database"])
            # fixture.session.login(username=config["UsernameCms"], password=config["PasswordCms"])

    def done():
        try:
            # fixture.session.logout(username=config["UsernameCms"])
            fixture.cancel()
        except:
            pass

    request.addfinalizer(done)
    return fixture


@pytest.fixture(scope="session")
def db(request):
    with open(request.config.getoption("--config")) as cfg:
        config = json.load(cfg)
        fixture = Connector(data=config["Postgres"]["RW"])
    request.addfinalizer(fixture.cancel)
    return fixture


@pytest.fixture(scope="session")
def mdb(request):
    with open(request.config.getoption("--config")) as cfg:
        config = json.load(cfg)
        # fixture = MongoConnector(data=config["Postgres"]["RW"])
        fixture = MongoConnector(str(config["Mongo_client"]))
    request.addfinalizer(fixture.cancel)
    return fixture


@pytest.fixture
def random_str_generator(size=random.randint(3, 129),
                         chars=string.ascii_uppercase + string.digits + string.ascii_lowercase + '\t'):
    return ''.join(random.choice(chars) for _ in range(size))


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="remote")
    parser.addoption("--config", action="store", default=ROOT_DIR + "/config_test.json")
