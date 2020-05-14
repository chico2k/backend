from .base import *
import os

print("###################################################################################")
print("########                Started with Staging Settings         #####################")
print("###################################################################################")

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    'ultigu-test.6qfyr2bjnx.eu-central-1.elasticbeanstalk.com'
]

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'http://ultigu-test.6qfyr2bjnx.eu-central-1.elasticbeanstalk.com',
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:8080',
    'http://localhost:80',
)

EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
