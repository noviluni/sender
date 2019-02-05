from flask import Blueprint, jsonify, abort, request

import config
from models import Email, db

mod = Blueprint('emails', __name__)


@mod.route('/emails/', endpoint='email_list', methods=['GET'])
def email_list():
    limit = int(request.args.get('limit', 10))
    sent = request.args.get('sent')

    if sent == 'true':
        emails = Email.query.filter_by(sent=True).\
            order_by(Email.id).limit(limit).all()
    elif sent == 'false':
        emails = Email.query.filter_by(sent=False).\
            order_by(Email.id).limit(limit).all()
    else:
        emails = Email.query.order_by(Email.id).limit(limit).all()

    return jsonify([
        {
            'id': email.id,
            'from_address': email.from_address,
            'to_address': email.to_address,
            'subject': email.subject,
            'text_message': email.text_message,
            'html_message': email.html_message,
            'created_at': email.created_at,
            'sent': email.sent,
            'sent_at': email.sent_at,
            'retries': email.retries,
        }
        for email in emails
    ])


@mod.route('/emails/', endpoint='create_email', methods=['POST'])
def create_email():
    autosend = request.args.get('autosend')

    json = request.get_json()

    if not json or 'subject' not in json or 'text_message' not in json:
        abort(400)

    to_address = json.get('to_address')
    subject = json.get('subject')
    text_message = json.get('text_message')
    html_message = json.get('html_message')

    from_address = config.FROM_ADDRESS

    new_email = Email(
        from_address=from_address,
        to_address=to_address if to_address else config.DEFAULT_TO_ADDRESS,
        subject=subject,
        text_message=text_message,
        html_message=html_message
    )

    sent = 'false'
    if autosend == 'true':
        sent_result = new_email.send()
        sent = 'true' if sent_result else 'false'

    db.session.add(new_email)
    db.session.commit()
    return jsonify({'id': new_email.id, 'sent': sent}), 201


@mod.route('/emails/<int:email_id>', endpoint='email_detail', methods=['GET'])
def email_detail(email_id):
    email = Email.query.filter_by(id=email_id).first()

    if not email:
        abort(404)

    return jsonify(
        {
            'id': email.id,
            'from_address': email.from_address,
            'to_address': email.to_address,
            'subject': email.subject,
            'text_message': email.text_message,
            'html_message': email.html_message,
            'created_at': str(email.created_at),
            'sent': email.sent,
            'sent_at': str(email.sent_at) if email.sent_at else '',
            'retries': email.retries,
        }
    )


@mod.route(
    '/emails/<int:email_id>/send', endpoint='send_email', methods=['POST']
)
def send_email(email_id):
    email = Email.query.filter_by(id=email_id).first()

    if not email:
        abort(404)

    sent = email.send()

    if sent:
        return jsonify(
            {
                'id': email.id,
                'sent_date': str(email.sent_at),
                'response': 'OK'
            }
        )
    return jsonify(
        {
            'response': 'KO'
        }
    )
