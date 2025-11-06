# 📚 LibraNet - Modern Library Management System

<div align="center">

![LibraNet Logo](app/static/images/logo.svg)

**A comprehensive, modern library management system built with Flask**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#features) • [Installation](#installation) • [Configuration](#configuration) • [Usage](#usage) • [API](#api) • [Contributing](#contributing)

</div>

---

## 🌟 Features

### 📖 Multi-Format Library
- **Physical Books** - Traditional book lending and management
- **E-Books** - Digital book collection with format support (PDF, EPUB, MOBI)
- **Audiobooks** - Integrated with LibriVox API for free audiobooks
- **Smart Search** - Powered by Open Library API for comprehensive book data

### 👥 User Management
- **Flexible Registration** - Email/password or Google OAuth sign-in
- **Email Verification** - OTP-based email verification system
- **User Profiles** - Customizable user profiles with borrowing history
- **Role-Based Access** - Admin and user role separation

### 🔐 Authentication & Security
- **Google OAuth 2.0** - One-click sign-in with Google
- **Secure Passwords** - Hashed password storage with Werkzeug
- **OTP Verification** - Time-limited email verification codes
- **Session Management** - Flask-Login for secure session handling

### 💳 Subscription System
- **Tiered Plans** - Free, Basic, Premium, and Ultimate tiers
- **Payment Integration** - Razorpay payment gateway
- **Auto-renewal** - Automatic subscription renewal
- **Borrowing Limits** - Tier-based borrowing restrictions

### 📊 Loan Management
- **Smart Tracking** - Comprehensive loan history and status
- **Due Date System** - 6-month default loan period
- **Fine Calculation** - Automated overdue fine calculation
- **Return Processing** - Easy book return workflow

### 🤖 AI-Powered Chatbot
- **Book Recommendations** - AI-powered book suggestions
- **Natural Language** - Chat with LibraNet for help
- **Context-Aware** - Understands library-specific queries
- **Powered by** - LangChain + Google Gemini

### 🎨 Modern UI/UX
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark Mode** - Toggle between light and dark themes
- **Animated UI** - Smooth transitions and animations
- **Accessible** - WCAG compliant design

### 🔍 Advanced Search
- **Multi-Criteria** - Search by title, author, ISBN, genre
- **Real-time Results** - Instant search suggestions
- **Filter Options** - Filter by format, availability, rating
- **API Integration** - Open Library API for enhanced metadata

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/vans-aj/LibraNet.git
cd LibraNet
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up MySQL Database
```bash
# Log into MySQL
mysql -u root -p

# Create database
CREATE DATABASE libranet;

# Create user (optional)
CREATE USER 'teamx'@'localhost' IDENTIFIED BY 'strongpass1234';
GRANT ALL PRIVILEGES ON libranet.* TO 'teamx'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 5: Configure Environment Variables
Create a `.env` file in the project root:

```env
# Database Configuration
SQLALCHEMY_DATABASE_URI=mysql+pymysql://teamx:strongpass1234@localhost/libranet
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Flask Secret Key (generate a random string)
SECRET_KEY=your-super-secret-key-here

# Email Configuration (Gmail)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password

# Google OAuth (Get from Google Cloud Console)
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
OAUTHLIB_INSECURE_TRANSPORT=1  # Only for development

# Razorpay Payment Gateway (Get from Razorpay Dashboard)
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret

# AI Chatbot (Google Gemini API)
GOOGLE_API_KEY=your-google-gemini-api-key
LANGCHAIN_API_KEY=your-langchain-api-key
LANGCHAIN_PROJECT=LibraNet

# External APIs
LIBRIVOX_API_URL=https://librivox.org/api/feed/audiobooks
OPEN_LIBRARY_SEARCH_URL=https://openlibrary.org/search.json
OPEN_LIBRARY_COVER_URL=https://covers.openlibrary.org/b/id/
```

### Step 6: Initialize Database
```bash
# Initialize Flask-Migrate
flask db init

