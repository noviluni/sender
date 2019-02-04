import smtplib
import socket

from contextlib import contextmanager

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import (
    FROM_ADDRESS,
    EMAIL_PASSWORD,
    DEFAULT_TO_ADDRESS,
    SMTP_HOST,
    SMTP_PORT
)


class SendEmailException(Exception):
    def __init__(self, message):
        super().__init__(message)


@contextmanager
def get_smtp_connection(smtp_host=SMTP_HOST, port=SMTP_PORT):
    from_address = FROM_ADDRESS
    email_password = EMAIL_PASSWORD

    smtp_server = None

    try:
        smtp_server = _get_smtp_connection(smtp_host, port)
        smtp_server = _smtp_login(smtp_server, from_address, email_password)

        yield smtp_server

    finally:
        if smtp_server:
            smtp_server.close()


def _get_smtp_connection(smtp_host, port):
    """
    Connects to SMTP_HOST and returns the connexion.

    :param smtp_host:
    :param port:
    :return: smtpserver (SMTP object)
    """
    try:
        smtp_server = smtplib.SMTP(smtp_host, port)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        return smtp_server

    except (socket.gaierror,
            socket.error,
            socket.herror,
            smtplib.SMTPException) as e:
        msg = f'Error connection to SMTP server. Error: {e}'
        raise SendEmailException(msg)


def _smtp_login(smtpserver, user, password):
    """
    Login "user" to the "smtpserver" using the provided "password".

    :param smtpserver:
    :param user:
    :param password:
    """
    try:
        smtpserver.login(user, password)
        return smtpserver

    except smtplib.SMTPException as e:
        msg =\
            f'Incorrect authentication data or attempt blocked by SMTP' \
            f' server. Error: {e}'
        raise SendEmailException(msg)


def _generate_email_message(subject, from_address, to_address,
                            text_message, html_message):
    """
    Generates a message to be sent.

    :param subject:
    :param from_address:
    :param to_address:
    :param text_message:
    :param html_message:
    :return: msg (MimeMultipart object)
    """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address
    part1 = MIMEText(text_message, 'plain')
    msg.attach(part1)

    if html_message:
        part2 = MIMEText(html_message, 'html')
        msg.attach(part2)

    return msg


def _send(smtpserver, from_address, to_address, message):
    """
    Given a logged SMTP server, a "from_address",
    a "to_address" and a "message", sends the message through the SMTP server.

    :param smtpserver:
    :param from_address:
    :param to_address:
    :param message:
    """
    smtpserver.sendmail(from_address, to_address, message.as_string())


def send_email(subject, text_message,
               html_message=None, to_address=DEFAULT_TO_ADDRESS):
    """
    Given a "subject", a "text_message" and optionally a
    "html_message" and a "to_address", send an e-mail through smtp.

    Returns True if e-mail has been sent, else returns False.
    """
    from_address = FROM_ADDRESS
    msg = _generate_email_message(subject, from_address, to_address,
                                  text_message, html_message)

    try:
        with get_smtp_connection() as smtp_server:
            _send(smtp_server, from_address, to_address, msg)
            return True

    except smtplib.SMTPException:
        return False
