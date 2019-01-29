import smtplib
from email.mime.multipart import MIMEMultipart
from unittest import mock
from unittest.mock import Mock

import pytest

from emails import _generate_email_message, _smtp_login, SendEmailException, \
    _send, get_smtp_connection, send_email


@pytest.fixture
def smtpserver_mock():
    return Mock(smtplib.SMTP)


@pytest.fixture
def message_mock():
    return Mock(MIMEMultipart('alternative'))


@mock.patch('emails._get_smtp_connection', return_value=smtpserver_mock())
@mock.patch('emails._smtp_login', return_value=smtpserver_mock())
def test__get_smtp_connection(mocked_get_smtp_connection, mocked_smtp_login):
    with get_smtp_connection() as smtp_server:  # noqa
        pass
    mocked_get_smtp_connection.assert_called_once()
    mocked_smtp_login.assert_called_once()


def test__smtp_login(smtpserver_mock):
    user = 'fake user'
    password = 'fake password'
    smtpserver = _smtp_login(smtpserver_mock, user, password)
    assert smtpserver
    smtpserver_mock.login.assert_called_once()


def test__smtp_login_fail(smtpserver_mock):
    user = 'fake user'
    password = 'fake password'
    smtpserver_mock.login.side_effect = smtplib.SMTPException()
    with pytest.raises(SendEmailException):
        _smtp_login(smtpserver_mock, user, password)
    smtpserver_mock.login.assert_called_once()


def test__generate_email_message():
    subject = 'testing subject'
    from_address = 'testing@test.com'
    to_address = 'testing2@test.com'
    text_message = 'test messages'
    html_message = '<p>test html messages</p>'
    message = _generate_email_message(subject, from_address,
                                      to_address,
                                      text_message, html_message)
    assert ('Subject', subject) in message._headers
    assert ('From', from_address) in message._headers
    assert ('To', to_address) in message._headers
    assert len(message._payload) == 2
    assert message._payload[0]._payload == text_message
    assert message._payload[1]._payload == html_message


def test__send(smtpserver_mock, message_mock):
    from_address = 'testing@test.com'
    to_address = 'testing2@test.com'
    _send(smtpserver_mock, from_address, to_address, message_mock)
    smtpserver_mock.sendmail.assert_called_once()


@mock.patch('emails._generate_email_message', return_value=message_mock())
@mock.patch('emails.get_smtp_connection', yield_value=smtpserver_mock())
@mock.patch('emails._send')
def test_send_email_ok(generate_email_message_mock, get_smtp_connection_mock,
                       _send_mock):
    subject = 'testing subject'
    text_message = 'test messages'
    to_address = 'testing2@test.com'
    send_email(subject, text_message, to_address=to_address)


@mock.patch('emails._generate_email_message', return_value=message_mock())
@mock.patch('emails.get_smtp_connection', yield_value=smtpserver_mock())
@mock.patch('emails._send', side_effect=smtplib.SMTPException)
def test_send_email_ko(generate_email_message_mock, get_smtp_connection_mock,
                       _send_mock):
    subject = 'testing subject'
    text_message = 'test messages'
    to_address = 'testing2@test.com'
    send_email(subject, text_message, to_address=to_address)
    generate_email_message_mock.assert_called_once()
    get_smtp_connection_mock.assert_called_once()
    _send_mock.assert_called_once()
