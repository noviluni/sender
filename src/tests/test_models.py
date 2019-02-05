from unittest import mock

import pytest

from models import Email


def test__validate_email(email):
    email = Email.query.filter_by(id=email.id).first()
    assert email._validate_email('from_address', 'hola@hola.com')
    with pytest.raises(AssertionError):
        email._validate_email('from_address', 'hola')


def test_get_email_data(email):
    email = Email.query.filter_by(id=email.id).first()
    data = email.get_email_data()
    assert len(data) == 4
    assert data.get('subject') == 'test_subject'
    assert data.get('text_message') == 'test_text_message'
    assert data.get('html_message') == 'test_text_message'
    assert data.get('to_address') == 'test2@test.com'


def fake_sender_function_ok(**kwargs):
    return True


def fake_sender_function_ko(**kwargs):
    return False


@mock.patch('models.Email.get_email_data', return_value={})
def test_send_ok(get_email_data_mocked, email):
    email = Email.query.filter_by(id=email.id).first()
    assert email.retries == 0
    assert not email.sent_at
    sent = email.send(sender_function=fake_sender_function_ok)
    assert sent
    assert email.retries == 1
    assert email.sent_at
    get_email_data_mocked.assert_called_once()

    email.send(sender_function=fake_sender_function_ok)
    assert email.retries == 2
    assert get_email_data_mocked.call_count == 2


@mock.patch('models.Email.get_email_data', return_value={})
def test_send_ko(get_email_data_mocked, email):
    email = Email.query.filter_by(id=email.id).first()
    assert email.retries == 0
    assert not email.sent_at
    sent = email.send(sender_function=fake_sender_function_ko)
    assert not sent
    assert email.retries == 1
    assert not email.sent_at
    get_email_data_mocked.assert_called_once()
