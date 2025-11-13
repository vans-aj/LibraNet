# LibraNet Feature Roadmap & Implementation Plan

## 🎯 Overview
Before deployment, we need to implement several major features to make LibraNet a complete library management system with modern capabilities.

---

## 📋 Feature List

### ✅ Already Implemented
- [x] User Authentication (Login/Register/OTP)
- [x] Physical Books Management
- [x] E-books System
- [x] Audiobooks System
- [x] Loan Management
- [x] Subscription Tiers
- [x] Payment Integration (Razorpay)
- [x] Email System
- [x] Chatbot Assistant
- [x] Profile Management with Phone Number
- [x] OAuth (Google, GitHub)

---

## 🚀 Features to Implement

### 1. 🤖 ML Book Recommendation System
**Priority: HIGH**

**Problem:** Users need personalized book suggestions but we don't have a dataset.

**Solution:**
- **Phase 1**: Create synthetic dataset from existing data
  - Track user interactions (views, searches, loans)
  - Generate ratings from loan history
  - Create user-book interaction matrix
  
- **Phase 2**: Implement recommendation algorithms
  - **Collaborative Filtering**: Based on similar users' preferences
  - **Content-Based**: Based on book attributes (genre, author)
  - **Hybrid Approach**: Combine both methods

- **Phase 3**: ML Model
  ```python
  # Techniques to use:
  - Matrix Factorization (SVD)
  - K-Nearest Neighbors (KNN)
  - Neural Collaborative Filtering
  - Use scikit-learn or TensorFlow
  ```

**Database Changes:**
```python
class BookView(db.Model):
    """Track when users view books"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer)
    book_type = db.Column(db.String(20))  # physical, ebook, audiobook
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)

class BookRating(db.Model):
    """Explicit ratings from users"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer)
    book_type = db.Column(db.String(20))
    rating = db.Column(db.Float)  # 1-5 stars
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Files to Create:**
- `app/services/recommendation_engine.py`
- `app/ml/train_model.py`
- `app/ml/generate_dataset.py`
- `app/models/interaction.py`

**Timeline:** 1 week

---

### 2. 📍 User Address Management
**Priority: MEDIUM**

**Why:** Essential for physical book delivery, library card, and user marketplace.

**Database Changes:**
```python
# In user.py model
class User(UserMixin, db.Model):
    # ... existing fields ...
    
    # Address fields
    street_address = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(100), nullable=True, default='India')
    
    # Or create separate Address table for multiple addresses
```

**OR Better Approach - Separate Table:**
```python
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address_type = db.Column(db.String(20))  # home, work, library
    street = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100), default='India')
    is_default = db.Column(db.Boolean, default=False)
```

**UI Changes:**
- Add address section to profile page
- Create address management page
- Add address selection during book checkout

**Files to Modify:**
- `app/models/user.py` or create `app/models/address.py`
- `app/forms.py` - Add AddressForm
- `app/templates/profile.html`
- `app/routes/auth_routes.py`

**Timeline:** 2 days

---

### 3. ⭐ Book Review System
**Priority: HIGH**

**Features:**
- Users can rate books (1-5 stars)
- Write text reviews
- Edit/delete their own reviews
- View all reviews on book detail page
- Display average rating
- Sort reviews (most helpful, recent, highest/lowest)

**Database Model:**
```python
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer)
    book_type = db.Column(db.String(20))  # physical, ebook, audiobook
    rating = db.Column(db.Integer)  # 1-5
    title = db.Column(db.String(100))  # Review title
    comment = db.Column(db.Text)
    helpful_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='reviews')

class ReviewHelpful(db.Model):
    """Track which users found a review helpful"""
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
```

**Files to Create:**
- `app/models/review.py`
- `app/routes/review_routes.py`
- `app/templates/reviews/review_section.html`

**Timeline:** 3 days

---

### 4. 📝 Book Summarization (AI)
**Priority: MEDIUM**

**Approach:**
- Use existing LangChain integration
- Generate summaries on-demand or batch process
- Store summaries in database
- Allow Hindi translation of summaries

**Implementation:**
```python
# app/services/book_summarizer.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

