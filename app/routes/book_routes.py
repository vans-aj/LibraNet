# In app/routes/book_routes.py

from flask import render_template, abort, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.routes import main_bp
from app.models.loan import Loan
from app import db
# --- UPDATE THIS IMPORT ---
from app.models.physical_book import PhysicalBook

@main_bp.route('/')
def landing_page():
    """Renders the public landing page."""
    return render_template('landing_page.html', title='Welcome to LibraNet')

@main_bp.route('/books')
@login_required
def list_books():
    search_term = request.args.get('search')
    if search_term:
        # --- UPDATE THE MODEL NAME HERE ---
        query = PhysicalBook.query.filter(
            or_(
                PhysicalBook.title.like(f'%{search_term}%'),
                PhysicalBook.author.like(f'%{search_term}%')
            )
        )
    else:
        # --- AND HERE ---
        query = PhysicalBook.query
    books = query.order_by(PhysicalBook.title).all()
    return render_template('books.html', title='Book Catalog', books=books, search_term=search_term)

@main_bp.route('/book/<int:book_id>')
@login_required
def book_detail(book_id):
    # --- AND HERE ---
    book = PhysicalBook.query.get_or_404(book_id)
    return render_template('book_detail.html', title=book.title, book=book)

@main_bp.route('/add-to-bag/<int:book_id>', methods=['POST'])
@login_required
def add_to_bag(book_id):
    bag = session.get('bag', [])
    # --- AND HERE ---
    book = PhysicalBook.query.get_or_404(book_id)
    if book.available_copies < 1:
        flash(f'"{book.title}" is currently unavailable.', 'danger')
    elif book_id not in bag:
        bag.append(book_id)
        session['bag'] = bag
        flash(f'Added "{book.title}" to your bag!', 'success')
    else:
        flash(f'"{book.title}" is already in your bag.', 'info')
    return redirect(url_for('main.book_detail', book_id=book_id))

@main_bp.route('/my-bag')
@login_required
def my_bag():
    book_ids = session.get('bag', [])
    books_in_bag = []
    if book_ids:
        # --- AND HERE ---
        books_in_bag = PhysicalBook.query.filter(PhysicalBook.id.in_(book_ids)).all()
    return render_template('my_bag.html', title='My Bag', books=books_in_bag)

@main_bp.route('/remove-from-bag/<int:book_id>', methods=['POST'])
@login_required
def remove_from_bag(book_id):
    bag = session.get('bag', [])
    if book_id in bag:
        bag.remove(book_id)
        session['bag'] = bag
        flash('The book has been removed from your bag.', 'success')
    return redirect(url_for('main.my_bag'))

@main_bp.route('/borrow-all', methods=['POST'])
@login_required
def borrow_all():
    book_ids = session.get('bag', [])
    if not book_ids:
        flash('Your bag is empty.', 'info')
        return redirect(url_for('main.my_bag'))
    # --- AND HERE ---
    books_to_borrow = PhysicalBook.query.filter(PhysicalBook.id.in_(book_ids)).all()
    for book in books_to_borrow:
        if book.available_copies > 0:
            new_loan = Loan(student_id=current_user.id, book_id=book.id)
            db.session.add(new_loan)
            book.available_copies -= 1
        else:
            flash(f'Sorry, "{book.title}" ran out of stock and could not be borrowed.', 'danger')
    session.pop('bag', None)
    db.session.commit()
    flash('You have successfully borrowed the books!', 'success')
    return redirect(url_for('main.list_books'))