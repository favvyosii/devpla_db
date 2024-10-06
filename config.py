# backend/config.py
import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///devs.db'  # Local SQLite DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # You can set this in an .env file
