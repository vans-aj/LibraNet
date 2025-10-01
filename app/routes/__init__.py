from flask import Blueprint

# We create a Blueprint named 'main'. All routes will be attached to this.
main_bp = Blueprint('main', __name__)

# Import the routes at the bottom to link them to the blueprint
from app.routes import auth_routes,book_routes