class BookSummarizer:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro")
    
    def generate_summary(self, book_title, author, full_text=None):
        """Generate book summary"""
        prompt = f"""
        Generate a concise 150-word summary of the book:
        Title: {book_title}
        Author: {author}
        
        Focus on:
        - Main plot/themes
        - Key characters
        - Important takeaways
        """
        return self.llm.invoke(prompt)
```

**Database Changes:**
```python
# Add to PhysicalBook, Ebook, Audiobook models
summary = db.Column(db.Text, nullable=True)
summary_generated_at = db.Column(db.DateTime, nullable=True)
```

**Timeline:** 2 days

---

### 5. 🌐 English to Hindi Translation
**Priority: MEDIUM**

**Options:**
1. **Google Translate API** (Free tier: 500k chars/month)
2. **IndicTrans** (Offline, specialized for Indian languages)
3. **LangChain + Gemini** (Use existing integration)

**Recommended: LangChain + Gemini**
```python
# app/services/translator.py
class Translator:
    def translate_to_hindi(self, text):
        prompt = f"Translate the following to Hindi: {text}"
        return self.llm.invoke(prompt)
```

**UI Implementation:**
- Add language toggle button (🇬🇧 / 🇮🇳)
- Store language preference in session/user profile
- Translate on-the-fly or cache translations

**Timeline:** 2 days

---

### 6. 📚 User Book Marketplace (Sell Old Books)
**Priority: HIGH**

**Concept:**
- Users can list their old books for sale
- Upload photos of book condition
- Set price
- Other users can buy
- Peer-to-peer marketplace within library

**Database Model:**
```python
class UserListedBook(db.Model):
    """Books listed by users for sale"""
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150))
    isbn = db.Column(db.String(20))
    condition = db.Column(db.String(20))  # new, like_new, good, fair, poor
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='available')  # available, sold, reserved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    seller = db.relationship('User', backref='listed_books')
    images = db.relationship('BookImage', backref='book', cascade='all, delete-orphan')

