import csv
import os
from app import create_app, db
from app.models.physical_book import PhysicalBook
import re

def convert_google_drive_url(url):
    """
    Converts a Google Drive sharing URL to a direct, embeddable image link.
    Handles both '.../d/FILE_ID/...' and '.../uc?id=FILE_ID' formats.
    """
    if not url or "drive.google.com" not in url:
        return url

    # Use regex to find the file ID
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    
    match = re.search(r"id=([a-zA-Z0-9_-]+)", url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=view&id={file_id}"

    # If it's a share.google link
    if "share.google" in url:
        # This is a bit of a guess, but often the last part is the key
        file_id = url.split('/')[-1]
        return f"https://drive.google.com/uc?export=view&id={file_id}"

    return url # Return original if no ID is found

def seed_books_from_csv(csv_file_path):
    """
    Seed the physical_books table from a CSV file.
    It will first DELETE all existing books and then add the new ones,
    converting Google Drive links to a direct format.
    """
    app = create_app()
    with app.app_context():
        try:
            # Delete all existing books to ensure a fresh start
            num_deleted = db.session.query(PhysicalBook).delete()
            db.session.commit()
            if num_deleted > 0:
                print(f"✅ Successfully deleted {num_deleted} existing books.")

        except Exception as e:
            db.session.rollback()
            print(f"❌ An error occurred while deleting books: {str(e)}")
            return

        if not os.path.exists(csv_file_path):
            print(f"❌ Error: CSV file not found at {csv_file_path}")
            return
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                if not reader.fieldnames:
                    print("❌ Error: CSV file is empty")
                    return
                
                print(f"📖 Starting to seed books from {csv_file_path}")
                
                books_added = 0
                
                for row in reader:
                    title = row.get('Book Name', '').strip()
                    author = row.get('Author', '').strip()
                    
                    if not title or not author:
                        continue
                    
                    total_copies = int(row.get('Available Copies', 1))
                    
                    # Get the original URL and convert it
                    original_url = row.get('Book Link', '').strip() or None
                    image_url = convert_google_drive_url(original_url)

                    new_book = PhysicalBook(
                        title=title,
                        author=author,
                        isbn=row.get('ISBN Code', '').strip() or None,
                        total_copies=max(1, total_copies),
                        available_copies=max(1, total_copies),
                        related_courses=row.get('Related Courses', '').strip() or None,
                        summary=row.get('Summary', '').strip() or None,
                        image_url=image_url
                    )
                    
                    db.session.add(new_book)
                    books_added += 1

                db.session.commit()
                print(f"✅ Successfully added {books_added} new books.")
        
        except Exception as e:
            db.session.rollback()
            print(f"❌ An error occurred during seeding: {str(e)}")

if __name__ == "__main__":
    csv_path = "books.csv"
    seed_books_from_csv(csv_path)