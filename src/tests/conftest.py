import pytest

from api import create_app

from models import db as _db


@pytest.yield_fixture(scope='session', autouse=True)
def app():
    _app = create_app()
    _app.testing = True
    _app.config['DEBUG'] = False
    _app.config['ENV'] = 'test'
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
    _app.config['FROM_ADDRESS'] = 'test_from_email@test.com'
    _app.config['DEFAULT_TO_ADDRESS'] = 'test_to_email@test.com'
    ctx = _app.app_context()
    ctx.push()
    yield _app

    ctx.pop()


@pytest.yield_fixture(autouse=True)
def db(app):
    _db.app = app
    _db.create_all()
    yield _db

    _db.session.remove()
    _db.drop_all()


@pytest.fixture(autouse=True)
def client(app):
    with app.test_request_context():
        return app.test_client()
