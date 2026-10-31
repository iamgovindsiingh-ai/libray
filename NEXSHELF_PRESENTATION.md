# NexShelf

## Smart Library Management System

**Project presentation**

> A digital library desk for managing books, members, borrowing, returns, and fines.

---

## Slide 1: Title

### NexShelf

**Smart Library Management System**

- Presented by: GOVIND SINGH & LAKSHYA 
- Course / department: BTECH CSE
- Project type: Mini project

**Speaker note:** NexShelf replaces scattered library records with one role-aware system for students and administrators.

---

## Slide 2: Problem Statement

### Why NexShelf?

- Manual registers are slow to update and difficult to search.
- Staff need a reliable view of available and issued books.
- Borrowing history and overdue items can be missed.
- Fine calculation and payment status need consistent tracking.
- Students need quick access to their own borrowing information.

**Goal:** Build a centralized, easy-to-use library management platform.

---

## Slide 3: Objectives

- Maintain an organized digital catalog of books.
- Manage student accounts and member profiles.
- Track book issue and return transactions.
- Detect overdue books and calculate fines.
- Provide separate experiences for administrators and students.
- Protect restricted operations with authenticated access.

---

## Slide 4: Users and Core Workflows

### Administrator

- Add, update, search, and remove books.
- Create and manage member records.
- Issue and return books.
- View overdue loans, fines, history, and dashboard statistics.
- Mark fines as paid.

### Student

- Browse available books.
- Borrow and return books.
- View active loans and borrowing history.
- View borrowing statistics and update profile details.

**Demo flow:** Login -> Browse catalog -> Borrow -> View due date -> Return -> Review fine status.

---

## Slide 5: Main Features

### Catalog and Members

- Book records include ISBN, title, author, category, publisher, year, and quantity.
- Search endpoint supports catalog lookup.
- Member profiles include student ID, email, department, year, phone, and address.

### Circulation

- Available quantity decreases when a book is issued.
- Available quantity increases when a book is returned.
- Issue records preserve dates, status, and member/book relationships.
- Borrowing is limited to three active books per member.

---

## Slide 6: Fines and Dashboard

### Operational visibility

- Overdue loans are identified from due dates and active status.
- Fines are calculated at **5 currency units per overdue day**.
- A fine is generated for a late return.
- Administrators can mark fines as paid.
- Dashboard statistics include:
  - Total books
  - Available books
  - Issued books
  - Registered members
  - Overdue books
  - Unpaid fine total

---

## Slide 7: System Architecture

```text
Browser UI
  |-- Admin dashboard
  |-- Student dashboard
  |-- Login / registration pages
          |
          v
Flask application
  |-- Blueprint routes: auth, books, members, library, dashboard, fines, student
  |-- Service layer: authentication, books, members, issues, fines, dashboard
  |-- Access decorators: admin_required, student_required
          |
          v
SQLAlchemy ORM
  |-- Users and Members
  |-- Books, Authors, Categories
  |-- Issue Records and Fines
          |
          v
SQLite for development / MySQL-compatible configuration for production
```

**Speaker note:** Routes handle HTTP requests, services hold business rules, and SQLAlchemy models persist the data.

---

## Slide 8: Technology Stack and Security

### Technology stack

- **Backend:** Python, Flask
- **Database layer:** Flask-SQLAlchemy / SQLAlchemy ORM
- **Authentication:** Flask-JWT-Extended
- **Password protection:** Werkzeug password hashing
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Database options:** SQLite for development, MySQL for production configuration

### Security controls

- JWT access tokens are issued at login.
- Admin and student endpoints use role-based decorators.
- Passwords are stored as hashes, not plain text.
- Unique constraints protect user emails, member IDs, and ISBNs.
- API errors return structured JSON responses.

---

## Slide 9: Demonstration and Expected Results

### Demonstration checklist

1. Register or log in as a student.
2. Log in as an administrator.
3. Add a book and confirm it appears in the catalog.
4. Issue the book to a member.
5. Confirm available quantity and dashboard totals change.
6. Open the overdue or issue records view.
7. Return the book and confirm inventory is restored.
8. Show fine generation for a late return and mark it paid.
9. Return to the student dashboard and show personal stats.

### Expected result

A complete circulation cycle is recorded consistently from acquisition to return.

---

## Slide 10: Conclusion and Future Scope

### Conclusion

NexShelf provides a structured digital workflow for library operations, combining catalog management, member management, circulation, overdue monitoring, and fine tracking in one application.

### Future improvements

- Add automated email or notification reminders for due dates.
- Add pagination and advanced catalog filters.
- Add audit logs for administrative actions.
- Add automated database migrations and deployment configuration.
- Add reporting exports for circulation and fines.
- Add automated tests and CI validation.

**Thank you**

### Questions?
