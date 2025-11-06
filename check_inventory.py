"""
Check Physical Books Inventory
==============================
Quick utility to view current physical books in the database.
"""

from app import create_app, db
from app.models.physical_book import PhysicalBook
from app.models.loan import Loan
from sqlalchemy import func

def display_inventory():
    """Display current physical books inventory with statistics."""
    
    # Get total count
    total_books = PhysicalBook.query.count()
    
    if total_books == 0:
        print("\n📚 No physical books in database yet.")
        print("💡 Run 'python seed_physical_books.py' to add books.\n")
        return
    
    # Calculate statistics
    total_copies = db.session.query(
        func.sum(PhysicalBook.total_copies)
    ).scalar() or 0
    
    available_copies = db.session.query(
        func.sum(PhysicalBook.available_copies)
    ).scalar() or 0
    
    loaned_copies = total_copies - available_copies
    
    # Get active loans
    active_loans = Loan.query.filter_by(status='borrowed').count()
    
    print("\n" + "="*70)
    print("📚 PHYSICAL BOOKS INVENTORY")
    print("="*70)
    print(f"📖 Unique Titles: {total_books}")
    print(f"📦 Total Copies: {total_copies}")
    print(f"✅ Available Copies: {available_copies}")
    print(f"📤 Loaned Copies: {loaned_copies}")
    print(f"👥 Active Loans: {active_loans}")
    print("="*70)
    
    # Display sample books
    print("\n📖 Sample Books (First 10):\n")
    books = PhysicalBook.query.limit(10).all()
    
    for idx, book in enumerate(books, 1):
        availability = f"{book.available_copies}/{book.total_copies}"
        status = "✅ Available" if book.is_available else "❌ All loaned"
        
        print(f"{idx}. {book.title[:50]}")
        print(f"   Author: {book.author}")
        print(f"   ISBN: {book.isbn}")
        print(f"   Copies: {availability} | {status}")
        
        if book.related_courses:
            print(f"   Category: {book.related_courses}")
        print()
    
    # Show most popular books (least available copies)
    print("\n🔥 Most Popular Books (Currently Borrowed):\n")
    popular = PhysicalBook.query.filter(
        PhysicalBook.available_copies < PhysicalBook.total_copies
    ).order_by(PhysicalBook.available_copies).limit(5).all()
    
    if popular:
        for idx, book in enumerate(popular, 1):
            borrowed = book.total_copies - book.available_copies
            print(f"{idx}. {book.title[:50]}")
            print(f"   Borrowed: {borrowed}/{book.total_copies} copies")
            print()
    else:
        print("   No books currently borrowed.\n")
    
    # Show fully available books
    fully_available = PhysicalBook.query.filter(
        PhysicalBook.available_copies == PhysicalBook.total_copies
    ).count()
    
    print(f"\n📚 Fully Available Books: {fully_available}/{total_books}")
    print("="*70 + "\n")


def show_book_details(book_id=None, title=None):
    """
    Show detailed information about a specific book.
    
    Args:
        book_id: Book ID to look up
        title: Book title to search for (partial match)
    """
    if book_id:
        book = PhysicalBook.query.get(book_id)
    elif title:
        book = PhysicalBook.query.filter(
            PhysicalBook.title.ilike(f"%{title}%")
        ).first()
    else:
        print("❌ Please provide either book_id or title")
        return
    
    if not book:
        print("❌ Book not found")
        return
    
    print("\n" + "="*70)
    print("📖 BOOK DETAILS")
    print("="*70)
    print(f"ID: {book.id}")
    print(f"Title: {book.title}")
    print(f"Author: {book.author}")
    print(f"ISBN: {book.isbn}")
    print(f"Category: {book.related_courses or 'Not specified'}")
    print(f"\nTotal Copies: {book.total_copies}")
    print(f"Available Copies: {book.available_copies}")
    print(f"Loaned Copies: {book.total_copies - book.available_copies}")
    print(f"\nStatus: {'✅ Available' if book.is_available else '❌ All copies loaned'}")
    
    if book.summary:
        print(f"\nSummary:")
        print(f"{book.summary[:200]}...")
    
    if book.image_url:
        print(f"\nCover Image: {book.image_url}")
    
    print("="*70 + "\n")


if __name__ == '__main__':
    import sys
    
    # Create Flask app instance
    app = create_app()
    
    with app.app_context():
        if len(sys.argv) > 1:
            # Show specific book details
            if sys.argv[1].isdigit():
                show_book_details(book_id=int(sys.argv[1]))
            else:
                show_book_details(title=' '.join(sys.argv[1:]))
        else:
            # Show general inventory
            display_inventory()
