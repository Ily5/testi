from fixture.application import Application
from fixture.database import Connector, MongoConnector
import pytest
import json
import sys
import os

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
                                  cms_db=config["Postgres"]["CMS"], mdb=config["Mongo_client"])
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
def db(request):
    with open(request.config.getoption("--config")) as cfg:
        config = json.load(cfg)
        fixture = Connector(data=config["Postgres"]["RW"])
    request.addfinalizer(fixture.cancel)
    return fixture

# @pytest.fixture(scope="session")
# def api(request):
#     with open(request.config.getoption("--config")) as cfg:
#         config = json.load(cfg)
#         fixture = Connector(data=config["Postgres"]["RW"])
#     request.addfinalizer(fixture.cancel)
#     return fixture


@pytest.fixture(scope="session")
def mdb(request):
    with open(request.config.getoption("--config")) as cfg:
        config = json.load(cfg)
        # fixture = MongoConnector(data=config["Postgres"]["RW"])
        fixture = MongoConnector(str(config["Mongo_client"]))
    request.addfinalizer(fixture.cancel)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="Remote")
    parser.addoption("--config", action="store", default=ROOT_DIR + "\config_prod.json")
