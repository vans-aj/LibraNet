# In app/routes/admin_routes.py

from flask import render_template, abort, flash, redirect, url_for, request
from flask_login import login_required, current_user
from functools import wraps
from app.routes import main_bp
from app.models.physical_book import PhysicalBook # <-- CORRECTED IMPORT
from app.models.student import Student
from app.forms import BookForm
from app import db

# --- This decorator is temporarily simplified for testing ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # We will build a proper admin authentication system later.
        # For now, we just check if the user is logged in.
        if not current_user.is_authenticated:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@main_bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html', title='Admin Dashboard')


@main_bp.route('/admin/books')
@login_required
@admin_required
def manage_books():
    # --- CORRECTED to use PhysicalBook ---
    books = PhysicalBook.query.order_by(PhysicalBook.title).all()
    return render_template('admin/manage_books.html', title='Manage Books', books=books)


@main_bp.route('/admin/add_book', methods=['GET', 'POST'])
@login_required
@admin_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        new_book = PhysicalBook(
            title=form.title.data,
            author=form.author.data,
            summary=form.summary.data, # <-- This was missing from your paste
            isbn=form.isbn.data,
            # format=form.format.data, <-- CORRECTED: Removed this line
            total_copies=form.total_copies.data,
            available_copies=form.total_copies.data
        )
        db.session.add(new_book)
        db.session.commit()
        flash(f'Book "{new_book.title}" has been added successfully!', 'success')
        return redirect(url_for('main.manage_books'))
    return render_template('admin/add_book.html', title='Add New Book', form=form)


@main_bp.route('/admin/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_book(book_id):
    # --- CORRECTED to use PhysicalBook ---
    book = PhysicalBook.query.get_or_404(book_id)
    form = BookForm(original_book=book)
    if form.validate_on_submit():
        borrowed_copies = book.total_copies - book.available_copies
        new_total_copies = form.total_copies.data

        if new_total_copies < borrowed_copies:
            flash(f'Error: Total copies ({new_total_copies}) cannot be less than the number of books currently on loan ({borrowed_copies}).', 'danger')
            return redirect(url_for('main.edit_book', book_id=book_id))
        else:
            new_available_copies = new_total_copies - borrowed_copies
            book.title = form.title.data
            book.author = form.author.data
            book.summary = form.summary.data # <-- This was missing from your paste
            book.isbn = form.isbn.data
            # book.format = form.format.data, <-- CORRECTED: Removed this line
            book.total_copies = new_total_copies
            book.available_copies = new_available_copies
            
            db.session.commit()
            flash('The book has been updated successfully!', 'success')
            return redirect(url_for('main.manage_books'))
    
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.summary.data = book.summary # <-- This was missing from your paste
        form.isbn.data = book.isbn
        # form.format.data = book.format.value, <-- CORRECTED: Removed this line
        form.total_copies.data = book.total_copies
        
    return render_template('admin/add_book.html', title=f'Edit "{book.title}"', form=form)


@main_bp.route('/admin/students')
@login_required
@admin_required
def manage_students():
    # --- CORRECTED to remove the role filter ---
    students = Student.query.order_by(Student.name).all()
    return render_template('admin/manage_students.html', title='Manage Students', students=students)


@main_bp.route('/admin/student/<int:student_id>')
@login_required
@admin_required
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('admin/student_detail.html', title=f'Details for {student.name}', student=student)