# In app/routes/book_routes.py

from flask import render_template , abort , session, redirect, url_for, flash 
from app.routes import main_bp
from app.models.book import Book
from flask_login import login_user, logout_user, login_required, current_user
from app.models.loan import Loan 
from app import db  
from app.models.loan import Loan             

@main_bp.route('/')
@main_bp.route('/books')
@login_required
def list_books():
    """Displays a list of all books in the catalog."""
    books = Book.query.all()
    return render_template('list_books.html', title='Book Catalog', books=books)

@main_bp.route('/book/<int:book_id>')
@login_required
def book_detail(book_id):
    """Displays the details for a single book."""
    # .get_or_404() is a handy shortcut: it gets the record by its primary key
    # or automatically returns a 404 Not Found error if it doesn't exist.
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', title=book.title, book=book)

@main_bp.route('/add-to-bag/<int:book_id>', methods=['POST'])
@login_required
def add_to_bag(book_id):
    """Adds a book to the user's bag stored in the session."""
    # Get the bag from the session, or create an empty list if it doesn't exist
    bag = session.get('bag', [])

    # Check if the book is available and not already in the bag
    book = Book.query.get_or_404(book_id)
    if book.available_copies < 1:
        flash(f'"{book.title}" is currently unavailable.', 'danger')
    elif book_id not in bag:
        bag.append(book_id)
        # Save the updated bag back to the session
        session['bag'] = bag
        flash(f'Added "{book.title}" to your bag!', 'success')
    else:
        flash(f'"{book.title}" is already in your bag.', 'info')

    # Redirect the user back to the book detail page
    return redirect(url_for('main.book_detail', book_id=book_id))

# In app/routes/book_routes.py

# ... your list_books(), book_detail(), and add_to_bag() functions are here ...


@main_bp.route('/my-bag')
@login_required
def my_bag():
    """Displays the contents of the user's bag."""
    # Get the list of book IDs from the session
    book_ids = session.get('bag', [])
    
    books_in_bag = []
    if book_ids:
        # Fetch the full book objects from the database for the IDs in the session.
        # The .in_() method is a very efficient way to get multiple items at once.
        books_in_bag = Book.query.filter(Book.id.in_(book_ids)).all()

    return render_template('my_bag.html', title='My Bag', books=books_in_bag)


@main_bp.route('/remove-from-bag/<int:book_id>', methods=['POST'])
@login_required
def remove_from_bag(book_id):
    """Removes a book from the user's bag."""
    bag = session.get('bag', [])

    if book_id in bag:
        bag.remove(book_id)
        session['bag'] = bag
        flash('The book has been removed from your bag.', 'success')
    
    return redirect(url_for('main.my_bag'))

@main_bp.route('/borrow-all', methods=['POST'])
@login_required
def borrow_all():
    """
    Takes all book IDs from the session bag, creates Loan records,
    and updates the available copies for each book.
    """
    book_ids = session.get('bag', [])
    if not book_ids:
        flash('Your bag is empty.', 'info')
        return redirect(url_for('main.my_bag'))

    books_to_borrow = Book.query.filter(Book.id.in_(book_ids)).all()
    
    for book in books_to_borrow:
        if book.available_copies > 0:
            # Create a new loan record for the current user and book
            new_loan = Loan(student_id=current_user.id, book_id=book.id)
            db.session.add(new_loan)
            
            # Decrement the number of available copies
            book.available_copies -= 1
        else:
            flash(f'Sorry, "{book.title}" ran out of stock and could not be borrowed.', 'danger')

    # Clear the bag from the session now that the books are "borrowed"
    session.pop('bag', None)
    
    # Commit all the changes (new loans and updated copies) to the database at once
    db.session.commit()

    flash('You have successfully borrowed the books!', 'success')
    # Redirect the user to their new "My Loans" page (we can build this next)
    # For now, let's send them back to the main book catalog.
    return redirect(url_for('main.list_books'))



@main_bp.route('/my-loans')
@login_required
def my_loans():
    """Displays all the books currently borrowed by the logged-in user."""
    # This is the core of this feature. We query the Loan table and filter
    # for all records where the student_id matches the current user's id.
    loans = Loan.query.filter_by(student_id=current_user.id).all()
    
    return render_template('my_loans.html', title='My Loans', loans=loans)
