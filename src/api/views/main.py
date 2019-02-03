from flask import Blueprint, jsonify

mod = Blueprint('main', __name__)


@mod.route('/')
def server_info():
    return jsonify({'server': 'Sender App'})
