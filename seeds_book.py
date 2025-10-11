import csv
import os
from app import create_app, db
from app.models.physical_book import PhysicalBook

def seed_books_from_csv(csv_file_path):
    """
    Seed the physical_books table from a CSV file.
    
    Expected CSV columns (EXACT NAMES):
    - Author
    - Book Name
    - Available Copies
    - ISBN Code
    - Related Courses (optional)
    - Summary (optional)
    - Book Link (optional - will be ignored)
    
    Usage:
        python seed_books.py
    """
    
    app = create_app()
    
    with app.app_context():
        # Check if file exists
        if not os.path.exists(csv_file_path):
            print(f"❌ Error: CSV file not found at {csv_file_path}")
            return
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Verify headers
                if not reader.fieldnames:
                    print("❌ Error: CSV file is empty")
                    return
                
                print(f"📖 Starting to seed books from {csv_file_path}")
                print(f"📋 Found columns: {reader.fieldnames}")
                print("-" * 60)
                
                books_added = 0
                books_skipped = 0
                errors = []
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 because row 1 is header
                    try:
                        # Get required fields - UPDATED TO MATCH YOUR CSV COLUMN NAMES
                        title = row.get('Book Name', '').strip()
                        author = row.get('Author', '').strip()
                        
                        if not title or not author:
                            errors.append(f"Row {row_num}: Missing 'Book Name' or 'Author' - SKIPPED")
                            books_skipped += 1
                            continue
                        
                        # Check if book already exists (by title and author)
                        existing_book = PhysicalBook.query.filter_by(
                            title=title,
                            author=author
                        ).first()
                        
                        if existing_book:
                            errors.append(f"Row {row_num}: '{title}' already exists - SKIPPED")
                            books_skipped += 1
                            continue
                        
                        # Get optional fields - UPDATED TO MATCH YOUR CSV COLUMN NAMES
                        isbn = row.get('ISBN Code', '').strip() or None
                        
                        # Get total_copies from "Available Copies" column
                        try:
                            total_copies = int(row.get('Available Copies', 1))
                        except ValueError:
                            total_copies = 1
                        
                        related_courses = row.get('Related Courses', '').strip() or None
                        summary = row.get('Summary', '').strip() or None
                        
                        # Validate total_copies
                        if total_copies < 1:
                            total_copies = 1
                        
                        # Create new book
                        new_book = PhysicalBook(
                            title=title,
                            author=author,
                            isbn=isbn,
                            total_copies=total_copies,
                            available_copies=total_copies,
                            related_courses=related_courses,
                            summary=summary
                        )
                        
                        db.session.add(new_book)
                        books_added += 1
                        print(f"✅ Row {row_num}: Added '{title}' by {author} ({total_copies} copies)")
                        
                    except ValueError as e:
                        errors.append(f"Row {row_num}: Invalid data format - {str(e)}")
                        books_skipped += 1
                    except Exception as e:
                        errors.append(f"Row {row_num}: Unexpected error - {str(e)}")
                        books_skipped += 1
                
                # Commit all changes
                try:
                    db.session.commit()
                    print("-" * 60)
                    print(f"✅ Successfully added {books_added} books to database")
                    print(f"⏭️  Skipped {books_skipped} books")
                    
                    if errors:
                        print("\n⚠️  Details:")
                        for error in errors:
                            print(f"   {error}")
                    
                except Exception as e:
                    db.session.rollback()
                    print(f"❌ Error committing to database: {str(e)}")
                    return False
        
        except Exception as e:
            print(f"❌ Error reading CSV file: {str(e)}")
            return False
    
    return True


if __name__ == "__main__":
    # Path to your CSV file
    csv_path = "books.csv"  # Change this to your CSV file path
    
    seed_books_from_csv(csv_path)