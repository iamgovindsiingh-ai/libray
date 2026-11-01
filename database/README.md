# NexShelf · Database Architecture

This directory houses the SQLite database file, relational database schemas, and seeder automation scripts for **NexShelf Ultra**.

---

## 📁 Directory Structure

| File | Purpose |
| :--- | :--- |
| `library_management.db` | Active SQLite production & development database file |
| `schema.sql` | Pure SQL DDL schema definitions for all 14 entity tables and indexes |
| `seed_demo_data.py` | Seeds administrative credentials (`admin@nexshelf.edu`), student accounts, and initial records |
| `seed_200_books.py` | Seeds 200+ university textbooks across 12 academic disciplines across Zones A through D |

---

## 🗄️ Relational Entities

The system maintains 14 interconnected relational models:

1. **`users`** — Authentication credentials, hashed passwords, and system roles (`admin`, `student`).
2. **`members`** — Student IDs, departments, graduation cohorts, and circulation eligibility.
3. **`books`** — Catalog volumes with 3D spine coordinates, physical rack locations, and stock levels.
4. **`authors`** & **`categories`** — Normalized bibliographic author and discipline relationships.
5. **`issue_records`** — Active circulations, checkout timestamps, due dates, and return history.
6. **`fines`** — Overdue penalty calculations, fine status, and payment tracking.
7. **`reviews`** & **`citations`** — Student peer ratings and automated academic citations.
8. **`book_offers`** — Student Peer Marketplace trade listings and book condition statuses.
9. **`study_notes`** — Peer Courseware notes vault uploads with semester categorization.
10. **`book_requests`** — Student acquisition wishlist tickets submitted for librarian review.
11. **`contact_messages`** — Help desk inquiries submitted to administration.
12. **`gamification_profiles`** & **`notifications`** — Reading streaks, rank badges, and alerts.

---

## ⚡ How to Run Database Seeders

To re-seed or populate records from the repository root:

```powershell
# 1. Seed demo student and administrator credentials:
python database/seed_demo_data.py

# 2. Seed 200+ curated academic textbooks:
python database/seed_200_books.py
```

