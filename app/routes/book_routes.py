from flask import render_template, flash, redirect, url_for, request, session
from app.routes import main_bp as main
from app import db  # CORRECTED: Import db from the app package
from app.models.physical_book import PhysicalBook
from app.models.loan import Loan
from flask_login import current_user, login_required
from datetime import date
from sqlalchemy import or_

# All routes are now attached to this blueprint
book_routes = main

@book_routes.route('/')
def landing_page():
    """
    Renders the main landing page.
    """
    return render_template('landing_page.html', title='Welcome to LibraNet')

@book_routes.route('/books')
@login_required
def list_books():
    """
    Displays the list of all books in the catalog.
    If a search term is provided, it filters the books based on the search term.
    """
    search_term = request.args.get('q', '', type=str)

    if search_term:
        books = PhysicalBook.query.filter(
            or_(
                PhysicalBook.title.ilike(f'%{search_term}%'),
                PhysicalBook.author.ilike(f'%{search_term}%')
            )
        ).all()
    else:
        books = PhysicalBook.query.all()

    return render_template('books.html', title='Book Catalog', books=books, search_term=search_term)

@book_routes.route('/search')
@login_required
def search():
    """
    Handles the search functionality and redirects to the filtered book list.
    """
    search_term = request.args.get('q', '', type=str)
    if not search_term:
        return redirect(url_for('main.list_books'))

    return redirect(url_for('main.list_books', q=search_term))

@book_routes.route('/book/<int:book_id>')
@login_required
def book_detail(book_id):
    """
    Displays the details of a specific book.
    """
    book = PhysicalBook.query.get_or_404(book_id)
    existing_loan = Loan.query.filter_by(
        student_id=current_user.id,
        book_id=book.id,
        date_returned=None
    ).first()

    return render_template('book_detail.html', title=book.title, book=book, existing_loan=existing_loan)

@book_routes.route('/add_to_bag/<int:book_id>', methods=['POST'])
@login_required
def add_to_bag(book_id):
    """
    Adds a book to the user's bag stored in the session.
    """
    if 'bag' not in session:
        session['bag'] = []

    if book_id not in session['bag']:
        session['bag'].append(book_id)
        flash('Book added to your bag.', 'success')
    else:
        flash('Book is already in your bag.', 'info')

    session.modified = True
    return redirect(url_for('main.book_detail', book_id=book_id))

@book_routes.route('/my_bag')
@login_required
def my_bag():
    """
    Displays the contents of the user's bag.
    """
    if 'bag' not in session or not session['bag']:
        return render_template('my_bag.html', title='My Bag', books=[], can_borrow=False)

    book_ids = session['bag']
    books = PhysicalBook.query.filter(PhysicalBook.id.in_(book_ids)).all()

    active_loans_count = Loan.query.filter_by(student_id=current_user.id, date_returned=None).count()
    can_borrow = (len(books) + active_loans_count) <= 5

    return render_template('my_bag.html', title='My Bag', books=books, can_borrow=can_borrow)

@book_routes.route('/remove_from_bag/<int:book_id>', methods=['POST'])
@login_required
def remove_from_bag(book_id):
    """
    Removes a book from the user's bag.
    """
    if 'bag' in session and book_id in session['bag']:
        session['bag'].remove(book_id)
        session.modified = True
        flash('Book removed from your bag.', 'success')
    return redirect(url_for('main.my_bag'))

@book_routes.route('/borrow', methods=['POST'])
@login_required
def borrow():
    """
    Handles the borrowing of all books currently in the bag.
    """
    if 'bag' not in session or not session['bag']:
        flash('Your bag is empty.', 'danger')
        return redirect(url_for('main.my_bag'))

    book_ids = session['bag']
    active_loans_count = Loan.query.filter_by(student_id=current_user.id, date_returned=None).count()

    if (len(book_ids) + active_loans_count) > 5:
        flash('You cannot borrow more than 5 books at a time.', 'danger')
        return redirect(url_for('main.my_bag'))

    for book_id in book_ids:
        book = PhysicalBook.query.get(book_id)
        if book and book.is_available:
            loan = Loan(student_id=current_user.id, book_id=book_id, due_date=date.today())
            db.session.add(loan)
            book.is_available = False
        else:
            flash(f"'{book.title}' could not be borrowed as it's not available.", 'danger')

    db.session.commit()
    session.pop('bag', None)
    flash('You have successfully borrowed the books.', 'success')
    return redirect(url_for('main.my_loans'))