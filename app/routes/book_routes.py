from flask import render_template, flash, redirect, url_for, request, session
from app import db
from app.models.physical_book import PhysicalBook
from app.models.loan import Loan
from flask_login import current_user, login_required
from datetime import datetime, timedelta
from sqlalchemy import or_
from app.routes import main_bp

@main_bp.route('/')
def landing_page():
    """Renders the main landing page."""
    return render_template('landing_page.html', title='Welcome to LibraNet')

@main_bp.route('/books')
@login_required
def list_books():
    """Displays the list of all books in the catalog."""
    search_term = request.args.get('q', '', type=str)

    if search_term:
        books = PhysicalBook.query.filter(
            or_(
                PhysicalBook.title.ilike(f'%{search_term}%'),
                PhysicalBook.author.ilike(f'%{search_term}%')
            )
        ).order_by(PhysicalBook.title).all()
    else:
        books = PhysicalBook.query.order_by(PhysicalBook.title).all()

    return render_template('books.html', title='Book Catalog', books=books, search_term=search_term)

@main_bp.route('/book/<int:book_id>')
@login_required
def book_detail(book_id):
    """Displays the details of a specific book."""
    book = PhysicalBook.query.get_or_404(book_id)
    existing_loan = Loan.query.filter_by(
        student_id=current_user.id,
        book_id=book.id,
        returned_date=None
    ).first()

    return render_template('book_detail.html', title=book.title, book=book, existing_loan=existing_loan)

@main_bp.route('/add_to_bag/<int:book_id>', methods=['POST'])
@login_required
def add_to_bag(book_id):
    """Adds a book to the user's bag stored in the session."""
    if 'bag' not in session:
        session['bag'] = []

    if book_id not in session['bag']:
        session['bag'].append(book_id)
        flash('Book added to your bag.', 'success')
    else:
        flash('Book is already in your bag.', 'info')

    session.modified = True
    return redirect(url_for('main.book_detail', book_id=book_id))

@main_bp.route('/my_bag')
@login_required
def my_bag():
    """Displays the contents of the user's bag."""
    if 'bag' not in session or not session['bag']:
        return render_template('my_bag.html', title='My Bag', books=[], can_borrow=False, due_date=datetime.utcnow() + timedelta(days=14))

    book_ids = session['bag']
    books = PhysicalBook.query.filter(PhysicalBook.id.in_(book_ids)).all()

    active_loans_count = Loan.query.filter_by(student_id=current_user.id, returned_date=None).count()
    can_borrow = (len(books) + active_loans_count) <= 5
    
    # Calculate due date (14 days from now)
    due_date = datetime.utcnow() + timedelta(days=14)

    return render_template('my_bag.html', title='My Bag', books=books, can_borrow=can_borrow, due_date=due_date)

@main_bp.route('/remove_from_bag/<int:book_id>', methods=['POST'])
@login_required
def remove_from_bag(book_id):
    """Removes a book from the user's bag."""
    if 'bag' in session and book_id in session['bag']:
        session['bag'].remove(book_id)
        session.modified = True
        flash('Book removed from your bag.', 'success')
    return redirect(url_for('main.my_bag'))

@main_bp.route('/borrow', methods=['POST'])
@login_required
def borrow():
    """Handles the borrowing of all books currently in the bag."""
    if 'bag' not in session or not session['bag']:
        flash('Your bag is empty.', 'danger')
        return redirect(url_for('main.my_bag'))

    book_ids = session['bag']
    active_loans_count = Loan.query.filter_by(student_id=current_user.id, returned_date=None).count()

    if (len(book_ids) + active_loans_count) > 5:
        flash(f'You cannot borrow more than 5 books at a time. You already have {active_loans_count} books on loan.', 'danger')
        return redirect(url_for('main.my_bag'))

    borrowed_books = 0
    for book_id in book_ids:
        book = PhysicalBook.query.get(book_id)
        if book and book.is_available:
            loan = Loan(student_id=current_user.id, book_id=book_id)
            db.session.add(loan)
            book.available_copies -= 1
            borrowed_books += 1
        else:
            flash(f"'{book.title if book else 'A book'}' could not be borrowed as it's not available.", 'danger')

    db.session.commit()
    session.pop('bag', None)
    if borrowed_books > 0:
        flash(f'You have successfully borrowed {borrowed_books} book(s).', 'success')
    return redirect(url_for('main.my_loans'))