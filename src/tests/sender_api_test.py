# import requests
#
# from api import create_app
# from conf import DEFAULT_TO_ADDRESS
# from models import Email
#
#


# TODO


# def test_create_email():
#     app = create_app()  # TODO: create fixture
#
#     url = 'http://0.0.0.0:3000/emails/'  # Create fixture for base_url
#     playload = {'to_address': DEFAULT_TO_ADDRESS,
#                 'subject': 'Just testing sender app',
#                 'text_message': 'This is the email '
#                 'body when testing sender app',
#                 'html_message': '<p>This is '
#                 'the email html <strong>body</strong> '
#                 'when testing sender app</p>'
#                 }
#
#     response = requests.post(
#         url=url, json=playload, headers={'Content-type': 'application/json'})
#     assert 201 == response.status_code
#
#     email_id = response.json().get('id')
#     assert Email.query.filter_by(id=email_id).count() == 1
#     # TODO: Test create email without subject, text, etc.
#
# #
# # def test_list_emails():
# #     app = create_app()  # TODO: create fixture
# #
# #     url = 'http://0.0.0.0:3000/emails/'
# #
# #     response = requests.get(
#           url=url, headers={'Content-type': 'application/json'}
#       )
# #     assert 200 == response.status_code
# #
# #     emails = response.json()
# #     emails_num = Email.query.order_by(Email.id).count()
# #
# #     # Should test limit?
# #     assert len(emails) <= emails_num
# #
# #
# def test_send_email():
#     app = create_app()  # TODO: create fixture
#
#     email = Email.query.first()
#
#     url = 'http://0.0.0.0:3000/send_email/'
#
#     response = requests.post(
#           url=url, headers={'Content-type': 'application/json'},
#           params={'id': email.id}
#         )
#     assert 200 == response.status_code
#
#     email_id = response.json().get('id')
#
#     assert email.id == email_id
#
#     assert email.sent is True
