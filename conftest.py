from fixture.application import Application
import pytest


# fixture = None

@pytest.fixture (scope="session")
def app(request):
    fixture = Application()
    fixture.session.login(username="ikoshkin", password="123456")

    def done():
        fixture.session.logout(username="ikoshkin")
        fixture.cancel()

    request.addfinalizer(done)
    return fixture

#
# ------
#from fixture.database import Connector
#@pytest.fixture
#def db(request):
#    fixture = Connector()
#    request.addfinalizer(fixture.cancel)
#    return fixture
# -------
#