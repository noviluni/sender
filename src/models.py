from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

from conf import DEFAULT_TO_ADDRESS
from emails import send_email

db = SQLAlchemy()


class Email(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    from_address = db.Column(db.String(200), nullable=False)
    to_address = db.Column(db.String(200), nullable=False, default=DEFAULT_TO_ADDRESS)

    subject = db.Column(db.String(255), nullable=False)
    text_message = db.Column(db.String(200), nullable=False)  # TODO: Define bigger body?
    html_message = db.Column(db.String(200))  # TODO: Define bigger body?

    created_at = db.Column(db.DateTime, nullable=False)
    sent = db.Column(db.Boolean(), server_default='f', nullable=False)
    sent_at = db.Column(db.DateTime)
    retries = db.Column(db.Integer, server_default='0')

    def __repr__(self):
        return '<Email {self.id} - {self.to_address}: {self.subject}>'

    def __init__(self, from_address, to_address, subject, text_message, html_message, created_at=None, sent=False):
        self.from_address = from_address
        self.to_address = to_address
        self.subject = subject
        self.text_message = text_message
        self.html_message = html_message
        self.created_at = datetime.utcnow() if created_at is None else created_at
        self.sent = sent
    
    @validates('from_address', 'to_address')
    def _validate_email(self, key, address):
        assert '@' in address
        return address

    def send(self, sender_function=send_email):
        if self.retries is None:
            self.retries = 1
        else:
            self.retries += 1
        email_data = self.get_email_data()
        sent = sender_function(**email_data)

        if sent:
            self.sent = True
            self.sent_at = datetime.utcnow()
        return sent
    
    def get_email_data(self):
        return {
            'subject': self.subject,
            'text_message': self.text_message,
            'html_message': self.html_message,
            'to_address': self.to_address
        }
