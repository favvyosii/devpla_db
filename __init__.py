# backend/__init__.py
from flask import Flask
from models import db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    CORS(app)  # Enable CORS for frontend-backend interaction

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return app
