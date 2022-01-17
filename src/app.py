import awsgi
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

with app.app_context():
    import config.routes


def handler(event, context):
    return awsgi.response(app, event, context)
