# NexShelf · Backend API Server

This directory contains the Python Flask REST API server powering the **NexShelf** smart library management system.

---

## 📁 Directory Structure

```
backend/
├── app/
│   ├── models/            # SQLAlchemy Database Entities (Book, User, Member, Issue, Fine, etc.)
│   ├── routes/            # Blueprint API Endpoints (Auth, Student, Books, Dashboard, Community, etc.)
│   ├── services/          # Business Logic Layer (IssueService, AuthService, DashboardService, etc.)
│   ├── utils/             # Decorators, JWT validation, and helpers
│   ├── static/            # Static assets and uploads
│   └── templates/         # Legacy UI templates (kept for backward compatibility)
├── tests/                 # Unit & integration test suites
├── config.py              # Environment configuration & database URI resolution
├── run.py                 # Development WSGI entry point
├── requirements.txt       # Python package dependencies
└── .flaskenv              # Flask environment settings
```

---

## 🚀 How to Run the Backend

From the repository root:

```powershell
python backend/run.py
```

Or from inside the `backend` folder:

```powershell
cd backend
python run.py
```

The Flask REST API will start listening at:
👉 **`http://127.0.0.1:5000`**

---

## 📡 Core API Blueprint Routes

| Route Prefix | Controller | Role / Purpose |
| :--- | :--- | :--- |
| `/api/auth` | `auth_routes.py` | User login, student registration, JWT tokens, `/api/auth/me` |
| `/api/student` | `student_routes.py` | Student stats, active loans, borrowing actions, pass data |
| `/api/books` | `book_routes.py` | Catalog search, category filter, 3D rack location lookup |
| `/api/dashboard` | `dashboard_routes.py` | Executive KPI reels (total volumes, active issues, overdue, fines) |
| `/api/offers` | `community_routes.py` | Student Peer Book Marketplace listings & trade statuses |
| `/api/notes` | `community_routes.py` | Courseware lecture notes and study guides |
| `/api/requests` | `community_routes.py` | Student book acquisition wishlist submissions |
| `/api/contact` | `community_routes.py` | Public help desk inquiry message dispatch |

