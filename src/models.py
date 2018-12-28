import datetime

from flask_sqlalchemy import SQLAlchemy

from conf import DEFAULT_TO_ADDRESS
from utils import send_email

db = SQLAlchemy()


class Email(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    from_address = db.Column(db.String(200), nullable=False)  # TODO: Add email validation
    to_address = db.Column(db.String(200), nullable=False, default=DEFAULT_TO_ADDRESS)  # TODO: Add email validation

    subject = db.Column(db.String(255), nullable=False)
    text_message = db.Column(db.String(200), nullable=False)  # TODO: Define bigger body?
    html_message = db.Column(db.String(200))  # TODO: Define bigger body?

    created_at = db.Column(db.DateTime, nullable=False)
    sent = db.Column(db.Boolean(), server_default=False, nullable=False)
    sent_at = db.Column(db.DateTime)
    retries = db.Column(db.Integer, server_default=0)

    def __repr__(self):
        return '<Email {} - {}: {}>'.format(self.id, self.to_address, self.subject)

    def __init__(self, from_address, to_address, subject, text_message, html_message, sent=False):
        self.from_address = from_address  # TODO: Add email validation
        self.to_address = to_address  # TODO: Add email validation
        self.subject = subject
        self.text_message = text_message
        self.html_message = html_message
        self.created_at = datetime.datetime.now()
        self.sent = sent

    def send(self, fnx=send_email):
        self.retries += 1
        email_data = self.get_email_data()
        sent = fnx(**email_data)

        if sent:
            self.sent = True
            self.sent_at = datetime.datetime.now()
        return sent
    
    def get_email_data(self):
        email_data = {'subject': self.subject,
                      'text_message': self.text_message,
                      'html_message': self.html_message,
                      'to_address': self.to_address}
        return email_data
