from flask import url_for

from models import Email


def test_404(client):
    response = client.get('doesntexist')
    assert response.status_code == 404
    assert 'error' in response.json


def test_server_info(client):
    assert client.get(url_for('main.server_info')).status_code == 200


def test_email_list(client):
    # Email.
    response = client.get(url_for('emails.email_list'))
    assert response.status_code == 200
    assert len(response.json) == Email.query.count()


# # @mod.route('/emails/', endpoint='email_list', methods=['GET'])
# # def email_list():
# #     limit = int(request.args.get('limit', 10))
# #     sent = request.args.get('sent')
# #
# #     if sent == 'true':
# #         emails = Email.query.filter_by(sent=True).
# #         order_by(Email.id).limit(limit).all()
# #     elif sent == 'false':
# #         emails = Email.query.filter_by(sent=False).
# #         order_by(Email.id).limit(limit).all()
# #     else:
# #         emails = Email.query.order_by(Email.id).limit(limit).all()
# #
# #     return jsonify([
# #         {
# #             'id': email.id,
# #             'from_address': email.from_address,
# #             'to_address': email.to_address,
# #             'subject': email.subject,
# #             'text_message': email.text_message,
# #             'html_message': email.html_message,
# #             'created_at': email.created_at,
# #             'sent': email.sent,
# #             'sent_at': email.sent_at,
# #             'retries': email.retries,
# #         }
# #         for email in emails
# #     ])
# #
#
#


def test_create_email_ko(client):
    response = client.post(url_for('emails.create_email'))
    assert response.status_code == 400


def test_create_email_ok(client):
    response = client.post(
        url_for('emails.create_email'),
        json={
            'subject': 'test subject',
            'text_message': 'test_text_message'
        }
    )
    assert response.status_code == 201
    assert not response.get('sent')
#     # email_id = response.get('id')


#
#
# # @mod.route('/emails/', endpoint='create_email', methods=['POST'])
# # def create_email():
# #     autosend = request.args.get('autosend')
# #
# #     json = request.get_json()
# #
# #     if 'subject' not in json or 'text_message' not in json:
# #         abort(400)
# #
# #     to_address = json.get('to_address')
# #     subject = json.get('subject')
# #     text_message = json.get('text_message')
# #     html_message = json.get('html_message')
# #
# #     from_address = config.FROM_ADDRESS
# #
# #     new_email = Email(
# #         from_address=from_address,
# #         to_address=to_address if to_address else config.DEFAULT_TO_ADDRESS,
# #         subject=subject,
# #         text_message=text_message,
# #         html_message=html_message
# #     )
# #
# #     sent = 'false'
# #     if autosend == 'true':
# #         sent = new_email.send()
# #
# #     db.session.add(new_email)
# #     db.session.commit()
# #     return jsonify({'id': new_email.id, 'sent': sent}), 201
# #
#
#
# def test_email_detail():
#     pass
#
#
# # @mod.route('/emails/<int:email_id>', endpoint='email_detail',
# # methods=['GET'])
# # def email_detail(email_id):
# #     email = Email.query.filter_by(id=email_id).first()
# #
# #     if not email:
# #         abort(404)
# #
# #     return jsonify(
# #         {
# #             'id': email.id,
# #             'from_address': email.from_address,
# #             'to_address': email.to_address,
# #             'subject': email.subject,
# #             'text_message': email.text_message,
# #             'html_message': email.html_message,
# #             'created_at': email.created_at,
# #             'sent': email.sent,
# #             'sent_at': email.sent_at,
# #             'retries': email.retries,
# #         }
# #     )
#
#
# def test_send_email():
#     pass
#
# #
# # @mod.route('/emails/<int:email_id>/send', endpoint='send_email',
# # methods=['POST'])
# # def send_email(email_id):
# #     email = Email.query.filter_by(id=email_id).first()
# #     sent = email.send()
# #
# #     if sent:
# #         return jsonify(
# #             {
# #                 'id': email.id,
# #                 'sent_date': email.sent_at,
# #                 'response': 'OK'
# #             }
# #         )
# #     return jsonify(
# #         {
# #             'response': 'KO'
# #         }
# #     )
# #
#
#
# db.session.remove()
# db.drop_all()
