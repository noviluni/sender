from datetime import datetime

import pytest

from api import create_app

from models import db as _db, Email


@pytest.yield_fixture(scope='session', autouse=True)
def app():
    _app = create_app()
    ctx = _app.test_request_context()
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


@pytest.fixture
def email(db):
    email = Email(
        from_address='test@test.com',
        to_address='test2@test.com',
        subject='test_subject',
        text_message='test_text_message',
        html_message='test_text_message',
    )
    db.session.add(email)
    db.session.commit()
    return email


@pytest.fixture(scope='function')
def email_sent(db):
    email = Email(
        from_address='test@test.com',
        to_address='test2@test.com',
        subject='test_subject',
        text_message='test_text_message',
        html_message='test_text_message',
        sent=True,
    )
    email.sent_at = datetime.now()
    db.session.add(email)
    db.session.commit()
    return email