# Create migration
flask db migrate -m "Initial database setup"

# Apply migration
flask db upgrade
```

### Step 7: Seed Sample Data (Optional)
```bash
# Seed physical books
python seed_physical_books.py

# Seed e-books
python seed_ebooks.py

# Seed audiobooks (from LibriVox)
python seed_db.py
```

### Step 8: Run the Application
```bash
python main.py
```

The application will be available at `http://127.0.0.1:8080`

---

## ⚙️ Configuration

### Google OAuth Setup

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/

2. **Create a New Project**
   - Click "Select a project" → "New Project"
   - Name: LibraNet (or your choice)

3. **Enable Google+ API**
   - Navigate to "APIs & Services" → "Library"
   - Search for "Google+ API" and enable it

4. **Create OAuth Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Application type: Web application
   - Name: LibraNet Web Client

5. **Configure Authorized Origins**
   Add these URLs:
   ```
   http://127.0.0.1:8080
   http://localhost:8080
   ```

6. **Configure Redirect URIs**
   Add these URLs:
   ```
   http://127.0.0.1:8080/auth/google
   http://localhost:8080/auth/google
   ```

7. **Copy Credentials**
   - Copy the Client ID and Client Secret
   - Add them to your `.env` file

For detailed instructions, see [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md)

### Email Configuration (Gmail)

1. **Enable 2-Factor Authentication**
   - Go to Google Account Settings
   - Security → 2-Step Verification

2. **Generate App Password**
   - Security → App passwords
   - Select app: Mail
   - Select device: Other (Custom name)
   - Name: LibraNet
   - Copy the 16-character password

3. **Update .env File**
   ```env
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-char-app-password
   ```

### Razorpay Payment Setup

1. **Sign Up for Razorpay**
   - Visit: https://razorpay.com/
   - Create an account

2. **Get API Keys**
   - Dashboard → Settings → API Keys
   - Generate Test Keys for development
   - Copy Key ID and Key Secret

3. **Update .env File**
   ```env
   RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
   RAZORPAY_KEY_SECRET=your_secret_key
   ```

---

## 📖 Usage

### For Users

#### Registration & Login
1. **Register New Account**
   - Click "Register" on the homepage
   - Fill in details (name, email, phone, password)
   - Verify email with OTP
   - Or use "Sign in with Google"

2. **Login**
   - Enter email and password
   - Or use Google OAuth

#### Browsing Books
1. **Physical Books**
   - Navigate to "Books" in navbar
   - Browse available physical books
   - Click on book for details

2. **E-Books**
   - Navigate to "E-Books"
   - Download in PDF, EPUB, or MOBI format

3. **Audiobooks**
   - Navigate to "Audiobooks"
   - Stream or download chapters

#### Borrowing Books
1. Click "Add to Bag" on any physical book
2. Go to "My Bag"
3. Review selected books
4. Click "Borrow All"
5. Books will appear in "My Loans"

#### Managing Subscriptions
1. Go to "Subscribe"
2. Choose a plan (Free, Basic, Premium, Ultimate)
3. Pay via Razorpay (for paid plans)
4. Enjoy increased borrowing limits

#### Using the Chatbot
1. Click the chat icon (bottom right)
2. Ask questions like:
   - "Recommend me a science fiction book"
   - "When is my book due?"
   - "What are the subscription plans?"
3. Get AI-powered responses

### For Administrators

#### Access Admin Panel
1. Login with admin credentials
2. Navigate to `/admin/dashboard`

#### Manage Books
- Add new books (physical, e-books, audiobooks)
- Edit book details
- Delete books
- Upload book covers

#### Manage Users
- View all registered users
- View user borrowing history
- Manage user subscriptions
- Handle fines and overdue books

#### Monitor Loans
- View all active loans
- Process book returns
- Calculate and manage fines

---

## 🗄️ Database Schema

### Tables

