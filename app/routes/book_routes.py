from flask import render_template, flash, redirect, url_for, request, session
from app import db
from app.models.physical_book import PhysicalBook
from app.models.loan import Loan
from app.models.fine import Fine
from flask_login import current_user, login_required
from datetime import datetime, timedelta
from sqlalchemy import or_
from app.routes import main_bp

@main_bp.route('/')
def landing_page():
    """Renders the main landing page."""
    return render_template('landing_page.html', title='Welcome to LibraNet')

@main_bp.route('/search')
def search():
    """Global search across all publications (books, ebooks, audiobooks)."""
    query = request.args.get('q', '', type=str)
    
    if not query:
        return redirect(url_for('main.list_books'))
    
    # Search physical books
    books = PhysicalBook.query.filter(
        or_(
            PhysicalBook.title.ilike(f'%{query}%'),
            PhysicalBook.author.ilike(f'%{query}%')
        )
    ).all()
    
    return render_template('books.html', title=f'Search: {query}', books=books, search_term=query)

@main_bp.route('/books')
def list_books():
    """Displays the list of all books in the catalog. (Publicly accessible)"""
    search_term = request.args.get('q', '', type=str)
    availability = request.args.get('availability', '', type=str)
    sort_by = request.args.get('sort', 'title', type=str)

    # Start with base query
    query = PhysicalBook.query

    # Apply search filter
    if search_term:
        query = query.filter(
            or_(
                PhysicalBook.title.ilike(f'%{search_term}%'),
                PhysicalBook.author.ilike(f'%{search_term}%'),
                PhysicalBook.isbn.ilike(f'%{search_term}%')
            )
        )

    # Apply availability filter
    if availability == 'available':
        query = query.filter(PhysicalBook.available_copies > 0)
    elif availability == 'unavailable':
        query = query.filter(PhysicalBook.available_copies == 0)

    # Apply sorting
    if sort_by == 'title':
        query = query.order_by(PhysicalBook.title.asc())
    elif sort_by == 'title_desc':
        query = query.order_by(PhysicalBook.title.desc())
    elif sort_by == 'author':
        query = query.order_by(PhysicalBook.author.asc())
    elif sort_by == 'newest':
        query = query.order_by(PhysicalBook.id.desc())
    else:
        query = query.order_by(PhysicalBook.title.asc())

    books = query.all()

    return render_template('books.html', title='Book Catalog', books=books, search_term=search_term)

@main_bp.route('/book/<int:book_id>')
def book_detail(book_id):
    """Displays the details of a specific book. (Publicly accessible)"""
    book = PhysicalBook.query.get_or_404(book_id)
    existing_loan = None
    
    if current_user.is_authenticated:
        existing_loan = Loan.query.filter_by(
            student_id=current_user.id,
            book_id=book.id,
            returned_date=None
        ).first()

    return render_template('book-detail.html', title=book.title, book=book, existing_loan=existing_loan)

@main_bp.route('/add_to_bag/<int:book_id>', methods=['POST'])
@login_required
def add_to_bag(book_id):
    """Adds a book to the user's bag stored in the session."""
    # Check subscription access
    if not current_user.has_access_to_physical_books():
        flash('Upgrade your plan to borrow physical books!', 'warning')
        return redirect(url_for('main.subscriptions'))
    
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
    # Check subscription access
    if not current_user.has_access_to_physical_books():
        return render_template('upgrade_required.html', 
                             title='Upgrade Required',
                             feature='physical_books')
    
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
    # Check subscription access
    if not current_user.has_access_to_physical_books():
        flash('Upgrade your plan to borrow physical books!', 'warning')
        return redirect(url_for('main.subscriptions'))
    
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

@main_bp.route('/return_book/<int:loan_id>', methods=['POST'])
@login_required
def return_book(loan_id):
    """Handles returning a borrowed book."""
    loan = Loan.query.get_or_404(loan_id)
    
    # Verify the loan belongs to the current user
    if loan.student_id != current_user.id:
        flash('You can only return your own books.', 'danger')
        return redirect(url_for('main.my_loans'))
    
    # Check if already returned
    if loan.returned_date:
        flash('This book has already been returned.', 'info')
        return redirect(url_for('main.my_loans'))
    
    # Mark as returned
    loan.returned_date = datetime.utcnow()
    loan.status = 'returned'
    
    # Update book availability
    book = PhysicalBook.query.get(loan.book_id)
    if book:
        book.available_copies += 1
    
    # Check if overdue and create fine
    if loan.is_overdue():
        # Calculate overdue days
        overdue_days = (datetime.utcnow() - loan.due_date).days
        
        # Create fine using the standard fine amount (₹200)
        fine = Fine.create_standard_fine(loan_id=loan.id)
        db.session.add(fine)
        
        flash(f'Book returned! However, it was {overdue_days} day(s) overdue. A fine of ₹{fine.amount} has been applied.', 'warning')
    else:
        flash('Book returned successfully!', 'success')
    
    db.session.commit()
    return redirect(url_for('main.my_loans'))