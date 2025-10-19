from flask import render_template, abort, flash, redirect, url_for, request
from flask_login import login_required, current_user
from functools import wraps
from app.routes import main_bp
from app.models.physical_book import PhysicalBook
from app.models.ebook import Ebook
from app.models.audiobook import Audiobook
from app.models.student import Student
from app.forms import BookForm, EbookForm, AudiobookForm
from app import db

# Admin decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@main_bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html', title='Admin Dashboard')


# ===== PHYSICAL BOOKS =====
@main_bp.route('/admin/books')
@login_required
@admin_required
def manage_books():
    books = PhysicalBook.query.order_by(PhysicalBook.title).all()
    return render_template('admin/manage_books.html', title='Manage Physical Books', books=books)


@main_bp.route('/admin/add_book', methods=['GET', 'POST'])
@login_required
@admin_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        new_book = PhysicalBook(
            title=form.title.data,
            author=form.author.data,
            summary=form.summary.data,
            isbn=form.isbn.data,
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
    book = PhysicalBook.query.get_or_404(book_id)
    form = BookForm(original_book=book)
    if form.validate_on_submit():
        borrowed_copies = book.total_copies - book.available_copies
        new_total_copies = form.total_copies.data

        if new_total_copies < borrowed_copies:
            flash(f'Error: Total copies ({new_total_copies}) cannot be less than books on loan ({borrowed_copies}).', 'danger')
            return redirect(url_for('main.edit_book', book_id=book_id))
        else:
            new_available_copies = new_total_copies - borrowed_copies
            book.title = form.title.data
            book.author = form.author.data
            book.summary = form.summary.data
            book.isbn = form.isbn.data
            book.total_copies = new_total_copies
            book.available_copies = new_available_copies
            
            db.session.commit()
            flash('The book has been updated successfully!', 'success')
            return redirect(url_for('main.manage_books'))
    
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.summary.data = book.summary
        form.isbn.data = book.isbn
        form.total_copies.data = book.total_copies
        
    return render_template('admin/add_book.html', title=f'Edit "{book.title}"', form=form)


# ===== EBOOKS =====
@main_bp.route('/admin/ebooks')
@login_required
@admin_required
def manage_ebooks():
    ebooks = Ebook.query.order_by(Ebook.title).all()
    return render_template('admin/manage_ebooks.html', title='Manage Ebooks', ebooks=ebooks)


@main_bp.route('/admin/add_ebook', methods=['GET', 'POST'])
@login_required
@admin_required
def add_ebook():
    form = EbookForm()
    if form.validate_on_submit():
        new_ebook = Ebook(
            title=form.title.data,
            author=form.author.data,
            summary=form.summary.data,
            file_path=form.file_path.data,
            file_format=form.file_format.data,
            file_size_mb=form.file_size_mb.data
        )
        db.session.add(new_ebook)
        db.session.commit()
        flash(f'Ebook "{new_ebook.title}" has been added successfully!', 'success')
        return redirect(url_for('main.manage_ebooks'))
    return render_template('admin/add_ebook.html', title='Add New Ebook', form=form)


@main_bp.route('/admin/edit_ebook/<int:ebook_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_ebook(ebook_id):
    ebook = Ebook.query.get_or_404(ebook_id)
    form = EbookForm()
    
    if form.validate_on_submit():
        ebook.title = form.title.data
        ebook.author = form.author.data
        ebook.summary = form.summary.data
        ebook.file_path = form.file_path.data
        ebook.file_format = form.file_format.data
        ebook.file_size_mb = form.file_size_mb.data
        
        db.session.commit()
        flash('The ebook has been updated successfully!', 'success')
        return redirect(url_for('main.manage_ebooks'))
    
    elif request.method == 'GET':
        form.title.data = ebook.title
        form.author.data = ebook.author
        form.summary.data = ebook.summary
        form.file_path.data = ebook.file_path
        form.file_format.data = ebook.file_format
        form.file_size_mb.data = ebook.file_size_mb
    
    return render_template('admin/add_ebook.html', title=f'Edit "{ebook.title}"', form=form)


# ===== AUDIOBOOKS =====
@main_bp.route('/admin/audiobooks')
@login_required
@admin_required
def manage_audiobooks():
    audiobooks = Audiobook.query.order_by(Audiobook.title).all()
    return render_template('admin/manage_audiobooks.html', title='Manage Audiobooks', audiobooks=audiobooks)


@main_bp.route('/admin/add_audiobook', methods=['GET', 'POST'])
@login_required
@admin_required
def add_audiobook():
    form = AudiobookForm()
    if form.validate_on_submit():
        new_audiobook = Audiobook(
            title=form.title.data,
            author=form.author.data,
            narrator=form.narrator.data,
            summary=form.summary.data,
            file_path=form.file_path.data,
            duration_minutes=form.duration_minutes.data,
            file_format=form.file_format.data,
            file_size_mb=form.file_size_mb.data
        )
        db.session.add(new_audiobook)
        db.session.commit()
        flash(f'Audiobook "{new_audiobook.title}" has been added successfully!', 'success')
        return redirect(url_for('main.manage_audiobooks'))
    return render_template('admin/add_audiobook.html', title='Add New Audiobook', form=form)


@main_bp.route('/admin/edit_audiobook/<int:audiobook_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_audiobook(audiobook_id):
    audiobook = Audiobook.query.get_or_404(audiobook_id)
    form = AudiobookForm()
    
    if form.validate_on_submit():
        audiobook.title = form.title.data
        audiobook.author = form.author.data
        audiobook.narrator = form.narrator.data
        audiobook.summary = form.summary.data
        audiobook.file_path = form.file_path.data
        audiobook.duration_minutes = form.duration_minutes.data
        audiobook.file_format = form.file_format.data
        audiobook.file_size_mb = form.file_size_mb.data
        
        db.session.commit()
        flash('The audiobook has been updated successfully!', 'success')
        return redirect(url_for('main.manage_audiobooks'))
    
    elif request.method == 'GET':
        form.title.data = audiobook.title
        form.author.data = audiobook.author
        form.narrator.data = audiobook.narrator
        form.summary.data = audiobook.summary
        form.file_path.data = audiobook.file_path
        form.duration_minutes.data = audiobook.duration_minutes
        form.file_format.data = audiobook.file_format
        form.file_size_mb.data = audiobook.file_size_mb
    
    return render_template('admin/add_audiobook.html', title=f'Edit "{audiobook.title}"', form=form)


# ===== STUDENTS =====
@main_bp.route('/admin/students')
@login_required
@admin_required
def manage_students():
    students = Student.query.order_by(Student.name).all()
    return render_template('admin/manage_students.html', title='Manage Students', students=students)


@main_bp.route('/admin/student/<int:student_id>')
@login_required
@admin_required
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('admin/student_detail.html', title=f'Details for {student.name}', student=student)
                