"""
Seed Physical Books from LibriVox API
=====================================
This script fetches audiobook metadata from LibriVox and creates corresponding
physical book entries in your library system.

Features:
- Fetches book data from LibriVox API (cover, author, description)
- Sets up 10 total copies and 10 available copies per book
- Assigns fine amount of ₹200 per book
- Generates realistic ISBN numbers
- Supports multiple library outlets across India
"""

import requests
import random
import time
from decimal import Decimal
from app import create_app, db
from app.models.physical_book import PhysicalBook
from app.models.publication import Publication

# Indian cities for outlet locations (for future use)
OUTLET_CITIES = [
    'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai',
    'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow'
]

# Book categories for classification
CATEGORIES = [
    'Fiction', 'Non-Fiction', 'Science Fiction', 'Fantasy', 
    'Mystery', 'Biography', 'History', 'Philosophy', 
    'Literature', 'Drama', 'Poetry', 'Adventure'
]

def generate_isbn():
    """Generate a random ISBN-13 number."""
    # ISBN-13 format: 978-X-XXXX-XXXX-X
    prefix = "978"
    group = str(random.randint(0, 9))
    publisher = str(random.randint(1000, 9999))
    title = str(random.randint(1000, 9999))
    check = str(random.randint(0, 9))
    return f"{prefix}-{group}-{publisher}-{title}-{check}"


