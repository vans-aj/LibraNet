from flask import Blueprint

# Create Blueprint
main_bp = Blueprint('main', __name__)

# Import all route modules
from app.routes import (
    auth_routes,
    book_routes,
    admin_routes,
    subscription_routes,
    ebook_routes,
    audiobook_routes
)