# 📚 NexShelf — Next-Gen Smart Library Management System & Scholar Suite

[![React](https://img.shields.io/badge/React-18.3-blue?logo=react&logoColor=white)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5.4-purple?logo=vite&logoColor=white)](https://vitejs.dev)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38bdf8?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.0-lightgrey?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%2F%20PostgreSQL-blue?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Deployment](https://img.shields.io/badge/Deployment-Render%20Ready-success?logo=render&logoColor=white)](https://render.com)

**NexShelf** is an all-in-one smart campus library management platform and scholar community suite. It merges traditional institutional catalog management with modern peer-to-peer textbook exchange, courseware revision sharing, and gamification.

---

## 📁 Clean 3-Tier Architecture

The project is organized into three dedicated, standalone modules:

```text
library/
│
├── 📂 frontend/               # ⚛️ React 18 + Vite + Tailwind CSS Single-Page App (SPA)
│   ├── 📂 src/
│   │   ├── 📂 api/            # Centralized Axios/fetch REST client with JWT Bearer auth
│   │   ├── 📂 components/     # Reusable components (Navbar, ProtectedRoute)
│   │   ├── 📂 context/        # Global AuthContext (user session, roles, tokens)
│   │   ├── 📂 pages/          # Login, Register, StudentDashboard, AdminDashboard, Contact
│   │   ├── 📄 App.jsx         # Client-side routing and route guards
│   │   ├── 📄 main.jsx        # ReactDOM root mount
│   │   └── 📄 index.css       # Aurora background canvas, glassmorphism, 3D spine styles
│   ├── 📄 index.html          # Web page root
│   ├── 📄 package.json        # Frontend dependencies
│   ├── 📄 vite.config.js      # Reverse proxy to Flask backend (:5000)
│   └── 📄 README.md           # Frontend guide
│
├── 📂 backend/                # 🐍 Python Flask REST API Server
│   ├── 📂 app/                # Application package (models, routes, services, utils, templates)
│   │   ├── 📂 models/         # 14 SQLAlchemy ORM relational models
│   │   ├── 📂 routes/         # REST API Blueprints (Auth, Books, Student, Dashboard, etc.)
│   │   ├── 📂 services/       # Business logic (IssueService, AuthService, etc.)
│   │   ├── 📂 utils/          # JWT authentication and decorators
│   │   └── 📂 templates/      # Fallback server-rendered HTML views
│   ├── 📂 tests/              # Backend test suites
│   ├── 📄 config.py           # Database URI & security configuration
│   ├── 📄 run.py              # Backend entrypoint (port 5000)
│   ├── 📄 requirements.txt    # Python dependencies
│   └── 📄 README.md           # Backend guide
│
├── 📂 database/               # 🗄️ Database Storage, Schema & Seeders
│   ├── 📄 library_management.db # Active SQLite database file
│   ├── 📄 schema.sql          # Clean SQL DDL table schema definitions
│   ├── 📄 seed_demo_data.py   # Initial credentials & demonstration data
│   ├── 📄 seed_200_books.py   # 200+ curated academic textbook catalog seeder
│   └── 📄 README.md           # Database documentation
│
├── 📄 run.py                  # Root launcher (convenience wrapper & Render WSGI target)
├── 📄 requirements.txt        # Root dependencies for cloud deployment
├── 📄 render.yaml             # Render cloud infrastructure blueprint
├── 📄 Procfile                # Production WSGI process specification
└── 📄 README.md               # Master repository guide
```

---

## 🚀 How to Run the Project

### Option A: Modern React SPA + Flask REST API (Recommended)

Open **two separate terminal windows**:

#### Terminal 1: Start Backend (Flask API)
```powershell
python backend/run.py
```
> Running at: `http://127.0.0.1:5000`

#### Terminal 2: Start Frontend (React + Vite)
```powershell
cd frontend
npm run dev
```
> Running at: `http://localhost:3000`

---

### Option B: Quick Root Launcher
```powershell
python run.py
```
> Starts the Flask application directly on `http://127.0.0.1:5000`.

---

## 🔑 Demo Account Credentials

| Role | Email | Password | What it opens |
| :--- | :--- | :--- | :--- |
| **Student** | `student@nexshelf.edu` | `student123` | **Scholar Dashboard** (`/student`) |
| **Admin** | `admin@nexshelf.edu` | `admin123` | **Control Console** (`/admin`) |
| **Admin** | `govind@gmail.com` | *(your password)* | **Control Console** (`/admin`) |

*(On the login screen, you can also click the one-click **Demo Student** or **Demo Admin** buttons!)*

---

## 🗄️ Database Seeding

To re-populate or update the database:
```powershell
# Seed demo accounts and initial records:
python database/seed_demo_data.py

# Seed 200+ curated university textbooks:
python database/seed_200_books.py
```
