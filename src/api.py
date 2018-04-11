from flask import Flask, jsonify, abort, make_response, request

import conf
from conf import DEBUG
from models import Email, db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/messages.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # app_settings = os.getenv('APP_SETTINGS')
    # app.config.from_object(app_settings)

    db.app = app
    db.init_app(app)

    @app.route('/')
    def server_info():
        return jsonify(
            {'server': 'Sender App'}
        )

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    @app.errorhandler(400)
    def not_found(error):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    @app.route("/emails/", endpoint='emails_list', methods=['GET'])
    def emails_list():
        limit = int(request.args.get('limit', 10))
        sent = request.args.get('sent')

        if sent == 'true':
            emails = Email.query.filter_by(sent=True).order_by(Email.id).limit(limit).all()
        elif sent == 'false':
            emails = Email.query.filter_by(sent=False).order_by(Email.id).limit(limit).all()
        else:
            emails = Email.query.order_by(Email.id).limit(limit).all()

        return jsonify([{'id': email.id,
                         'from_address': email.from_address,
                         'to_address': email.to_address,
                         'subject': email.subject,
                         'text_message': email.text_message,
                         'html_message': email.html_message,
                         'created_at': email.created_at,
                         'sent': email.sent,
                         'sent_at': email.sent_at,
                         'retries': email.retries,
                         } for email in emails]
                       )

    @app.route('/emails/', endpoint='create_email', methods=['POST'])
    def create_email():
        autosend = request.args.get('autosend')

        json = request.get_json()

        if 'subject' not in json or 'text_message' not in json:
            abort(400)

        to_address = json.get('to_address')
        subject = json.get('subject')
        text_message = json.get('text_message')
        html_message = json.get('html_message')

        from_address = conf.GMAIL_USER

        new_email = Email(from_address=from_address,
                          to_address=to_address,
                          subject=subject,
                          text_message=text_message,
                          html_message=html_message)

        db.session.add(new_email)
        db.session.commit()

        if autosend == 'true':
            sent = new_email.send()  # TODO: Fix. Doesn't mark as sent in bbdd

        return jsonify({'id': new_email.id}), 201

    @app.route("/emails/<int:email_id>", endpoint='email_detail', methods=['GET'])
    def email_detail(email_id):
        email = Email.query.filter_by(id=email_id).first()

        if not email:
            abort(404)

        return jsonify({'id': email.id,
                        'from_address': email.from_address,
                        'to_address': email.to_address,
                        'subject': email.subject,
                        'text_message': email.text_message,
                        'html_message': email.html_message,
                        'created_at': email.created_at,
                        'sent': email.sent,
                        'sent_at': email.sent_at,
                        'retries': email.retries,
                        })

    @app.route("/emails/<int:email_id>/send", endpoint='send_email', methods=['POST'])
    def send_email(email_id):

        email = Email.query.filter_by(id=email_id).first()
        sent = email.send()

        if sent:
            return jsonify({'id': email.id, 'sent_date': email.sent_at, 'response': 'OK'})
        return jsonify({'response': 'KO'})

    db.create_all()  # Should this be here?
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=3000, host='0.0.0.0', debug=DEBUG)
