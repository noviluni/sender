import datetime

from flask_sqlalchemy import SQLAlchemy

from utils import send_email

db = SQLAlchemy()


class Email(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    from_address = db.Column(db.String(200))  # TODO: Add email validation
    to_address = db.Column(db.String(200))  # TODO: Add email validation

    subject = db.Column(db.String(255))
    text_message = db.Column(db.String(200))  # TODO: Define bigger body?
    html_message = db.Column(db.String(200))  # TODO: Define bigger body?

    created_at = db.Column(db.DateTime, nullable=False)
    sent = db.Column(db.Boolean(), default=False, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=True)
    retries = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Email {} - {}: {}>'.format(self.id, self.to_address, self.subject)

    def __init__(self, from_address, to_address, subject, text_message, html_message):
        self.from_address = from_address
        self.to_address = to_address
        self.subject = subject
        self.text_message = text_message
        self.html_message = html_message
        self.created_at = datetime.datetime.now()

    def send(self):

        sent = send_email(**self.__dict__)
        self. retries += 1

        if sent:
            self.sent = True
            self.sent_at = datetime.datetime.now()
            db.session.commit()
            return True
        else:
            db.session.commit()
            return False
