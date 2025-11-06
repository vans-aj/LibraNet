# Physical Books Seeding Guide

## Overview
This guide explains how to populate your LibraNet library system with physical books from LibriVox.

## System Architecture

### Multi-Outlet Library System
Your LibraNet platform operates with:
- **Multiple outlets across India** (Mumbai, Delhi, Bangalore, etc.)
- **E-books**: Read directly from the website
- **Audiobooks**: Listen directly from the website
- **Physical Books**: Apply to borrow → Delivered to your location

### Physical Book Specifications
- **Total Copies**: 10 per book
- **Available Copies**: 10 (initially)
- **Fine Amount**: ₹200 per book (for late returns)
- **Data Source**: LibriVox API (covers, authors, summaries)

## Quick Start

### 1. Install Dependencies
```bash
# Make sure you're in your virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install if not already installed
pip install requests
```

### 2. Run the Seeding Script
```bash
python seed_physical_books.py
```

### 3. Follow the Prompts
```
How many books do you want to add? (default: 50): 100
Add 100 physical books from LibriVox? (yes/no): yes
```

## What the Script Does

1. **Fetches from LibriVox API**
   - Book titles
   - Author names
   - Book descriptions/summaries
   - Cover images

2. **Generates Realistic Data**
   - ISBN-13 numbers
   - Categories (Fiction, Science, History, etc.)
   - Sets 10 total copies per book
   - Sets 10 available copies per book

3. **Creates Database Entries**
   - Adds books to `physical_book` table
   - Links to base `publication` table
   - Ready for loan system

## Book Borrowing Flow

```
User browses physical books
    ↓
Applies to borrow (adds to bag)
    ↓
Confirms loan request
    ↓
System checks available copies
    ↓
If available:
    - Reduces available_copies by 1
    - Creates Loan record
    - Sets return date
    ↓
Book delivered to user's location
    ↓
User returns book
    ↓
If late: Fine of ₹200 applied
```

## Fine System

### Standard Fine: ₹200 per book

**Implementation:**
```python
# In your loan return logic
from app.models.fine import Fine

# When book is returned late
fine = Fine.create_standard_fine(loan_id=loan.id)
db.session.add(fine)
db.session.commit()
```

**Fine Model Features:**
- `STANDARD_FINE_AMOUNT = ₹200`
- `create_standard_fine()` helper method
- Automatic pending status
- Balance calculation

## Database Schema

### PhysicalBook Table
```sql
- id (Primary Key, Foreign Key to Publication)
- isbn (Unique, Generated)
- total_copies (Default: 10)
- available_copies (Default: 10)
- related_courses (Used for category)
```

### Publication Table (Base)
```sql
- id (Primary Key)
- title (From LibriVox)
- author (From LibriVox)
- summary (From LibriVox, cleaned)
- image_url (From LibriVox/Archive.org)
- type ('physical_book')
```

### Fine Table
```sql
- id (Primary Key)
- amount (₹200.00)
- paid_amount (Default: 0.00)
- status (PENDING/PAID/CANCELLED)
- loan_id (Foreign Key to Loan)
```

## Customization

### Change Number of Copies
Edit `seed_physical_books.py`:
```python
physical_book = PhysicalBook(
    # ... other fields
    total_copies=20,      # Change from 10 to desired number
    available_copies=20,  # Same as total_copies
)
```

### Change Fine Amount
Edit `app/models/fine.py`:
```python
class Fine(db.Model):
    STANDARD_FINE_AMOUNT = Decimal('300.00')  # Change from 200
```

### Add More Book Categories
Edit `seed_physical_books.py`:
```python
CATEGORIES = [
    'Fiction', 'Non-Fiction', 'Science Fiction',
    'Your New Category 1',
    'Your New Category 2',
]
```

## LibriVox API Details

### Endpoint
```
https://librivox.org/api/feed/audiobooks
```

### Parameters
- `format=json`: JSON response
- `extended=1`: Full metadata
- `limit=50`: Books per request
- `offset=random`: Variety in results

### Data Retrieved
- Title
- Authors (first name, last name)
- Description (cleaned and truncated)
- Book ID (for cover image URL)

## Troubleshooting

### "No books fetched"
- Check internet connection
- LibriVox API might be down (try again later)
- Increase timeout in requests

### "Database error"
- Check if database is initialized: `flask db upgrade`
- Verify models are imported correctly
- Check for unique constraint violations

### "Duplicate books"
- Script skips duplicates automatically
- Based on title + author combination
- Increases offset to get different books

### Cover images not loading
- Archive.org links may be slow
- Images load on-demand
- Fallback to Unsplash generic book image

## Testing the System

### 1. Check Books Added
```python
from app import app, db
from app.models.physical_book import PhysicalBook

with app.app_context():
    count = PhysicalBook.query.count()
    print(f"Total physical books: {count}")
    
    # Show first 5
    books = PhysicalBook.query.limit(5).all()
    for book in books:
        print(f"{book.title} by {book.author}")
        print(f"  Available: {book.available_copies}/{book.total_copies}")
```

### 2. Test Borrowing Flow
1. Go to Physical Books page
2. Add book to bag
3. Confirm loan
4. Check available_copies decreased
5. Return book
6. Check available_copies increased

### 3. Test Fine System
1. Create loan with past due date
2. Mark as overdue
3. Fine of ₹200 should be created
4. Check Fine.query.filter_by(status='PENDING')

## Production Deployment

### Environment Variables
Add to `.env`:
```bash
# LibriVox API settings
LIBRIVOX_API_URL=https://librivox.org/api/feed/audiobooks
LIBRIVOX_TIMEOUT=30

# Fine settings
STANDARD_FINE_AMOUNT=200
OVERDUE_CHECK_INTERVAL=24  # hours
```

### Scheduled Tasks
Set up cron job to check overdue books:
```bash
# Every day at midnight
0 0 * * * cd /path/to/LibraNet && python check_overdue_loans.py
```

### Monitoring
- Track available_copies to restock popular books
- Monitor fine collection rates
- Alert when books are frequently overdue

## Support

For issues or questions:
1. Check this README
2. Review model files in `app/models/`
3. Check seed script: `seed_physical_books.py`
4. Review loan routes: `app/routes/book_routes.py`

## Credits

- **Book Data**: LibriVox (https://librivox.org)
- **Cover Images**: Internet Archive (archive.org)
- **Fallback Images**: Unsplash
