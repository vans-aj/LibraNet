# 📚 LibraNet - Modern Digital Library Management System# 📚 LibraNet - Modern Library Management System



<div align="center"><div align="center">



**A comprehensive library management platform with AI-powered features, multi-format book support, and intelligent reading assistance**![LibraNet Logo](app/static/images/logo.svg)



[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)**A comprehensive, modern library management system built with Flask**

[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)

[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Configuration](#-configuration) • [Tech Stack](#-tech-stack)[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)



</div>[Features](#features) • [Installation](#installation) • [Configuration](#configuration) • [Usage](#usage) • [API](#api) • [Contributing](#contributing)



---</div>



## ✨ Features---



### 📚 Multi-Format Library System## 🌟 Features

- **Physical Books** - Traditional book lending with inventory management

- **E-Books** - Digital library with PDF, EPUB, and MOBI format support### 📖 Multi-Format Library

- **Audiobooks** - Integrated with LibriVox API for free public domain audiobooks- **Physical Books** - Traditional book lending and management

- **Smart Cataloging** - Automated metadata enrichment via Open Library API- **E-Books** - Digital book collection with format support (PDF, EPUB, MOBI)

- **Audiobooks** - Integrated with LibriVox API for free audiobooks

### 🤖 AI-Powered Reading Assistant- **Smart Search** - Powered by Open Library API for comprehensive book data

- **Intelligent Chatbot** - Context-aware library assistance powered by LangChain + Google Gemini

- **AI Dictionary** - Real-time word and sentence meaning lookup while reading### 👥 User Management

- **Book Recommendations** - Personalized suggestions based on reading history- **Flexible Registration** - Email/password or Google OAuth sign-in

- **Natural Language Queries** - Ask questions in plain English- **Email Verification** - OTP-based email verification system

- **User Profiles** - Customizable user profiles with borrowing history

### 👥 User Management & Authentication- **Role-Based Access** - Admin and user role separation

- **Multiple Sign-in Options** - Email/password or Google OAuth 2.0

- **Email Verification** - OTP-based email verification system### 🔐 Authentication & Security

- **Role-Based Access Control** - Admin and user privilege separation- **Google OAuth 2.0** - One-click sign-in with Google

- **Profile Management** - Track reading history and preferences- **Secure Passwords** - Hashed password storage with Werkzeug

- **OTP Verification** - Time-limited email verification codes

### 💳 Subscription & Payment System- **Session Management** - Flask-Login for secure session handling

- **Tiered Plans** - Free, Basic, Premium, and Ultimate membership levels

- **Secure Payments** - Razorpay payment gateway integration### 💳 Subscription System

- **Borrowing Limits** - Subscription-based access control- **Tiered Plans** - Free, Basic, Premium, and Ultimate tiers

- **Auto-renewal** - Automated subscription management- **Payment Integration** - Razorpay payment gateway

- **Auto-renewal** - Automatic subscription renewal

### 📖 Advanced Reading Experience- **Borrowing Limits** - Tier-based borrowing restrictions

- **Split-Screen E-Reader** - Book content on left, AI assistant on right

- **Text Selection** - Select words/phrases for instant definitions### 📊 Loan Management

- **Dark/Light Mode** - Comfortable reading in any environment- **Smart Tracking** - Comprehensive loan history and status

- **Pagination Controls** - Smooth navigation through books- **Due Date System** - 6-month default loan period

- **Responsive Design** - Seamless experience across all devices- **Fine Calculation** - Automated overdue fine calculation

- **Return Processing** - Easy book return workflow

### 📊 Library Operations

- **Loan Management** - Track borrowing, due dates, and returns### 🤖 AI-Powered Chatbot

- **Fine Calculation** - Automated overdue fine system- **Book Recommendations** - AI-powered book suggestions

- **Inventory Tracking** - Real-time availability status- **Natural Language** - Chat with LibraNet for help

- **Search & Filter** - Multi-criteria search by title, author, ISBN, genre- **Context-Aware** - Understands library-specific queries

- **Powered by** - LangChain + Google Gemini

---

### 🎨 Modern UI/UX

## 🚀 Quick Start- **Responsive Design** - Works on desktop, tablet, and mobile

- **Dark Mode** - Toggle between light and dark themes

```bash- **Animated UI** - Smooth transitions and animations

# Clone the repository- **Accessible** - WCAG compliant design

git clone https://github.com/vans-aj/LibraNet.git

cd LibraNet### 🔍 Advanced Search

- **Multi-Criteria** - Search by title, author, ISBN, genre

# Create and activate virtual environment- **Real-time Results** - Instant search suggestions

python -m venv venv- **Filter Options** - Filter by format, availability, rating

source venv/bin/activate  # On Windows: venv\Scripts\activate- **API Integration** - Open Library API for enhanced metadata



# Install dependencies---

pip install -r requirements.txt

## 🚀 Installation

# Set up environment variables (see Configuration section)

cp .env.example .env  # Edit with your credentials### Prerequisites

- Python 3.8 or higher

# Initialize database- MySQL 5.7 or higher

flask db upgrade- pip (Python package manager)

- Git

# Run the application

python main.py### Step 1: Clone the Repository

``````bash

git clone https://github.com/vans-aj/LibraNet.git

Visit `http://127.0.0.1:8080` in your browser.cd LibraNet

```

---

### Step 2: Create Virtual Environment

## 📋 Installation```bash

# Create virtual environment

### Prerequisitespython -m venv venv

- Python 3.8 or higher

- MySQL 5.7+ or PostgreSQL 12+# Activate virtual environment

- pip (Python package manager)# On macOS/Linux:

- Gitsource venv/bin/activate



### Detailed Setup# On Windows:

venv\Scripts\activate

#### 1. Database Setup```



**MySQL:**### Step 3: Install Dependencies

```sql```bash

CREATE DATABASE libranet CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;pip install -r requirements.txt

CREATE USER 'libranet_user'@'localhost' IDENTIFIED BY 'your_secure_password';```

GRANT ALL PRIVILEGES ON libranet.* TO 'libranet_user'@'localhost';

FLUSH PRIVILEGES;### Step 4: Set Up MySQL Database

``````bash

# Log into MySQL

**PostgreSQL:**mysql -u root -p

```sql

CREATE DATABASE libranet;# Create database

CREATE USER libranet_user WITH PASSWORD 'your_secure_password';CREATE DATABASE libranet;

GRANT ALL PRIVILEGES ON DATABASE libranet TO libranet_user;

```# Create user (optional)

CREATE USER 'teamx'@'localhost' IDENTIFIED BY 'strongpass1234';

#### 2. Environment ConfigurationGRANT ALL PRIVILEGES ON libranet.* TO 'teamx'@'localhost';

FLUSH PRIVILEGES;

Create a `.env` file in the project root:EXIT;

```

```env

# Flask Configuration### Step 5: Configure Environment Variables

SECRET_KEY=your-super-secret-key-hereCreate a `.env` file in the project root:

FLASK_ENV=development

```env

# Database Configuration# Database Configuration

SQLALCHEMY_DATABASE_URI=mysql+pymysql://libranet_user:your_secure_password@localhost/libranetSQLALCHEMY_DATABASE_URI=mysql+pymysql://teamx:strongpass1234@localhost/libranet

# Or for PostgreSQL:SQLALCHEMY_TRACK_MODIFICATIONS=False

# SQLALCHEMY_DATABASE_URI=postgresql://libranet_user:your_secure_password@localhost/libranet

# Flask Secret Key (generate a random string)

# Email Configuration (Gmail)SECRET_KEY=your-super-secret-key-here

MAIL_SERVER=smtp.gmail.com

MAIL_PORT=587# Email Configuration (Gmail)

MAIL_USE_TLS=TrueMAIL_USERNAME=your-email@gmail.com

MAIL_USERNAME=your-email@gmail.comMAIL_PASSWORD=your-app-specific-password

MAIL_PASSWORD=your-gmail-app-password

MAIL_DEFAULT_SENDER=your-email@gmail.com# Google OAuth (Get from Google Cloud Console)

GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com

# Google OAuth 2.0GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret

GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.comOAUTHLIB_INSECURE_TRANSPORT=1  # Only for development

GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret

OAUTHLIB_INSECURE_TRANSPORT=1  # Development only# Razorpay Payment Gateway (Get from Razorpay Dashboard)

RAZORPAY_KEY_ID=your-razorpay-key-id

# Payment Gateway (Razorpay)RAZORPAY_KEY_SECRET=your-razorpay-key-secret

RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx

RAZORPAY_KEY_SECRET=your-razorpay-secret# AI Chatbot (Google Gemini API)

GOOGLE_API_KEY=your-google-gemini-api-key

# AI Configuration (Google Gemini + LangChain)LANGCHAIN_API_KEY=your-langchain-api-key

GOOGLE_API_KEY=your-google-gemini-api-keyLANGCHAIN_PROJECT=LibraNet

LANGCHAIN_API_KEY=your-langchain-api-key

LANGCHAIN_PROJECT=LibraNet# External APIs

LANGCHAIN_TRACING_V2=trueLIBRIVOX_API_URL=https://librivox.org/api/feed/audiobooks

OPEN_LIBRARY_SEARCH_URL=https://openlibrary.org/search.json

# External APIsOPEN_LIBRARY_COVER_URL=https://covers.openlibrary.org/b/id/

LIBRIVOX_API_URL=https://librivox.org/api/feed/audiobooks```

OPEN_LIBRARY_SEARCH_URL=https://openlibrary.org/search.json

OPEN_LIBRARY_COVER_URL=https://covers.openlibrary.org/b/id/### Step 6: Initialize Database

``````bash

# Initialize Flask-Migrate

#### 3. Database Migrationflask db init



```bash# Create migration

# Initialize migration repository (first time only)flask db migrate -m "Initial database setup"

flask db init

# Apply migration

# Create initial migrationflask db upgrade

flask db migrate -m "Initial database setup"```



# Apply migrations### Step 7: Seed Sample Data (Optional)

flask db upgrade```bash

```# Seed physical books

python seed_physical_books.py

#### 4. Seed Sample Data (Optional)

# Seed e-books

```bashpython seed_ebooks.py

# Seed physical books

python seed_physical_books.py# Seed audiobooks (from LibriVox)

python seed_db.py

# Seed e-books from Project Gutenberg```

python seed_ebooks.py

```### Step 8: Run the Application

```bash

---python main.py

```

## ⚙️ Configuration

The application will be available at `http://127.0.0.1:8080`

### Google OAuth 2.0 Setup

---

1. **Create Project** at [Google Cloud Console](https://console.cloud.google.com/)

2. **Enable Google+ API** under "APIs & Services"## ⚙️ Configuration

3. **Create OAuth 2.0 Credentials**

   - Application type: Web application### Google OAuth Setup

   - Authorized origins: `http://127.0.0.1:8080`, `http://localhost:8080`

   - Redirect URIs: `http://127.0.0.1:8080/auth/google`1. **Go to Google Cloud Console**

4. **Copy credentials** to `.env` file   - Visit: https://console.cloud.google.com/



### Gmail App Password2. **Create a New Project**

   - Click "Select a project" → "New Project"

1. Enable 2-Factor Authentication in Google Account   - Name: LibraNet (or your choice)

2. Generate App Password: Account → Security → App passwords

3. Select "Mail" and "Other (Custom name)"3. **Enable Google+ API**

4. Copy 16-character password to `MAIL_PASSWORD` in `.env`   - Navigate to "APIs & Services" → "Library"

   - Search for "Google+ API" and enable it

### Razorpay Payment Gateway

4. **Create OAuth Credentials**

1. Sign up at [Razorpay](https://razorpay.com/)   - Go to "APIs & Services" → "Credentials"

2. Navigate to Dashboard → Settings → API Keys   - Click "Create Credentials" → "OAuth 2.0 Client ID"

3. Generate Test/Live keys   - Application type: Web application

4. Add `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` to `.env`   - Name: LibraNet Web Client



### Google Gemini API5. **Configure Authorized Origins**

   Add these URLs:

1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)   ```

2. Add `GOOGLE_API_KEY` to `.env`   http://127.0.0.1:8080

   http://localhost:8080

### LangChain Configuration   ```



1. Sign up at [LangSmith](https://smith.langchain.com/)6. **Configure Redirect URIs**

2. Create new project   Add these URLs:

3. Generate API key   ```

4. Add `LANGCHAIN_API_KEY` and `LANGCHAIN_PROJECT` to `.env`   http://127.0.0.1:8080/auth/google

   http://localhost:8080/auth/google

---   ```



## 🛠️ Tech Stack7. **Copy Credentials**

   - Copy the Client ID and Client Secret

### Backend   - Add them to your `.env` file

- **Framework:** Flask 3.1.2

- **Database ORM:** SQLAlchemy 2.0.43For detailed instructions, see [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md)

- **Migrations:** Alembic 1.16.5 (Flask-Migrate 4.1.0)

- **Authentication:** Flask-Login 0.6.3### Email Configuration (Gmail)

- **Forms:** Flask-WTF 1.2.2, WTForms 3.2.1

- **Email:** Flask-Mail 0.10.01. **Enable 2-Factor Authentication**

   - Go to Google Account Settings

### Database   - Security → 2-Step Verification

- **Primary:** MySQL (via PyMySQL 1.1.2)

- **Alternative:** PostgreSQL (via psycopg2-binary 2.9.10)2. **Generate App Password**

   - Security → App passwords

### AI & Machine Learning   - Select app: Mail

- **LLM Framework:** LangChain   - Select device: Other (Custom name)

- **Model:** Google Gemini (via google-generativeai)   - Name: LibraNet

- **Monitoring:** LangSmith   - Copy the 16-character password

- **Alternative:** Groq (langchain-groq)

3. **Update .env File**

### Payment & OAuth   ```env

- **Payment Gateway:** Razorpay 1.4.2   MAIL_USERNAME=your-email@gmail.com

- **OAuth:** Google Auth 2.36.0, google-auth-oauthlib 1.2.1   MAIL_PASSWORD=your-16-char-app-password

   ```

### Frontend

- **Template Engine:** Jinja2 3.1.6### Razorpay Payment Setup

- **Styling:** Custom CSS with CSS Variables

- **JavaScript:** Vanilla JS (ES6+)1. **Sign Up for Razorpay**

- **Responsive Design:** Mobile-first approach   - Visit: https://razorpay.com/

   - Create an account

### Deployment

- **WSGI Server:** Gunicorn 23.0.02. **Get API Keys**

- **Image Processing:** Pillow 11.0.0   - Dashboard → Settings → API Keys

- **Environment:** python-dotenv 1.1.1   - Generate Test Keys for development

   - Copy Key ID and Key Secret

### External APIs

- **Book Metadata:** Open Library API3. **Update .env File**

- **Audiobooks:** LibriVox API   ```env

- **E-books:** Project Gutenberg   RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx

   RAZORPAY_KEY_SECRET=your_secret_key

---   ```



## 📁 Project Structure---



```## 📖 Usage

LibraNet/

│### For Users

├── app/

│   ├── __init__.py           # Flask app factory#### Registration & Login

│   ├── forms.py              # WTForms definitions1. **Register New Account**

│   ├── models/               # SQLAlchemy models   - Click "Register" on the homepage

│   │   ├── user.py   - Fill in details (name, email, phone, password)

│   │   ├── physical_book.py   - Verify email with OTP

│   │   ├── ebook.py   - Or use "Sign in with Google"

│   │   ├── audiobook.py

│   │   ├── loan.py2. **Login**

│   │   ├── subscription.py   - Enter email and password

│   │   └── ...   - Or use Google OAuth

│   ├── routes/               # Blueprint routes

│   │   ├── auth_routes.py#### Browsing Books

│   │   ├── book_routes.py1. **Physical Books**

│   │   ├── ebook_routes.py   - Navigate to "Books" in navbar

│   │   ├── audiobook_routes.py   - Browse available physical books

│   │   ├── subscription_routes.py   - Click on book for details

│   │   ├── chat_routes.py

│   │   └── admin_routes.py2. **E-Books**

│   ├── services/             # Business logic   - Navigate to "E-Books"

│   │   └── chatbot.py        # AI chatbot service   - Download in PDF, EPUB, or MOBI format

│   ├── utils/                # Utility functions

│   │   └── file_upload.py3. **Audiobooks**

│   ├── static/               # Static assets   - Navigate to "Audiobooks"

│   │   ├── css/   - Stream or download chapters

│   │   ├── js/

│   │   ├── images/#### Borrowing Books

│   │   └── uploads/1. Click "Add to Bag" on any physical book

│   └── templates/            # Jinja2 templates2. Go to "My Bag"

│       ├── base.html3. Review selected books

│       ├── books.html4. Click "Borrow All"

│       ├── ebooks/5. Books will appear in "My Loans"

│       │   ├── ebooks.html

│       │   └── reader.html   # AI-powered e-reader#### Managing Subscriptions

│       └── ...1. Go to "Subscribe"

│2. Choose a plan (Free, Basic, Premium, Ultimate)

├── migrations/               # Alembic migrations3. Pay via Razorpay (for paid plans)

├── config.py                 # Configuration settings4. Enjoy increased borrowing limits

├── db.py                     # Database initialization

├── main.py                   # Application entry point#### Using the Chatbot

├── requirements.txt          # Python dependencies1. Click the chat icon (bottom right)

├── .env                      # Environment variables (not in git)2. Ask questions like:

└── README.md                 # This file   - "Recommend me a science fiction book"

```   - "When is my book due?"

   - "What are the subscription plans?"

---3. Get AI-powered responses



## 🎯 Usage### For Administrators



### User Workflows#### Access Admin Panel

1. Login with admin credentials

#### Registration & Login2. Navigate to `/admin/dashboard`

1. Visit homepage and click "Register"

2. Fill in details or use "Sign in with Google"#### Manage Books

3. Verify email with OTP code- Add new books (physical, e-books, audiobooks)

4. Access personalized dashboard- Edit book details

- Delete books

#### Browsing & Reading- Upload book covers

1. **Physical Books:** Browse catalog, add to bag, borrow

2. **E-Books:** Access digital library, read with AI assistant#### Manage Users

3. **Audiobooks:** Stream or download chapters- View all registered users

- View user borrowing history

#### AI Reading Assistant- Manage user subscriptions

1. Open any e-book in the reader- Handle fines and overdue books

2. Select text to see AI dictionary sidebar

3. Click "Get Meaning" for instant definitions#### Monitor Loans

4. Use floating chatbot for general queries- View all active loans

- Process book returns

#### Subscriptions- Calculate and manage fines

1. Navigate to "Subscribe" page

2. Choose plan (Free/Basic/Premium/Ultimate)---

3. Complete payment via Razorpay

4. Enjoy increased borrowing limits## 🗄️ Database Schema



### Admin Features### Tables

- Add/edit/delete books, e-books, audiobooks

- Manage user accounts and subscriptions#### `user`

- Track loans and process returns- User accounts and authentication

- Calculate and collect fines- Fields: id, name, email, password_hash, roll_no, phone, joined_at, is_active, is_verified

- View system analytics

#### `physical_book`

---- Physical book inventory

- Fields: id, title, author, isbn, publisher, publication_date, genre, total_copies, available_copies, description, cover_image_url

## 🔒 Security

#### `ebook`

- **Password Hashing:** Werkzeug PBKDF2 SHA-256- Digital book collection

- **CSRF Protection:** Flask-WTF tokens- Fields: id, title, author, isbn, publisher, publication_date, genre, file_size, description, cover_image_url, file_url

- **SQL Injection:** SQLAlchemy ORM parameterization

- **XSS Prevention:** Jinja2 auto-escaping#### `ebook_format`

- **Session Security:** Secure cookies with SECRET_KEY- Available e-book formats

- **OAuth 2.0:** Industry-standard authentication- Fields: id, ebook_id, format_type (PDF/EPUB/MOBI), file_url, file_size



---#### `audiobook`

- Audiobook catalog (LibriVox integration)

## 🚢 Deployment- Fields: id, title, author, narrator, language, genre, total_duration, description, cover_image_url, librivox_id



### Production Checklist#### `audiobook_chapter`

- Audiobook chapter information

```env- Fields: id, audiobook_id, chapter_number, title, duration, audio_url

# Update .env for production

FLASK_ENV=production#### `loan`

OAUTHLIB_INSECURE_TRANSPORT=0- Book borrowing records

SECRET_KEY=<generate-strong-random-key>- Fields: id, user_id, book_id, borrowed_date, due_date, returned_date, status

```

#### `fine`

### Deploy with Gunicorn- Overdue fine tracking

- Fields: id, loan_id, amount, status, created_at, paid_at

```bash

gunicorn -w 4 -b 0.0.0.0:8080 main:app#### `subscription`

```- User subscription plans

- Fields: id, user_id, tier, start_date, end_date, is_active, auto_renew, price_paid

### Environment Variables

Ensure all required environment variables are set:#### `otp`

- Database credentials- Email verification codes

- OAuth client ID/secret- Fields: id, email, code, created_at, expires_at, is_used

- API keys (Gemini, LangChain, Razorpay)

- Email configuration---



---## 🛠️ API Endpoints



## 🤝 Contributing### Authentication

```

Contributions are welcome! Please follow these steps:POST   /register          - Register new user

POST   /auth/google       - Google OAuth login

1. Fork the repositoryPOST   /login             - User login

2. Create a feature branch (`git checkout -b feature/AmazingFeature`)GET    /logout            - User logout

3. Commit changes (`git commit -m 'Add AmazingFeature'`)POST   /verify-otp        - Verify email OTP

4. Push to branch (`git push origin feature/AmazingFeature`)```

5. Open a Pull Request

### Books

---```

GET    /books             - List all physical books

## 📄 LicenseGET    /book/<id>         - Get book details

POST   /book/<id>/borrow  - Add book to bag

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.```



---### E-Books

```

## 👨‍💻 AuthorGET    /ebooks            - List all e-books

GET    /ebook/<id>        - Get e-book details

**Vansaj Rawat**GET    /ebook/<id>/download/<format> - Download e-book

- GitHub: [@vans-aj](https://github.com/vans-aj)```



---### Audiobooks

```

## 🙏 AcknowledgmentsGET    /audiobooks        - List all audiobooks

GET    /audiobook/<id>    - Get audiobook details

- [Project Gutenberg](https://www.gutenberg.org/) - Free e-booksGET    /audiobook/<id>/chapter/<num>/stream - Stream chapter

- [LibriVox](https://librivox.org/) - Free public domain audiobooks```

- [Open Library](https://openlibrary.org/) - Book metadata API

- [Google Gemini](https://deepmind.google/technologies/gemini/) - AI model### User

- [LangChain](https://www.langchain.com/) - LLM framework```

- [Flask](https://flask.palletsprojects.com/) - Web frameworkGET    /my-loans          - View user's loans

GET    /my-bag            - View borrowing cart

---POST   /my-bag/remove/<id> - Remove from bag

POST   /borrow-all        - Borrow all books in bag

## 📞 SupportGET    /my-subscription   - View subscription status

```

For issues, questions, or suggestions:

- Open an [Issue](https://github.com/vans-aj/LibraNet/issues)### Subscriptions

- Contact: vansajrawat@example.com```

GET    /subscribe         - View subscription plans

---POST   /subscribe/<tier>  - Subscribe to plan

POST   /payment/verify    - Verify Razorpay payment

<div align="center">```



Made with ❤️ by Vansaj Rawat### Admin

```

**LibraNet** - Bringing libraries into the AI eraGET    /admin/dashboard   - Admin dashboard

GET    /admin/books       - Manage books

</div>POST   /admin/add-book    - Add new book

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
