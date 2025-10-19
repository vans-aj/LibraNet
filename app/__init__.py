from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()  
login_manager.login_view = 'main.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Import and register the blueprint
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Import models for Flask-Migrate
    with app.app_context():
        from app.models import student, publication, physical_book, ebook, audiobook, loan, fine, subscription

    return app