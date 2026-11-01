# 📚 NexShelf — Next-Gen Smart Library Management System & Scholar Suite

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.0-lightgrey?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%2F%20PostgreSQL-blue?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![UI Style](https://img.shields.io/badge/UI-Bootstrap%205%20%2B%20Glassmorphism-purple?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Deployment](https://img.shields.io/badge/Deployment-Render%20Ready-success?logo=render&logoColor=white)](https://render.com)

**NexShelf** is an all-in-one smart campus library management platform and scholar community suite. It merges traditional institutional catalog management with peer-to-peer textbook exchange, courseware revision sharing, and gamification.

---

## 📁 Project Architecture & Folder Structure

The project follows a clean **3-Tier MVC (Model-View-Controller) / Service-Layer Architecture** designed for maintainability and scalability:

```text
library/
│
├── 📄 run.py                  # Application Entrypoint (starts WSGI development server)
├── 📄 config.py               # Central Configuration (detects SQLite vs. Cloud PostgreSQL)
├── 📄 requirements.txt        # Production & development dependencies (Flask, SQLAlchemy, Gunicorn)
├── 📄 Procfile                # Cloud runtime command for Render / Heroku (Gunicorn runner)
├── 📄 render.yaml             # Render Blueprint automation (1-click deployment)
├── 📄 seed_demo_data.py       # Initial database provisioner (users, catalog, notes, marketplace)
├── 📄 seed_200_books.py       # Catalog generator for 200+ academic volumes
├── 📄 .gitignore              # Files excluded from git tracking (venv, cache, environment secrets)
│
├── 📂 app/                    # Main Application Package
│   │
│   ├── 📄 __init__.py         # Flask App Factory (Registers blueprints, initializes DB & JWT)
│   │
│   ├── 📂 models/             # 🗄️ Database Entity Models (SQLAlchemy ORM)
│   │   ├── __init__.py        # Exports all database models
│   │   ├── user.py            # User authentication, hashed passwords, roles (admin/student)
│   │   ├── member.py          # Student library membership profile & borrow limits
│   │   ├── book.py            # Physical catalog volumes, shelf coordinates, ISBNs
│   │   ├── author.py          # Book authors catalog
│   │   ├── category.py        # Subject categories (AI, Algorithms, Systems, Math)
│   │   ├── issue_record.py    # Circulation ledger (borrow, return, due dates)
│   │   ├── fine.py            # Late return penalty ledger & payment status
│   │   ├── request.py         # Book acquisition requests & student wishlists
│   │   ├── review.py          # Book ratings and verified reader reviews
│   │   ├── study_note.py      # Student-uploaded courseware & formula sheets
│   │   ├── gamification.py    # Reading milestones, badges, and scholar points
│   │   ├── notification.py    # Due date alerts & circulation notices
│   │   └── base.py            # Base SQLAlchemy model declarations
│   │
│   ├── 📂 routes/             # 🌐 Web Controllers & RESTful API Endpoints (Blueprints)
│   │   ├── __init__.py        # Exports all route blueprints
│   │   ├── ui_routes.py       # Front-end view routers (/, /login, /student, /admin, /contact)
│   │   ├── auth_routes.py     # Authentication APIs (/api/auth/login, /api/auth/register, /api/auth/me)
│   │   ├── book_routes.py     # Catalog CRUD & search APIs (/api/books)
│   │   ├── student_routes.py  # Student circulation actions (borrow, return, active loans)
│   │   ├── community_routes.py# P2P marketplace, study notes, book swaps (/api/offers, /api/notes)
│   │   ├── dashboard_routes.py# Admin executive analytics & circulation KPI stats
│   │   ├── shelf_routes.py    # Virtual 3D bookshelf coordinates & shelf locator
│   │   ├── scanner_routes.py  # Barcode / QR checkout scanner endpoints
│   │   ├── fine_routes.py     # Fines calculation & settlement
│   │   ├── gamification_routes.py # Reading streak & badge unlocks
│   │   ├── library_routes.py  # General circulation & transaction logging
│   │   ├── member_routes.py   # Student member management for librarians
│   │   ├── citation_routes.py # APA, MLA, IEEE citation generators
│   │   ├── ai_routes.py       # AI reading assistant & semantic search
│   │   └── analytics_routes.py# Circulations charts & departmental usage trends
│   │
│   ├── 📂 services/           # ⚙️ Business Logic Layer (Separates logic from routes)
│   │   ├── auth_service.py    # Password verification, token issuance, role security
│   │   ├── book_service.py    # Catalog queries, copy allocation, inventory checks
│   │   ├── issue_service.py   # Borrowing constraints, renewals, return workflows
│   │   ├── book_offer_service.py # P2P marketplace listing validation
│   │   ├── study_note_service.py # Courseware upload validation & moderation
│   │   ├── dashboard_service.py  # Aggregated metrics for librarians
│   │   ├── shelf_service.py   # Physical shelf aisle/rack mapping
│   │   ├── fine_service.py    # Overdue fine calculations
│   │   ├── gamification_service.py # Badge triggers & reading score calculations
│   │   ├── contact_service.py # Help desk inquiries handling
│   │   ├── request_service.py # Book procurement request processing
│   │   ├── review_service.py  # Star ratings & reader feedback
│   │   ├── member_service.py  # Student membership provisioning
│   │   ├── notification_service.py # Automated reminder generation
│   │   ├── citation_service.py# Formatted bibliography generator
│   │   ├── ai_service.py      # Natural language catalog search
│   │   └── analytics_service.py# Chart datasets preparation
│   │
│   ├── 📂 templates/          # 🎨 Front-End HTML5 / Jinja2 Templates
│   │   ├── 📂 auth/           # Login & Registration Pages
│   │   │   ├── login.html     # Glassmorphic user login portal
│   │   │   └── register.html  # Student digital membership registration
│   │   │
│   │   ├── 📂 student/        # Student Experience Portal
│   │   │   └── dashboard.html # Scholar Concierge, 3D Virtual Spine Shelf,
│   │   │                      # P2P Marketplace, Courseware Vault, Swaps Desk
│   │   │
│   │   ├── 📂 admin/          # Librarian Management Console
│   │   │   └── dashboard.html # Executive Dashboard, Circulation Desk,
│   │   │                      # Inventory Master, Analytics & Fines Ledger
│   │   │
│   │   └── 📂 public/         # Public Information Pages
│   │       └── contact.html   # Campus library help desk & inquiries
│   │
│   ├── 📂 static/             # 📦 Static Assets & File Storage
│   │   └── 📂 uploads/        # User-uploaded textbook photos and notes previews
│   │
│   └── 📂 utils/              # 🛡️ Helpers & Security Decorators
│       └── decorators.py      # `@admin_required` and `@student_required` JWT gates
│
├── 📂 instance/               # 💾 Local Persistent Database
│   └── library_management.db  # SQLite database file (created automatically on startup)
│
└── 📂 tests/                  # 🧪 Unit & Integration Test Suites
    └── test_unique_features.py # Automated test cases for core library functions
```

---

## 🚀 Quick Start Guide (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/iamgovindsiingh-ai/libray.git
cd libray
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Seed the Database (Initial Records & Demo Catalog)
```bash
python seed_demo_data.py
```
*(Optional: Run `python seed_200_books.py` to populate 200+ academic volumes)*

### 5. Start the Application
```bash
python run.py
```
Open your browser and navigate to: **[http://localhost:5000](http://localhost:5000)**

---

## 🔑 Default Login Credentials

| Role | Email Address | Password | Accessible Portal |
| :--- | :--- | :--- | :--- |
| **Full Administrator** | `admin@nexshelf.edu` | `admin123` | **[http://localhost:5000/admin](http://localhost:5000/admin)** |
| **Personal Admin** | `govind@gmail.com` | *(your password)* | **[http://localhost:5000/admin](http://localhost:5000/admin)** |
| **Scholar / Student** | `student@nexshelf.edu` | `student123` | **[http://localhost:5000/student](http://localhost:5000/student)** |

---

## 🌟 Core Modules & Capabilities

### 1. 🏛️ Scholar Action Hub & Concierge
- **Unified Portal Grid**: Fast one-click shortcuts to Borrowing, Selling, Notes Upload, Philanthropy, and Acquisition Wishlists.
- **3D Virtual Bookshelf Spine Rack**: Interactive perspective bookshelf showing realistic book spines with embossed titles that pull out on hover.

### 2. 🛒 Peer-to-Peer Textbook Marketplace
- **Student-to-Student Commerce**: List coursework textbooks for sale directly to campus peers with transparent pricing in ₹ and specimen condition photographs.
- **Direct Handover**: Direct WhatsApp and phone contact channels for on-campus exchange.

### 3. 📝 Scholar Courseware & Examination Vault
- **Classmate Notes**: Upload and access subject-indexed handwritten revision sheets, formula dossiers, and solved past exam papers.
- **Interactive Community**: Preview document pages and upvote helpful courseware.

### 4. 🤝 Textbook Philanthropy & Swaps
- **Free Book Grants**: Endow completed course textbooks to incoming junior scholars.
- **Semester Swaps**: Facilitate trade-for-trade exchanges for identical semester syllabus courses.

### 5. 🛡️ Executive Admin Command Console
- **Live Circulation Odometers**: Real-time KPI reels tracking catalog totals, active loans, overdue items, and collected penalties.
- **Master Drawer**: Manage books, student members, issue records, acquisition requests, and visitor inquiries from a centralized interface.
- **Barcode & QR Integration**: Built-in camera scanner for fast circulation desk checkouts.

---

## ☁️ Deployment on Render (render.com)

NexShelf is pre-configured for deployment on Render:

1. Push your repository to GitHub.
2. Log in to [render.com](https://render.com) and click **New +** &rarr; **Blueprint**.
3. Select your repository `libray`.
4. Render will detect `render.yaml`, configure the environment with Python 3.12, install dependencies, and launch Gunicorn automatically via:
   ```bash
   gunicorn --bind 0.0.0.0:$PORT run:app
   ```
5. *(Optional)* Connect a free **Render PostgreSQL** database by creating one in your dashboard and adding `DATABASE_URL` to your Web Service environment.

---

## 🛡️ Security & Role-Based Access Control
- **JWT Authentication**: Secured with `flask_jwt_extended` using HTTP Bearer tokens.
- **Decorators**: Routes are gated using `@admin_required()` and `@student_required()`.
- **Public Registration Protection**: Public self-registration only creates `student` accounts to prevent unauthorized administrative escalation.

---

## 📄 License
This project is licensed under the MIT License — free for academic and institutional use.