#### `user`
- User accounts and authentication
- Fields: id, name, email, password_hash, roll_no, phone, joined_at, is_active, is_verified

#### `physical_book`
- Physical book inventory
- Fields: id, title, author, isbn, publisher, publication_date, genre, total_copies, available_copies, description, cover_image_url

#### `ebook`
- Digital book collection
- Fields: id, title, author, isbn, publisher, publication_date, genre, file_size, description, cover_image_url, file_url

#### `ebook_format`
- Available e-book formats
- Fields: id, ebook_id, format_type (PDF/EPUB/MOBI), file_url, file_size

#### `audiobook`
- Audiobook catalog (LibriVox integration)
- Fields: id, title, author, narrator, language, genre, total_duration, description, cover_image_url, librivox_id

#### `audiobook_chapter`
- Audiobook chapter information
- Fields: id, audiobook_id, chapter_number, title, duration, audio_url

#### `loan`
- Book borrowing records
- Fields: id, user_id, book_id, borrowed_date, due_date, returned_date, status

#### `fine`
- Overdue fine tracking
- Fields: id, loan_id, amount, status, created_at, paid_at

#### `subscription`
- User subscription plans
- Fields: id, user_id, tier, start_date, end_date, is_active, auto_renew, price_paid

#### `otp`
- Email verification codes
- Fields: id, email, code, created_at, expires_at, is_used

---

## 🛠️ API Endpoints

### Authentication
```
POST   /register          - Register new user
POST   /auth/google       - Google OAuth login
POST   /login             - User login
GET    /logout            - User logout
POST   /verify-otp        - Verify email OTP
```

### Books
```
GET    /books             - List all physical books
GET    /book/<id>         - Get book details
POST   /book/<id>/borrow  - Add book to bag
```

### E-Books
```
GET    /ebooks            - List all e-books
GET    /ebook/<id>        - Get e-book details
GET    /ebook/<id>/download/<format> - Download e-book
```

### Audiobooks
```
GET    /audiobooks        - List all audiobooks
GET    /audiobook/<id>    - Get audiobook details
GET    /audiobook/<id>/chapter/<num>/stream - Stream chapter
```

### User
```
GET    /my-loans          - View user's loans
GET    /my-bag            - View borrowing cart
POST   /my-bag/remove/<id> - Remove from bag
POST   /borrow-all        - Borrow all books in bag
GET    /my-subscription   - View subscription status
```

### Subscriptions
```
GET    /subscribe         - View subscription plans
POST   /subscribe/<tier>  - Subscribe to plan
POST   /payment/verify    - Verify Razorpay payment
```

### Admin
```
GET    /admin/dashboard   - Admin dashboard
GET    /admin/books       - Manage books
POST   /admin/add-book    - Add new book
GET    /admin/students    - View all users
GET    /admin/loans       - View all loans
```

### Chatbot
```
POST   /chat              - Send message to AI chatbot
```

---

## 🏗️ Project Structure

```
LibraNet/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── forms.py                 # WTForms definitions
│   ├── models/                  # Database models
│   │   ├── user.py
│   │   ├── physical_book.py
│   │   ├── ebook.py
│   │   ├── audiobook.py
│   │   ├── loan.py
│   │   ├── fine.py
│   │   ├── subscription.py
│   │   └── otp.py
│   ├── routes/                  # Route blueprints
│   │   ├── auth_routes.py       # Authentication
│   │   ├── book_routes.py       # Book management
│   │   ├── ebook_routes.py      # E-book routes
│   │   ├── audiobook_routes.py  # Audiobook routes
│   │   ├── subscription_routes.py
│   │   ├── admin_routes.py
│   │   └── chat_routes.py       # AI chatbot
│   ├── services/
│   │   └── chatbot.py           # LangChain integration
│   ├── static/
│   │   ├── css/                 # Stylesheets
│   │   ├── js/                  # JavaScript files
│   │   └── images/              # Static images
│   └── templates/               # Jinja2 templates
│       ├── base.html
│       ├── landing_page.html
│       ├── register.html
│       ├── login.html
│       ├── books.html
│       ├── ebooks/
│       ├── audiobooks/
│       └── admin/
├── migrations/                  # Database migrations
├── config.py                    # Configuration
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
└── README.md                    # This file
```

