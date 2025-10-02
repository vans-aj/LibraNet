# In app/routes/admin_routes.py

from flask import render_template, abort ,flash , redirect , url_for  ,request
from flask_login import login_required, current_user
from functools import wraps
from app.routes import main_bp
from app.models import RoleEnum
from app.models.book import Book
from app.models.student import Student
from app.forms import BookForm
from app import db

# --- This is our custom decorator for role-based access ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in and has the ADMIN role
        if not current_user.is_authenticated or current_user.role != RoleEnum.ADMIN:
            # If not, return a 403 Forbidden error
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


# --- This is our first protected admin route ---
@main_bp.route('/admin')
@login_required   # Ensures the user is logged in first
@admin_required   # THEN checks if they are an admin
def admin_dashboard():
    """Admin dashboard page."""
    # We will create this template in the next step
    return render_template('admin/dashboard.html', title='Admin Dashboard')

# In app/routes/admin_routes.py

# ... (all your existing imports and functions are here) ...

# --- ADD THIS NEW ROUTE AT THE BOTTOM ---

@main_bp.route('/admin/books')
@login_required
@admin_required
def manage_books():
    """Admin page to view and manage all books."""
    # We query all books and order them alphabetically by title for easy viewing.
    books = Book.query.order_by(Book.title).all()
    return render_template('admin/manage_books.html', title='Manage Books', books=books)

@main_bp.route('/admin/add_book', methods=['GET', 'POST'])
@login_required
@admin_required
def add_book():
    """Route for adding a new book."""
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            format=form.format.data,
            total_copies=form.total_copies.data,
            available_copies=form.total_copies.data
        )
        db.session.add(new_book)
        db.session.commit()
        flash(f'Book "{new_book.title}" has been added successfully!', 'success')
        # A good user experience is to redirect back to the list of all books
        return redirect(url_for('main.manage_books'))
    return render_template('admin/add_book.html', title='Add New Book', form=form)



@main_bp.route('/admin/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_book(book_id):
    """Route for editing an existing book."""
    book = Book.query.get_or_404(book_id)
    form = BookForm(original_book=book)

    if form.validate_on_submit():
        # --- THIS IS THE NEW, SMARTER LOGIC ---
        
        # Calculate how many books are currently on loan. This number doesn't change.
        borrowed_copies = book.total_copies - book.available_copies
        new_total_copies = form.total_copies.data

        # Safety Check: Don't allow total_copies to be less than what's already borrowed.
        if new_total_copies < borrowed_copies:
            flash(f'Error: Total copies ({new_total_copies}) cannot be less than the number of books currently on loan ({borrowed_copies}).', 'danger')
            # We redirect back without saving to prevent invalid data
            return redirect(url_for('main.edit_book', book_id=book_id))
        else:
            # Calculate the new number of available copies
            new_available_copies = new_total_copies - borrowed_copies
            
            # Update all the book's attributes from the form data
            book.title = form.title.data
            book.author = form.author.data
            book.isbn = form.isbn.data
            book.format = form.format.data
            book.total_copies = new_total_copies
            book.available_copies = new_available_copies # Use our new calculated value
            
            db.session.commit()
            flash('The book has been updated successfully!', 'success')
            return redirect(url_for('main.manage_books'))
    
    elif request.method == 'GET':
        # Pre-populate the form (this logic is unchanged)
        form.title.data = book.title
        form.author.data = book.author
        form.isbn.data = book.isbn
        form.format.data = book.format.value
        form.total_copies.data = book.total_copies
        
    return render_template('admin/add_book.html', title=f'Edit "{book.title}"', form=form)

@main_bp.route('/admin/students')
@login_required
@admin_required
def manage_students():
    """Admin page to view and manage all students."""
    # Query all students from the database, ordered by name
    students = Student.query.filter_by(role=RoleEnum.STUDENT).order_by(Student.name).all()
    return render_template('admin/manage_students.html', title='Manage Students', students=students)


@main_bp.route('/admin/student/<int:student_id>')
@login_required
@admin_required
def student_detail(student_id):
    """Admin page to view details and loan history of a single student."""
    student = Student.query.get_or_404(student_id)
    # The student.loans relationship will automatically fetch all related loans!
    # No extra database query is needed here.
    return render_template('admin/student_detail.html', title=f'Details for {student.name}', student=student)