from flask import Flask, jsonify

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

    @app.route('/new_email/', endpoint='create_email', methods=['POST'])
    def create_email():
        from flask import request
        json = request.get_json()

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

        return jsonify(
            {'id': new_email.id}
        ), 201

    @app.route("/emails/", endpoint='emails_list', methods=['GET'])
    def emails_list():
        from flask import request
        limit = int(request.args.get('limit', 10))

        emails = Email.query.order_by(Email.id).limit(limit).all()

        return jsonify([{'id': email.id,
                         'from_address': email.from_address,
                         'to_address': email.to_address,
                         'subject': email.subject,
                         'text_message': email.text_message,
                         'html_message': email.html_message,
                         } for email in emails]
                       )

    @app.route("/send_email/", endpoint='send_email', methods=['POST'])
    def send_email():
        from flask import request
        email_id = int(request.args.get('id'))

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
