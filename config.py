# config.py

import os
from dotenv import load_dotenv

# Find the .env file in the root directory and load its variables
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """
    Base configuration class.
    Contains default configuration settings and settings imported from .env file.
    """
    
    # Secret key is used by Flask for session signing and by Flask-WTF for CSRF protection.
    # It's crucial to keep this secret.
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-should-really-change-this-fallback-key')

    # Database configuration
    # Reads the database URL from the .env file.
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    # This is a Flask-SQLAlchemy configuration setting that we can disable
    # to save resources, as we are not using the event system.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET') or 'YOUR_KEY_SECRET'