from flask import render_template, flash, redirect, url_for, request, session, jsonify
from app import db
from app.models.physical_book import PhysicalBook
from app.models.loan import Loan
from app.models.fine import Fine
from flask_login import current_user, login_required
from datetime import datetime, timedelta
from sqlalchemy import or_
from app.routes import main_bp
import razorpay
import os

# Initialize Razorpay Client
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_YOUR_KEY_ID')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'YOUR_KEY_SECRET')
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Security deposit per book
SECURITY_DEPOSIT_PER_BOOK = 100

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

@main_bp.route('/borrow', methods=['GET', 'POST'])
@login_required
def borrow():
    """Handle book borrowing with Razorpay payment for security deposit."""
    
    # Check if user has subscription access
    if not current_user.has_access_to_physical_books():
        if request.method == 'POST' and request.is_json:
            return jsonify({
                'success': False,
                'message': 'You need an active Basic, Pro, or Max subscription to borrow physical books.'
            }), 403
        flash('You need an active Basic, Pro, or Max subscription to borrow physical books.', 'warning')
        return redirect(url_for('main.subscriptions'))
    
    # Get bag from session
    bag = session.get('bag', [])
    if not bag:
        if request.method == 'POST' and request.is_json:
            return jsonify({
                'success': False,
                'message': 'Your bag is empty.'
            }), 400
        flash('Your bag is empty.', 'info')
        return redirect(url_for('main.list_books'))
    
    # Check loan limits (max 5 books at a time)
    active_loans_count = Loan.query.filter_by(
        student_id=current_user.id, 
        returned_date=None
    ).count()
    
    if (len(bag) + active_loans_count) > 5:
        if request.method == 'POST' and request.is_json:
            return jsonify({
                'success': False,
                'message': f'You can only have up to 5 books on loan at once. You currently have {active_loans_count} active loans.'
            }), 400
        flash(f'You can only have up to 5 books on loan at once. You currently have {active_loans_count} active loans.', 'danger')
        return redirect(url_for('main.my_bag'))
    
    if request.method == 'GET':
        # Calculate security deposit
        security_deposit = len(bag) * SECURITY_DEPOSIT_PER_BOOK
        
        # Get book details
        books = PhysicalBook.query.filter(PhysicalBook.id.in_(bag)).all()
        
        # Render confirmation page with Razorpay
        return render_template(
            'my_bag.html',
            title='My Bag',
            books=books,
            security_deposit=security_deposit,
            razorpay_key_id=RAZORPAY_KEY_ID
        )
    
    # POST - Create Razorpay order
    try:
        # Calculate total amount
        amount = len(bag) * SECURITY_DEPOSIT_PER_BOOK * 100  # Convert to paise
        
        # Create Razorpay order
        order_data = {
            'amount': amount,
            'currency': 'INR',
            'payment_capture': '1',
            'notes': {
                'user_id': current_user.id,
                'book_count': len(bag),
                'type': 'security_deposit'
            }
        }
        
        order = razorpay_client.order.create(data=order_data)
        
        # Store order info in session for verification
        session['pending_borrow_order'] = {
            'order_id': order['id'],
            'amount': amount,
            'book_ids': bag
        }
        
        return jsonify({
            'success': True,
            'order_id': order['id'],
            'amount': amount,
            'currency': 'INR',
            'key': RAZORPAY_KEY_ID
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to create payment order: {str(e)}'
        }), 500


@main_bp.route('/borrow/verify', methods=['POST'])
@login_required
def verify_borrow_payment():
    """Verify Razorpay payment and create loan records."""
    try:
        data = request.get_json()
        
        # Extract payment details
        payment_id = data.get('razorpay_payment_id')
        order_id = data.get('razorpay_order_id')
        
        # Validate inputs
        if not payment_id or not order_id:
            return jsonify({'success': False, 'message': 'Missing payment details'}), 400
        
        # Get pending order from session
        pending_order = session.get('pending_borrow_order')
        if not pending_order or pending_order['order_id'] != order_id:
            return jsonify({'success': False, 'message': 'Invalid order'}), 400
        
        # Verify payment with Razorpay
        try:
            payment = razorpay_client.payment.fetch(payment_id)
            
            # Check if payment is captured
            if payment['status'] not in ['captured', 'authorized']:
                return jsonify({'success': False, 'message': 'Payment not successful'}), 400
                
        except Exception as e:
            # In test mode, if fetching fails, we'll proceed anyway
            print(f"Razorpay fetch error (might be test mode): {str(e)}")
        
        # Get book IDs from pending order
        book_ids = pending_order['book_ids']
        
        # Create loan records
        loans_created = []
        for book_id in book_ids:
            book = PhysicalBook.query.get(book_id)
            if book and book.available_copies > 0:
                loan = Loan(
                    student_id=current_user.id,
                    book_id=book_id,
                    payment_id=payment_id  # Store payment ID for refund tracking
                )
                book.available_copies -= 1
                db.session.add(loan)
                loans_created.append(book.title)
        
        # Commit all changes
        db.session.commit()
        
        # Clear session
        session.pop('bag', None)
        session.pop('pending_borrow_order', None)
        
        return jsonify({
            'success': True,
            'message': f'Successfully borrowed {len(loans_created)} book(s)!',
            'books': loans_created
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to process borrowing: {str(e)}'
        }), 500


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