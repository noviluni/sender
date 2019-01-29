import os


DEBUG = os.environ.get('DEBUG', True)
DEFAULT_TO_ADDRESS = os.environ.get('DEFAULT_TO_ADDRESS', '')
FROM_ADDRESS = os.environ.get('FROM_ADDRESS', '')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = os.environ.get('SMTP_PORT', 587)
