import string
import random
import os
import time
import json

import pytest

from fixture.application import Application
from fixture.database import Connector, MongoConnector
from test_3.fixture.Helper import FileHelper, SshHelper

from test_3.fixture.application_3 import ApplicationNewVersion

from test_3.fixture.ApiWF.ExternalApi import ExternalApi
from test_3.fixture.ApiWF.CmsApi import CmsApi
from test_3.fixture.ApiWF.PoolApi import PoolApi
from test_3.fixture.ApiWF.NluApi import NluApi

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

""" Фикстуры для V2"""


@pytest.fixture(scope="session")
def app(request):
    # global fixture
    fixture = None
    if fixture is None:
        browser = request.config.getoption("--browser")
        with open(request.config.getoption("--config")) as cfg:
            config = json.load(cfg)
            fixture = Application(
                browser=browser,
                cms_url=config["CmsUrl"],
                api_url=config["ApiEndpoint"],
                api_headers=config["ApiHeaders"],
                api_methods=config["ApiMethods"],
                pool_api=config["PoolApiUrl"],
                p_api_headers=config["PoolApiHeaders"],
                project=config["ProjectId"],
                rwdb=config["Postgres"]["RW"],
                cms_db=config["Postgres"]["CMS"],
                mdb=config["Mongo_client"],
                speech_engine=config["speech_engine"],
                database=config["database"],
            )
            fixture.session.login(
                username=config["UsernameCms"], password=config["PasswordCms"]
            )

    def done():
        try:
            fixture.session.logout(username=config["UsernameCms"])
            fixture.cancel()
        except:
            pass

    request.addfinalizer(done)
    return fixture


""" Фикстуры для V3"""


@pytest.fixture(scope="session")
def api_v3(request):
    fixture = None
    if fixture is None:
        with open(request.config.getoption("--config")) as cfg:
            config = json.load(cfg)
            with open(ROOT_DIR + "/config_v3.json", "r", encoding="UTF-8") as conf:
                config_v3 = json.load(conf)
                fixture = ExternalApi(
                    base_url=config["api"]["external_api_base_url"],
                    test_data=config["test_data"],
                    path_end_point=config_v3["api"]["external_api"],
                    database=config["Postgres"],
                )
                token, refresh_token = fixture.get_api_token(
                    password=config["auth"]["pass"], login=config["auth"]["login"]
                )
            fixture.token, fixture.refresh_token = token, refresh_token

    return fixture


@pytest.fixture(scope="session")
def cms_api_v3(request):
    fixture = None
    if fixture is None:
        with open(request.config.getoption("--config")) as cfg:
            config = json.load(cfg)
            with open(ROOT_DIR + "/config_v3.json", "r", encoding="UTF-8") as conf:
                config_v3 = json.load(conf)
                fixture = CmsApi(
                    base_url=config["api"]["external_api_base_url"],
                    test_data=config["test_data"],
                    path_end_point=config_v3["api"]["cms_api"],
                    database=config["Postgres"],
                )
                token, refresh_token = fixture.get_api_token(
                    password=config["auth"]["pass"], login=config["auth"]["login"]
                )
            fixture.token, fixture.refresh_token = token, refresh_token

    return fixture


@pytest.fixture(scope="session")
def nlu_api_v3(request):
    fixture = None
    if fixture is None:
        with open(request.config.getoption("--config")) as cfg:
            config = json.load(cfg)
            with open(ROOT_DIR + "/config_v3.json", "r", encoding="UTF-8") as conf:
                config_v3 = json.load(conf)
                fixture = NluApi(
                    base_url=config["api"]["nlu_api_url"],
                    path_end_point=config_v3["api"]["nlu_api"],
                )
    return fixture


@pytest.fixture(scope="session")
def pool_api_v3(request):
    fixture = None
    if fixture is None:
        with open(request.config.getoption("--config")) as cfg:
            config = json.load(cfg)
            with open(ROOT_DIR + "/config_v3.json", "r", encoding="UTF-8") as conf:
                config_v3 = json.load(conf)
                fixture = PoolApi(
                    base_url=config["api"]["poll_api_v3_url"],
                    test_data=config["test_data"],
                    path_end_point=config_v3["api"]["poll_api"],
                )
    return fixture


@pytest.fixture(scope="class")
def app_3_web(request):
    fixture = None
    if fixture is None:
        browser = request.config.getoption("--browser")
        with open(request.config.getoption("--config")) as cfg:
            config = json.load(cfg)
        fixture = ApplicationNewVersion(
            browser=browser, cms_url=config["CmsUrl3"], test_data=config, database=None
        )
        fixture.wd.get(fixture.cms_url)
        fixture.LoginPage.login_in_cms(
            username=fixture.test_data["auth"]["login"],
            password=fixture.test_data["auth"]["pass"],
        )
        time.sleep(3)

    def done():
        fixture.cancel()

    request.addfinalizer(done)
    return fixture


"""Общие фикстуры """


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


@pytest.fixture()
def file_helper(api_v3):
    helper = FileHelper(path_to_file="/var/jenkins_home/call_files/", api_helper=api_v3)
    # helper = FileHelper(path_to_file='/home/renat/', api_helper=api_v3)
    return helper


@pytest.fixture()
def ssh_helper(request):
    with open(request.config.getoption("--config")) as cfg:
        config = json.load(cfg)
        fixture = SshHelper(
            username=config["test_data"]["ssh"]["login"],
            hosts=config["test_data"]["ssh"]["hosts"],
        )

    return fixture


@pytest.fixture
def random_str_generator(
        size=random.randint(3, 129),
        chars=string.ascii_uppercase + string.digits + string.ascii_lowercase + "\t",
):
    return "".join(random.choice(chars) for _ in range(size))


@pytest.fixture()
def get_asr_engine(request):
    return request.config.getoption("--asr")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="remote")
    parser.addoption("--config", action="store", default=ROOT_DIR + "/config_prod.json")
    parser.addoption(
        "--asr",
        action="store",
        default="yandex",
        help="Set ASR engine: yandex or google",
    )

# TODO : make universal parametrize method in future
# def pytest_make_parametrize_id(val):
#     return repr(val)
