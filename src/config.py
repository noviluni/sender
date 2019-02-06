import os

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'SQLALCHEMY_DATABASE_URI', 'sqlite:///messages.db'
)
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
    'SQLALCHEMY_TRACK_MODIFICATIONS', False
)
DEBUG = os.environ.get('DEBUG', True)
DEFAULT_TO_ADDRESS = os.environ.get('DEFAULT_TO_ADDRESS', '')
FROM_ADDRESS = os.environ.get('FROM_ADDRESS', '')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = os.environ.get('SMTP_PORT', 587)
SERVER_NAME = os.environ.get('SERVER_NAME', 'SENDER')
