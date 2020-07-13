from fixture.application import Application
from fixture.database import Connector
import pytest


# fixture = None

@pytest.fixture(scope="session")
def app(request):
    fixture = Application()
    fixture.session.login(username="ikoshkin", password="123456")

    def done():
        try:
            fixture.session.logout(username="ikoshkin")
            fixture.cancel()
        except:
            pass

    request.addfinalizer(done)
    return fixture


@pytest.fixture(scope="session")
def db(request):
    fixture = Connector()
    request.addfinalizer(fixture.cancel)
    return fixture
