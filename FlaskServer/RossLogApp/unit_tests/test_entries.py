import pytest

from RossLogApp.log_factory import get_logger

from .. import create_app
from ..extensions import db

logger = get_logger(__name__)


@pytest.fixture(scope='session')
def app():
    logger.test("Test app instance being created...")
    app = create_app("sqlite://")   # passing this "sqlite://" will make a test db in memory, rather than on file!
    app.config['TESTING'] = True
    yield app


@pytest.fixture(scope='session')
def test_db(app):
    logger.test("Creating test db instance...")
    with app.app_context():
        # set up
        db.create_all()
        yield db
        # tear down
        #db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    logger.test("Getting test client...")
    return app.test_client()    # allows us to simulate requests to the client