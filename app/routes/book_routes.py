# In app/routes/book_routes.py

from flask import render_template
from app.routes import main_bp
from app.models.book import Book
from flask_login import login_user, logout_user, login_required, current_user

@main_bp.route('/')
@main_bp.route('/books')
@login_required
def list_books():
    """Displays a list of all books in the catalog."""
    books = Book.query.all()
    return render_template('list_books.html', title='Book Catalog', books=books)

