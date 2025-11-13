"""
Routes for photo upload and book management with images
"""

from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.routes import main_bp
from app import db
from app.utils.file_upload import ImageUploader
from app.models.physical_book import PhysicalBook
from app.models.book_image import BookImage
from app.models.loan import Loan
from app.forms import AddPhysicalBookForm
from werkzeug.utils import secure_filename
import os


@main_bp.route('/test-upload', methods=['GET'])
@login_required
def test_upload_page():
    """Test page for photo upload"""
    return render_template('test_upload.html', title='Test Photo Upload')


@main_bp.route('/upload-image', methods=['POST'])
@login_required
def upload_image():
    """
    Handle single image upload
    
    Returns JSON with upload status and image paths
    """
    try:
        # Check if file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Initialize uploader
        uploader = ImageUploader()
        
        # Validate file size
        uploader.validate_file_size(file)
        
        # Upload and process image
        result = uploader.upload_image(file, subfolder='books')
        
        return jsonify({
            'success': True,
            'message': 'Image uploaded successfully',
            'data': result
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@main_bp.route('/upload-multiple-images', methods=['POST'])
@login_required
def upload_multiple_images():
    """
    Handle multiple image uploads
    
    Returns JSON with upload status and list of image paths
    """
    try:
        # Check if files are present
        if 'images' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('images')
        
        if not files or len(files) == 0:
            return jsonify({'error': 'No files selected'}), 400
        
        # Initialize uploader
        uploader = ImageUploader()
        
        # Validate each file size
        for file in files:
            uploader.validate_file_size(file)
        
        # Upload and process images
        results = uploader.upload_multiple_images(files, subfolder='books', max_images=5)
        
        return jsonify({
            'success': True,
            'message': f'{len(results)} images uploaded successfully',
            'data': results
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@main_bp.route('/delete-image', methods=['POST'])
@login_required
def delete_image():
    """
    Delete uploaded image
    
    Expects JSON with image paths
    """
    try:
        data = request.get_json()
        
        if not data or 'image_paths' not in data:
            return jsonify({'error': 'Image paths not provided'}), 400
        
        # Initialize uploader
        uploader = ImageUploader()
        
        # Delete image
        uploader.delete_image(data['image_paths'])
        
        return jsonify({
            'success': True,
            'message': 'Image deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Delete failed: {str(e)}'}), 500


@main_bp.route('/add-physical-book', methods=['GET', 'POST'])
@login_required
def add_physical_book():
    """
    Add a new physical book with images to the library
    """
    form = AddPhysicalBookForm()
    
    if form.validate_on_submit():
        try:
            # Create new book
            book = PhysicalBook(
                title=form.title.data,
                author=form.author.data,
                summary=form.summary.data,
                isbn=form.isbn.data if form.isbn.data else None,
                total_copies=form.total_copies.data,
                available_copies=form.total_copies.data,
                related_courses=form.related_courses.data if form.related_courses.data else None,
                added_by_user_id=current_user.id  # Track who added this book
            )
            
            # Save book to database first (to get book.id)
            db.session.add(book)
            db.session.flush()  # Get book.id without committing
            
            # Handle image uploads if any
            if 'book_images' in request.files:
                files = request.files.getlist('book_images')
                files = [f for f in files if f.filename != '']  # Filter empty files
                
                if files:
                    uploader = ImageUploader()
                    
                    # Upload images (max 3)
                    if len(files) > 3:
                        files = files[:3]
                    
                    for idx, file in enumerate(files):
                        # Upload and process image
                        result = uploader.upload_image(file, subfolder='books')
                        
                        # Create BookImage record
                        book_image = BookImage(
                            book_id=book.id,
                            original_path=result['original'],
                            large_path=result['large'],
                            thumbnail_path=result['thumbnail'],
                            filename=result['filename'],
                            is_primary=(idx == 0)  # First image is primary
                        )
                        db.session.add(book_image)
                    
                    # Set book's image_url to the primary image
                    primary_image = BookImage.query.filter_by(book_id=book.id, is_primary=True).first()
                    if primary_image:
                        book.image_url = '/static/' + primary_image.large_path
            
            # Commit all changes
            db.session.commit()
            
            flash(f'✓ Book "{book.title}" added successfully!', 'success')
            return redirect(url_for('main.book_detail', book_id=book.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error adding book: {str(e)}', 'danger')
            print(f"ERROR: {str(e)}")  # Log to console
            return render_template('add_book.html', title='Add Book', form=form)
    
    # If form validation failed
    elif request.method == 'POST':
        flash('❌ Please fix the errors below', 'danger')
        print(f"Form errors: {form.errors}")  # Log validation errors
    
    return render_template('add_book.html', title='Add Book', form=form)


@main_bp.route('/delete-book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    """
    Delete a book - only if the current user added it
    """
    book = PhysicalBook.query.get_or_404(book_id)
    
    # Check if the user is the one who added this book
    if book.added_by_user_id != current_user.id:
        flash('❌ You can only delete books that you added', 'danger')
        return redirect(url_for('main.book_detail', book_id=book_id))
    
    # Check if there are any active loans
    active_loans = Loan.query.filter_by(book_id=book_id, status='active').count()
    if active_loans > 0:
        flash('❌ Cannot delete book with active loans', 'danger')
        return redirect(url_for('main.book_detail', book_id=book_id))
    
    try:
        # Delete associated images from filesystem
        book_images = BookImage.query.filter_by(book_id=book_id).all()
        uploader = ImageUploader()
        
        for img in book_images:
            # Create dictionary for delete_image method
            image_paths = {
                'original': img.original_path,
                'large': img.large_path,
                'thumbnail': img.thumbnail_path
            }
            # Delete files from filesystem
            uploader.delete_image(image_paths)
            # Delete from database
            db.session.delete(img)
        
        # Delete the book
        db.session.delete(book)
        db.session.commit()
        
        flash(f'✓ Book "{book.title}" deleted successfully', 'success')
        return redirect(url_for('main.list_books'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error deleting book: {str(e)}', 'danger')
        return redirect(url_for('main.book_detail', book_id=book_id))


@main_bp.route('/my-listings')
@login_required
def my_listings():
    """
    Show all books added by the current user
    """
    # Get all books added by current user
    my_books = PhysicalBook.query.filter_by(added_by_user_id=current_user.id).order_by(PhysicalBook.id.desc()).all()
    
    return render_template('my_listings.html', title='My Listings', books=my_books)