class BookImage(db.Model):
    """Images for user-listed books"""
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('user_listed_book.id'))
    image_path = db.Column(db.String(255))
    is_primary = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class BookPurchase(db.Model):
    """Track book purchases"""
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('user_listed_book.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    price = db.Column(db.Float)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))  # pending, confirmed, shipped, delivered
```

**Features:**
- Upload multiple photos (front, back, condition)
- Image compression and optimization
- Search/filter marketplace
- Contact seller
- Purchase flow
- Seller dashboard

**Files to Create:**
- `app/models/marketplace.py`
- `app/routes/marketplace_routes.py`
- `app/templates/marketplace/`
  - `list_book.html`
  - `browse.html`
  - `book_detail.html`
  - `my_listings.html`

**Timeline:** 1 week

---

### 7. 📸 Photo Upload System
**Priority: HIGH** (Required for marketplace)

**Storage Options:**
1. **Local Storage** (Development)
   - Store in `app/static/uploads/books/`
   - Simple, no external dependencies
   
2. **Cloudinary** (Recommended for Production)
   - Free tier: 25GB storage, 25GB bandwidth
   - Automatic image optimization
   - CDN delivery
   
3. **AWS S3** (Scalable)
   - Pay as you go
   - Industry standard

**Implementation:**
```python
# config.py
UPLOAD_FOLDER = 'app/static/uploads/books'
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# app/utils/file_upload.py
from PIL import Image
import os

class ImageUploader:
    def compress_image(self, image_path, max_size=(800, 800)):
        """Compress and resize image"""
        img = Image.open(image_path)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(image_path, optimize=True, quality=85)
    
    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

**Timeline:** 2 days

---

### 8. 📊 ML Dataset Creation
**Priority: HIGH** (For recommendations)

**Strategy:**
Since you don't have real user data yet, we'll create synthetic data:

```python
# app/ml/generate_dataset.py
import pandas as pd
import numpy as np

def generate_synthetic_data():
    """Generate synthetic user-book interaction data"""
    
    # Get all books
    books = PhysicalBook.query.all()
    users = User.query.all()
    
    # Generate realistic interactions
    interactions = []
    
    for user in users:
        # Each user interacts with 5-20 books
        num_interactions = np.random.randint(5, 20)
        
        for _ in range(num_interactions):
            book = np.random.choice(books)
            
            # Generate rating (skewed towards positive)
            rating = np.random.choice([3, 4, 5], p=[0.2, 0.4, 0.4])
            
            interactions.append({
                'user_id': user.id,
                'book_id': book.id,
                'rating': rating,
                'timestamp': generate_random_timestamp()
            })
    
    df = pd.DataFrame(interactions)
    df.to_csv('data/interactions.csv', index=False)
    return df
```

**Real Data Collection:**
```python
# Track user behavior
@main_bp.route('/book/<int:id>')
def book_detail(id):
    # Track view
    if current_user.is_authenticated:
        view = BookView(
            user_id=current_user.id,
            book_id=id,
            book_type='physical'
        )
        db.session.add(view)
        db.session.commit()
    
    # ... rest of route
```

**Timeline:** 3 days

---

### 9. 🔧 Small Fixes & Improvements
**Priority: ONGOING**

**List of Known Issues:**
- [ ] Mobile responsiveness on profile page
- [ ] Form validation improvements
- [ ] Error message clarity
- [ ] Loading states for async operations
- [ ] Better search functionality
- [ ] Pagination for book lists
- [ ] Sort and filter options
- [ ] Accessibility improvements
- [ ] Dark mode consistency
- [ ] Email templates styling
- [ ] Password strength indicator
- [ ] Session timeout handling

**Timeline:** Ongoing

---

## 📅 Implementation Timeline

### Phase 1: Core Features (2 weeks)
1. **Week 1:**
   - Day 1-2: User Address Management ✅
   - Day 3-5: Book Review System ✅
   - Day 6-7: Photo Upload System ✅

2. **Week 2:**
   - Day 1-5: User Book Marketplace ✅
   - Day 6-7: ML Dataset Creation ✅

### Phase 2: AI Features (1 week)
3. **Week 3:**
   - Day 1-3: ML Recommendation System ✅
   - Day 4-5: Book Summarization ✅
   - Day 6-7: Translation Feature ✅

### Phase 3: Polish & Deploy (1 week)
4. **Week 4:**
   - Day 1-3: Testing & Bug Fixes
   - Day 4-5: UI/UX Improvements
   - Day 6-7: Deployment & Documentation

**Total Timeline: 1 Month**

---

## 🏗️ Architecture Decisions

### Database Schema
```
Users (existing)
├── Addresses (new)
├── Reviews (new)
├── BookViews (new - for ML)
├── BookRatings (new - for ML)
└── UserListedBooks (new - marketplace)
    └── BookImages (new)

Books (existing - Physical, Ebook, Audiobook)
├── Reviews (linked)
└── Summary (new field)
```

### File Structure
```
LibraNet/
├── app/
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── recommendation_engine.py
│   │   ├── train_model.py
│   │   └── generate_dataset.py
│   ├── services/
│   │   ├── chatbot.py (existing)
│   │   ├── book_summarizer.py (new)
│   │   ├── translator.py (new)
│   │   └── image_processor.py (new)
│   ├── utils/
│   │   ├── file_upload.py (new)
│   │   └── validators.py (new)
│   ├── models/
│   │   ├── address.py (new)
│   │   ├── review.py (new)
│   │   ├── marketplace.py (new)
│   │   └── interaction.py (new)
│   └── routes/
│       ├── marketplace_routes.py (new)
│       └── review_routes.py (new)
└── data/ (new)
    ├── interactions.csv
    └── trained_models/
```

---

## 🎯 Priority Order

Based on value and dependencies:

1. **Photo Upload System** (Required for marketplace)
2. **User Address Management** (Required for delivery)
3. **User Book Marketplace** (Major feature)
4. **Book Review System** (Enhances user engagement)
5. **ML Dataset Creation** (Foundation for recommendations)
6. **ML Recommendation System** (Key differentiator)
7. **Book Summarization** (Nice to have)
8. **Translation Feature** (Accessibility)
9. **Small Fixes** (Ongoing)

---

## 🚦 Let's Start!

**Which feature should we implement first?**

I recommend starting with:
1. **Photo Upload System** (2 days) - Foundation for marketplace
2. **User Address Management** (2 days) - Quick win
3. **Book Review System** (3 days) - High impact

This gives us solid groundwork in **1 week**, then we can tackle the marketplace.

**What do you think? Should we start with Photo Upload System?**
