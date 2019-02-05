import pytest
from flask import url_for

from models import Email


def test_404(client):
    response = client.get('doesntexist')
    assert response.status_code == 404
    assert 'error' in response.json


def test_server_info(client):
    assert client.get(url_for('main.server_info')).status_code == 200


@pytest.mark.parametrize("target_email", [
    'no_sent',
    'sent'
])
def test_email_detail_ok(target_email, client, email, email_sent):
    email = email if target_email == 'no_sent' else email_sent
    response = client.get(
        url_for('emails.email_detail', email_id=email.id),
    )
    assert response.status_code == 200
    assert response.json['id'] == email.id
    assert response.json['from_address'] == email.from_address
    assert response.json['to_address'] == email.to_address
    assert response.json['subject'] == email.subject
    assert response.json['text_message'] == email.text_message
    assert response.json['html_message'] == email.html_message
    assert response.json['created_at'] == str(email.created_at)

    assert response.json['sent'] == email.sent
    sent_at = str(email.sent_at) if email.sent_at else ''
    assert response.json['sent_at'] == sent_at
    assert response.json['retries'] == email.retries


def test_email_detail_ko(client, email):
    response = client.get(
        url_for('emails.email_detail', email_id=0),
    )
    assert response.status_code == 404


def test_email_list(client, email, email_sent):
    response = client.get(url_for('emails.email_list'))
    assert response.status_code == 200
    assert len(response.json) == Email.query.count() == 2
    for attr in ('id', 'from_address', 'to_address', 'subject',
                 'text_message', 'html_message', 'created_at',
                 'sent', 'sent_at', 'retries'):
        assert attr in response.json[0]


@pytest.mark.parametrize("sent_param,sent_query", [
    ('?sent=true', True),
    ('?sent=false', False),
    ('', '')
])
def test_email_list_sent(sent_param, sent_query, client, email, email_sent):
    response = client.get(url_for('emails.email_list')+sent_param)
    assert response.status_code == 200
    if sent_param:
        assert len(response.json) == \
               Email.query.filter_by(sent=sent_query).count() == 1
    else:
        assert len(response.json) == Email.query.count() == 2


@pytest.mark.parametrize("autosend,param,sent_value", [
    (False, '', 'false'),
    (True, '?autosend=true', 'true')
])
# @mock.patch('models.send_email', return_value=True)
def test_create_email_ok(autosend, param, sent_value, client):
    response = client.post(
        url_for('emails.create_email')+param,
        json={
            'subject': 'test subject',
            'text_message': 'test_text_message'
        }
    )
    # send_email_mocked.assert_called_once()
    assert response.status_code == 201
    assert response.json.get('id') == Email.query.order_by(
        Email.id.desc()
    )[-1].id
    assert response.json.get('sent') == sent_value


def test_create_email_ko(client):
    response = client.post(url_for('emails.create_email'))
    assert response.status_code == 400


# @mock.patch('models.send_email', return_value=True)
def test_send_email_ok(client, email):
    assert email.sent is False
    assert email.sent_at is None
    response = client.post(url_for('emails.send_email', email_id=email.id))
    # send_email_mocked.assert_called_once()
    assert response.status_code == 200
    assert response.json.get('id') == email.id
    assert response.json.get('sent_date') == str(email.sent_at)
    assert response.json.get('response') == 'OK'


def test_send_email_ko(client):
    response = client.post(
        url_for('emails.send_email', email_id=0),
    )
    assert response.status_code == 404

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