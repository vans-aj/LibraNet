# app/__init__.py (The corrected, professional version)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config  # Import the Config class
from flask_login import LoginManager #If a user who is not logged in tries to access a protected page, redirect them to the login page
from app.models import RoleEnum 

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()  
login_manager.login_view = 'main.login'

def create_app(config_class=Config): # Set the default config
    app = Flask(__name__)
    # Load all configuration settings from the object in one line
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    @app.context_processor

    def inject_role_enum():
        """Makes RoleEnum available to all templates."""
        return dict(RoleEnum=RoleEnum)
    
    # Import and register the blueprint
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # This part is primarily for Flask-Migrate to detect your models
    with app.app_context():
        from app.models import student, book, loan, fine # noqa

    return app


