import pytest
import json
from test_3.fixture.api import APIClientV3


@pytest.fixture(scope='session')
def api_v3(request):
    fixture = None
    if fixture is None:
        with open(request.config.getoption("--config")) as cfg:
            config = json.load(cfg)
            fixture = APIClientV3(base_url=config['v3']['api']['api_base_url'],
                                  company_uuid=config['v3']['test_data']['company_uuid'])

            fixture.token = fixture.get_token(password=config['v3']['auth']['pass'],
                                              login=config['v3']['auth']['login'])

    return fixture

# TODO добавить конфиги v3 в соотвествующие данные
