from flask import Flask, jsonify

from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.app = app
    db.init_app(app)

    from api.views import main
    from api.views import emails
    app.register_blueprint(main.mod)
    app.register_blueprint(emails.mod)

    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(405)
    def not_found(error):
        return jsonify({'error': error.description}), error.code

    db.create_all()
    return app
