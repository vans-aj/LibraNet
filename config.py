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

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')

    OTP_EXPIRY_MINUTES = 10
    
    # Google OAuth Configuration
    GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
    OAUTHLIB_INSECURE_TRANSPORT = os.getenv('OAUTHLIB_INSECURE_TRANSPORT', '1')  # Only for development
    
    # GitHub OAuth Configuration
    GITHUB_OAUTH_CLIENT_ID = os.getenv('GITHUB_OAUTH_CLIENT_ID')
    GITHUB_OAUTH_CLIENT_SECRET = os.getenv('GITHUB_OAUTH_CLIENT_SECRET')
    
    os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
    os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')
    os.environ['LANGCHAIN_TRACING_V2'] = "true"
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
    os.environ["LIBRIVOX_API_URL"] = os.getenv("LIBRIVOX_API_URL")