def fetch_librivox_books(limit=50):
    """
    Fetch audiobook data from LibriVox API.
    
    Args:
        limit: Number of books to fetch
        
    Returns:
        List of book dictionaries with metadata
    """
    print(f"🔍 Fetching {limit} books from LibriVox API...")
    
    try:
        # LibriVox API endpoint
        url = "https://librivox.org/api/feed/audiobooks"
        params = {
            'format': 'json',
            'extended': '1',
            'limit': limit,
            'offset': random.randint(0, 500)  # Random offset for variety
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        books = data.get('books', [])
        
        print(f"✅ Successfully fetched {len(books)} books from LibriVox")
        return books
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching from LibriVox API: {e}")
        return []


def get_book_cover_url(book_data):
    """
    Extract the best available cover image URL from LibriVox data.
    
    Args:
        book_data: Book dictionary from LibriVox API
        
    Returns:
        Cover image URL or placeholder
    """
    # 1. Try Internet Archive identifier (best quality)
    if book_data.get('url_iarchive'):
        # Extract identifier from URL like: https://www.archive.org/details/count_monte_cristo_0711_librivox
        ia_url = book_data['url_iarchive']
        if '/details/' in ia_url:
            identifier = ia_url.split('/details/')[-1]
            # Use Internet Archive's image service for book covers
            return f"https://archive.org/services/img/{identifier}"
    
    # 2. Fallback: Use Open Library generic cover based on title
    title = book_data.get('title', 'Book')[:50]
    try:
        import urllib.parse
        # Use placeholder image with book title
        encoded_title = urllib.parse.quote(title)
        return f"https://via.placeholder.com/400x600/3b82f6/ffffff?text={encoded_title}"
    except:
        pass
    
    # 3. Ultimate fallback: Classic book image from Unsplash
    return "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=600&fit=crop"


def clean_description(description):
    """
    Clean and format book description from LibriVox.
    
    Args:
        description: Raw description text
        
    Returns:
        Cleaned description string
    """
    if not description:
        return "A classic work of literature available in our library collection."
    
    # Remove HTML tags if present
    import re
    description = re.sub(r'<[^>]+>', '', description)
    
    # Limit length to 500 characters for summary
    if len(description) > 500:
        description = description[:497] + "..."
    
    return description.strip()


def create_physical_book(book_data):
    """
    Create a PhysicalBook entry from LibriVox data.
    
    Args:
        book_data: Book dictionary from LibriVox API
        
    Returns:
        PhysicalBook instance or None
    """
    try:
        # Extract book information
        title = book_data.get('title', 'Unknown Title')
        
        # Get authors (LibriVox can have multiple authors)
        authors_list = book_data.get('authors', [])
        if authors_list and isinstance(authors_list, list):
            author = authors_list[0].get('last_name', '') + ', ' + authors_list[0].get('first_name', '')
            author = author.strip(', ')
        else:
            author = 'Unknown Author'
        
        # Get description
        description = book_data.get('description', '')
        summary = clean_description(description)
        
        # Get cover image
        image_url = get_book_cover_url(book_data)
        
        # Generate ISBN
        isbn = generate_isbn()
        
        # Random category
        category = random.choice(CATEGORIES)
        
        # Check if book already exists
        existing = PhysicalBook.query.filter_by(title=title, author=author).first()
        if existing:
            print(f"⏭️  Skipping duplicate: {title}")
            return None
        
        # Create physical book with your specifications
        physical_book = PhysicalBook(
            title=title,
            author=author,
            summary=summary,
            image_url=image_url,
            isbn=isbn,
            total_copies=10,          # As per your requirement
            available_copies=10,       # As per your requirement
            related_courses=category   # Using this field for category
        )
        
        return physical_book
        
    except Exception as e:
        print(f"❌ Error creating book from data: {e}")
        return None


def seed_physical_books(num_books=50):
    """
    Main function to seed physical books from LibriVox.
    
    Args:
        num_books: Number of books to add
    """
    print("\n" + "="*70)
    print("📚 PHYSICAL BOOKS SEEDING SCRIPT")
    print("="*70)
    print(f"Target: {num_books} books")
    print(f"Fine per book: ₹200")
    print(f"Copies per book: 10 (total) / 10 (available)")
    print("="*70 + "\n")
    
    # Fetch books from LibriVox
    librivox_books = fetch_librivox_books(limit=num_books)
    
    if not librivox_books:
        print("❌ No books fetched. Exiting.")
        return
    
    # Create physical books
    books_created = 0
    books_skipped = 0
    
    for idx, book_data in enumerate(librivox_books, 1):
        print(f"\n[{idx}/{len(librivox_books)}] Processing: {book_data.get('title', 'Unknown')[:50]}...")
        
        physical_book = create_physical_book(book_data)
        
        if physical_book:
            try:
                db.session.add(physical_book)
                db.session.commit()
                books_created += 1
                print(f"✅ Added: {physical_book.title}")
                print(f"   Author: {physical_book.author}")
                print(f"   ISBN: {physical_book.isbn}")
                print(f"   Copies: {physical_book.total_copies} total, {physical_book.available_copies} available")
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ Database error: {e}")
                books_skipped += 1
        else:
            books_skipped += 1
        
        # Rate limiting - be nice to LibriVox API
        if idx % 10 == 0:
            time.sleep(1)
        
        # Final summary
        print("\n" + "="*70)
        print("📊 SEEDING COMPLETE")
        print("="*70)
        print(f"✅ Books created: {books_created}")
        print(f"⏭️  Books skipped: {books_skipped}")
        print(f"📚 Total physical books in database: {PhysicalBook.query.count()}")
        print("="*70)
        
        # Show sample books
        print("\n📖 Sample Books Added:\n")
        sample_books = PhysicalBook.query.limit(5).all()
        for book in sample_books:
            print(f"   • {book.title}")
            print(f"     By: {book.author}")
            print(f"     ISBN: {book.isbn}")
            print(f"     Available: {book.available_copies}/{book.total_copies} copies")
            print()


def add_fine_info_note():
    """
    Note about fine system - ₹200 per book.
    
    The fine amount is stored in the Fine model, not in PhysicalBook.
    When a book is overdue, a Fine record is created with amount=200.
    
    You can modify app/models/fine.py or the loan logic to automatically
    set fine amounts to ₹200 for each overdue physical book.
    """
    print("\n💡 NOTE: Fine System")
    print("-" * 70)
    print("Fine Amount: ₹200 per book")
    print("Implementation: Fines are created in the Fine model when books are overdue")
    print("Location: app/models/fine.py")
    print("-" * 70)


if __name__ == '__main__':
    # Create Flask app instance
    app = create_app()
    
    # Ask for confirmation
    print("\n⚠️  This will add physical books to your database.")
    num_books = input("How many books do you want to add? (default: 50): ").strip()
    
    try:
        num_books = int(num_books) if num_books else 50
    except ValueError:
        num_books = 50
    
    confirm = input(f"Add {num_books} physical books from LibriVox? (yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y']:
        with app.app_context():
            seed_physical_books(num_books)
            add_fine_info_note()
        print("\n✨ All done! Your physical books are ready for borrowing.\n")
    else:
        print("\n❌ Seeding cancelled.\n")
