# Quick Start: Physical Books Setup

## 🎯 Your Library System Overview

### Multi-Outlet Library Across India
- **E-books**: Read directly from website (no delivery needed)
- **Audiobooks**: Listen directly from website (no delivery needed)  
- **Physical Books**: Apply to borrow → We deliver to you across India

### Physical Book Details
- ✅ 10 total copies per book
- ✅ 10 available copies initially
- ✅ ₹200 fine per book for late returns
- ✅ Data from LibriVox (cover, author, summary)

## 🚀 Step-by-Step Setup

### 1️⃣ Activate Virtual Environment
```bash
cd /Users/vansajrawat/Desktop/librafinal/LibraNet
source venv/bin/activate
```

### 2️⃣ Seed Physical Books
```bash
python seed_physical_books.py
```

**You'll see:**
```
How many books do you want to add? (default: 50): 100
Add 100 physical books from LibriVox? (yes/no): yes
```

**Script will:**
- ✅ Fetch 100 books from LibriVox API
- ✅ Get cover images, authors, summaries
- ✅ Set 10 copies per book
- ✅ Generate ISBN numbers
- ✅ Save to database

### 3️⃣ Check Inventory
```bash
python check_inventory.py
```

**Output:**
```
📚 PHYSICAL BOOKS INVENTORY
====================================
📖 Unique Titles: 100
📦 Total Copies: 1000
✅ Available Copies: 1000
📤 Loaned Copies: 0
```

### 4️⃣ Test Borrowing Flow (Optional)
```bash
python test_borrowing.py
```

**This simulates:**
1. Student borrows a book
2. Available copies decrease
3. Book returned late
4. ₹200 fine created
5. Fine paid

## 📋 What Each Script Does

| Script | Purpose |
|--------|---------|
| `seed_physical_books.py` | Add books from LibriVox to database |
| `check_inventory.py` | View current book inventory |
| `test_borrowing.py` | Test complete borrow/return workflow |

## 🔍 Checking Specific Books

```bash
# By book ID
python check_inventory.py 1

# By title (partial match)
python check_inventory.py "Pride and Prejudice"
```

## 💰 Fine System Details

### When Fine is Created
- Book returned after due date
- Amount: ₹200 (standard)
- Status: PENDING

### Fine Model Location
`app/models/fine.py`

### Creating Fine in Code
```python
from app.models.fine import Fine

# Automatic ₹200 fine
fine = Fine.create_standard_fine(loan_id=loan.id)
db.session.add(fine)
db.session.commit()
```

## 📊 Database Tables

### physical_book
- `id` - Primary key
- `isbn` - Generated ISBN-13
- `total_copies` - Always 10
- `available_copies` - Starts at 10
- Inherits from `publication`:
  - `title` - From LibriVox
  - `author` - From LibriVox
  - `summary` - From LibriVox
  - `image_url` - Cover image

### fine
- `id` - Primary key
- `amount` - ₹200.00
- `paid_amount` - Default 0.00
- `status` - PENDING/PAID/CANCELLED
- `loan_id` - Link to loan

## 🛠️ Common Commands

```bash
# Add 50 books
python seed_physical_books.py

# Check what's in database
python check_inventory.py

# View loan statistics
python test_borrowing.py stats

# Run the app
python main.py
```

## 🌐 LibriVox API

### What We Get
- ✅ Book titles (classic literature)
- ✅ Author names (first + last)
- ✅ Book descriptions
- ✅ Cover images (via Archive.org)

### API Endpoint
```
https://librivox.org/api/feed/audiobooks
```

### Rate Limiting
- Script pauses every 10 books
- Be respectful to LibriVox servers

## ✅ Success Indicators

After seeding, you should see:

```
📊 SEEDING COMPLETE
====================================
✅ Books created: 100
⏭️  Books skipped: 0
📚 Total physical books in database: 100
====================================
```

## 🔧 Troubleshooting

### No books fetched
```bash
# Check internet connection
ping librivox.org

# Try again with smaller number
# Edit seed_physical_books.py, line ~253
```

### Database errors
```bash
# Initialize database
flask db upgrade

# Check models
python -c "from app.models.physical_book import PhysicalBook; print('OK')"
```

### Duplicate books
- Script automatically skips
- Based on title + author
- Not an error

## 📱 Using in Your App

### Routes to Create

**List Physical Books**
```python
@main_bp.route('/physical-books')
def list_physical_books():
    books = PhysicalBook.query.filter(
        PhysicalBook.available_copies > 0
    ).all()
    return render_template('physical_books.html', books=books)
```

**Borrow Book**
```python
@main_bp.route('/borrow/<int:book_id>')
@login_required
def borrow_book(book_id):
    book = PhysicalBook.query.get_or_404(book_id)
    
    if not book.is_available:
        flash('No copies available', 'warning')
        return redirect(url_for('main.list_physical_books'))
    
    # Create loan
    loan = Loan(
        student_id=current_user.id,
        book_id=book.id,
        borrowed_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14)
    )
    
    book.available_copies -= 1
    
    db.session.add(loan)
    db.session.commit()
    
    flash('Book borrowed! We will deliver it soon.', 'success')
    return redirect(url_for('main.my_loans'))
```

## 🎓 Next Steps

1. ✅ Run seed script
2. ✅ Check inventory
3. ✅ Test borrowing workflow
4. 🔲 Create UI for physical books
5. 🔲 Add delivery tracking
6. 🔲 Set up fine notifications
7. 🔲 Create admin panel for inventory

## 📚 Full Documentation

See `PHYSICAL_BOOKS_SETUP.md` for complete details on:
- System architecture
- Customization options
- Production deployment
- Monitoring tips

---

**Ready?** Run:
```bash
python seed_physical_books.py
```

🎉 Happy Reading!