---

## 🎨 Technologies Used

### Backend
- **Flask 3.1.2** - Web framework
- **SQLAlchemy 2.0** - ORM
- **Flask-Login** - User session management
- **Flask-WTF** - Form handling and validation
- **Flask-Mail** - Email sending
- **Flask-Migrate** - Database migrations
- **PyMySQL** - MySQL connector

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with custom variables
- **JavaScript (Vanilla)** - Interactivity
- **Responsive Design** - Mobile-first approach

### Authentication
- **Werkzeug** - Password hashing
- **Google OAuth 2.0** - Social login
- **OTP System** - Email verification

### Payment
- **Razorpay** - Payment gateway integration

### AI & APIs
- **LangChain** - AI orchestration
- **Google Gemini** - Language model
- **LibriVox API** - Free audiobooks
- **Open Library API** - Book metadata

### Database
- **MySQL 5.7+** - Relational database
- **Alembic** - Schema migrations

---

## 🔒 Security Features

- **Password Hashing** - Werkzeug SHA-256
- **CSRF Protection** - Flask-WTF tokens
- **SQL Injection Prevention** - SQLAlchemy ORM
- **XSS Protection** - Jinja2 auto-escaping
- **Session Security** - Secure cookie flags
- **Email Verification** - OTP-based confirmation
- **Environment Variables** - Sensitive data protection

---

## 📱 Responsive Design

LibraNet is fully responsive and works seamlessly across:
- 📱 **Mobile** - iOS and Android (320px+)
- 📱 **Tablet** - iPad and Android tablets (768px+)
- 💻 **Desktop** - Laptops and desktops (1024px+)
- 🖥️ **Large Screens** - 4K displays (1920px+)

---

## 🌙 Dark Mode

LibraNet features a beautiful dark mode:
- Toggle button in navbar
- Persists across sessions (localStorage)
- Smooth transitions
- Eye-friendly color palette

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Repository**
   ```bash
   git fork https://github.com/vans-aj/LibraNet.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Commit Changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

4. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

5. **Open Pull Request**
   - Describe your changes
   - Reference any issues
   - Add screenshots if UI changes

### Development Guidelines
- Follow PEP 8 style guide
- Write meaningful commit messages
- Add comments for complex logic
- Test thoroughly before submitting
- Update documentation as needed

---

## 🐛 Bug Reports

Found a bug? Please open an issue with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, browser)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Vansh Ajrawat** - *Lead Developer* - [@vans-aj](https://github.com/vans-aj)

---

## 🙏 Acknowledgments

- **Graphic Era Hill University** - For supporting this project
- **LibriVox** - Free audiobook catalog
- **Open Library** - Book metadata API
- **Google** - OAuth and Gemini AI
- **Flask Community** - Excellent documentation
- **Contributors** - All who have contributed to this project

---

## 📞 Support

Need help? Reach out:
- 📧 Email: vnshajrawat951@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/vans-aj/LibraNet/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/vans-aj/LibraNet/discussions)

---

## 🗺️ Roadmap

### Upcoming Features
- [ ] Mobile app (React Native)
- [ ] Book recommendations based on ML
- [ ] Social features (reviews, ratings)
- [ ] Book clubs and reading lists
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Barcode scanning
- [ ] Integration with Goodreads
- [ ] Progressive Web App (PWA)
- [ ] Export data functionality

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/vans-aj/LibraNet?style=social)
![GitHub forks](https://img.shields.io/github/forks/vans-aj/LibraNet?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/vans-aj/LibraNet?style=social)

---

<div align="center">

**Made with ❤️ by Vansh Ajrawat**

⭐ **Star this repo if you find it helpful!** ⭐

</div>
