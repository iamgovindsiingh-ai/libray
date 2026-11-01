"""
Seed Demo Data for NexShelf Next-Gen
Creates demo users, categorized books with shelf coordinates, initial wishlist requests, marketplace listings, study notes, and reviews.
"""

from datetime import datetime, timedelta
from app import db
from app.models import (
    Author, Book, Category, Member, User,
    BookOffer, StudyNote, BookRequest
)
from app.services.auth_service import AuthService
from app.services.review_service import ReviewService
from app.services.request_service import RequestService


def seed_data():
    print("[*] Seeding NexShelf demo data...")

    # 1. Admin User
    admin = User.query.filter_by(email="admin@nexshelf.edu").first()
    if not admin:
        admin = AuthService.register_user({
            "email": "admin@nexshelf.edu",
            "password": "admin123",
            "full_name": "Chief Librarian Elena Vance",
            "role": "admin",
<<<<<<< HEAD
        }, allow_admin_role=True)
=======
        })
>>>>>>> 574f13998c394861bfc566a3ff6e3c6c6f0f5e99
        print("  [+] Created Admin: admin@nexshelf.edu (pass: admin123)")

    # 2. Student Users
    students = [
        ("student@nexshelf.edu", "student123", "Aarav Mehta", "Computer Science", 4),
        ("rhea.sharma@nexshelf.edu", "student123", "Rhea Sharma", "Mathematics & Computing", 3),
        ("vikram.patel@nexshelf.edu", "student123", "Vikram Patel", "Artificial Intelligence", 2),
    ]
    student_users = []
    for email, pwd, name, dept, year in students:
        u = User.query.filter_by(email=email).first()
        if not u:
            u = AuthService.register_user({
                "email": email,
                "password": pwd,
                "full_name": name,
                "role": "student",
            })
            print(f"  [+] Created Student: {email} (pass: {pwd})")
        
        m = Member.query.filter_by(user_id=u.id).first()
        if not m:
            m = Member(
                user_id=u.id,
                full_name=name,
                email=email,
                department=dept,
                academic_year=year,
                max_allowed=5,
            )
            db.session.add(m)
            db.session.commit()
        student_users.append((u, m))

    # 3. Categories & Authors
    cat_ai = Category.query.filter_by(name="Artificial Intelligence & ML").first() or Category(name="Artificial Intelligence & ML", description="Deep learning, neural nets, NLP, and agentic workflows.")
    cat_cs = Category.query.filter_by(name="Systems & Algorithms").first() or Category(name="Systems & Algorithms", description="Operating systems, distributed architectures, algorithms.")
    cat_math = Category.query.filter_by(name="Mathematics & Cryptography").first() or Category(name="Mathematics & Cryptography", description="Linear algebra, discrete math, and modern cryptographic primitives.")
    cat_db = Category.query.filter_by(name="Database & Cloud Engineering").first() or Category(name="Database & Cloud Engineering", description="Relational systems, high-throughput cloud storage, and distributed ledgers.")
    
    db.session.add_all([cat_ai, cat_cs, cat_math, cat_db])
    db.session.commit()

    # Books catalog
    books_data = [
        ("978-0262033848", "Introduction to Algorithms (4th Edition)", "Thomas H. Cormen", cat_cs.id, 2022, 6, "Zone A · Rack 01 · Shelf 1", "Algorithms", "#4f46e5", "https://images.unsplash.com/photo-1532012164546-f432f2e3777a?auto=format&fit=crop&w=600&q=80"),
        ("978-0131103627", "The C Programming Language (2nd Edition)", "Brian W. Kernighan", cat_cs.id, 1988, 4, "Zone A · Rack 01 · Shelf 2", "C, Systems", "#06b6d4", "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80"),
        ("978-0262035613", "Deep Learning", "Ian Goodfellow", cat_ai.id, 2016, 5, "Zone A · Rack 02 · Shelf 1", "Deep Learning", "#10b981", "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=600&q=80"),
        ("978-0134685991", "Effective Java (3rd Edition)", "Joshua Bloch", cat_cs.id, 2018, 5, "Zone A · Rack 02 · Shelf 3", "Java, Best Practices", "#f59e0b", "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80"),
        ("978-1491950357", "Designing Data-Intensive Applications", "Martin Kleppmann", cat_db.id, 2017, 7, "Zone B · Rack 01 · Shelf 1", "Distributed Systems, DB", "#8b5cf6", "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=600&q=80"),
        ("978-0132350884", "Clean Code: A Handbook of Agile Craftsmanship", "Robert C. Martin", cat_cs.id, 2008, 6, "Zone B · Rack 01 · Shelf 3", "Software Craft", "#ef4444", "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?auto=format&fit=crop&w=600&q=80"),
        ("978-0134093413", "Operating Systems: Three Easy Pieces", "Remzi H. Arpaci-Dusseau", cat_cs.id, 2018, 5, "Zone B · Rack 02 · Shelf 2", "Operating Systems", "#0284c7", "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=600&q=80"),
        ("978-0980232714", "Mathematics for Machine Learning", "Marc Peter Deisenroth", cat_math.id, 2020, 6, "Zone C · Rack 01 · Shelf 1", "Linear Algebra, Calculus", "#14b8a6", "https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=600&q=80"),
    ]

    for isbn, title, author_name, cat_id, year, qty, shelf, tags, color, cover in books_data:
        b = Book.query.filter_by(isbn=isbn).first()
        if not b:
            auth = Author.query.filter_by(name=author_name).first() or Author(name=author_name)
            db.session.add(auth)
            db.session.commit()
            
            b = Book(
                title=title,
                isbn=isbn,
                category_id=cat_id,
                author_id=auth.id,
                publish_year=year,
                total_copies=qty,
                available_copies=qty,
                shelf_location=shelf,
                tags=tags,
                accent_color=color,
                cover_image_url=cover,
                summary=f"Standard academic edition of {title}. Comprehensive reference volume.",
            )
            db.session.add(b)
    db.session.commit()
    print("  [+] Verified curated library volume catalog.")

    # 4. Student Marketplace Listings
    m_default = student_users[0][1] if student_users else None
    if m_default and BookOffer.query.count() == 0:
        offers_data = [
            ("Introduction to Algorithms (CLRS 3rd Ed)", "Cormen, Leiserson, Rivest", "Computer Science", "Good", "sell", "Aarav Mehta", "+91 98765 43210", "+91 98765 43210", "aarav.mehta@nexshelf.edu", "CS Canteen / Central Library Steps", "Clean edition with no torn pages. All diagrams intact.", 350.0, "https://images.unsplash.com/photo-1532012164546-f432f2e3777a?auto=format&fit=crop&w=600&q=80"),
            ("Operating System Concepts (10th Ed Dinosaur)", "Silberschatz, Galvin, Gagne", "Computer Science", "Like New", "sell", "Rhea Sharma", "+91 98123 45678", "+91 98123 45678", "rhea.sharma@nexshelf.edu", "Girls Hostel 2 Common Room", "Hardcover, sparingly used for OS course last semester. Mint condition.", 450.0, "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=600&q=80"),
            ("Digital Design: With an Introduction to Verilog", "M. Morris Mano, Michael D. Ciletti", "Electronics & CS", "Good", "sell", "Vikram Patel", "+91 97234 56789", "+91 97234 56789", "vikram.patel@nexshelf.edu", "ECE Lab 3 Foyer", "Essential book for 3rd semester logic design. Includes solved state machine examples.", 280.0, "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80"),
            ("Fundamentals of Software Engineering (5th Edition)", "Rajib Mall", "Software Engineering", "Good", "free_donation", "Shreya Dixit", "+91 98123 45678", "+91 98123 45678", "shreya.dixit@nexshelf.edu", "Girls Hostel 1 Common Room", "Free donation (Semester Endowment) for juniors taking Software Engineering! UML diagrams neatly bookmarked.", 0.0, "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=600&q=80"),
            ("Computer Organization and Architecture (11th Ed)", "William Stallings", "Computer Science", "Fair", "lend", "Karan Malhotra", "+91 98345 67890", "+91 98345 67890", "karan.malhotra@nexshelf.edu", "Main Auditorium Steps", "Lending for entire semester! RISC pipeline and cache mapping chapters highlighted.", 0.0, "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80"),
        ]
        for t, a, c, cond, o_type, d_name, phone, wa, email, loc, desc, price, img in offers_data:
            bo = BookOffer(
                title=t,
                author=a,
                category=c,
                condition=cond,
                offer_type=o_type,
                donor_name=d_name,
                contact_phone=phone,
                contact_whatsapp=wa,
                contact_email=email,
                pickup_location=loc,
                description=desc,
                price=price,
                image_url=img,
                member_id=m_default.id,
                status="available",
            )
            db.session.add(bo)
        db.session.commit()
        print("  [+] Seeded Student Peer Marketplace offers.")

    # 5. Study Notes & Exam Materials
    if m_default and StudyNote.query.count() == 0:
        notes_data = [
            ("Data Structures & Dynamic Programming Formula Sheet", "CS201 · Data Structures", "Trees, Avl Rotations, DP State Equations, and Graph Algorithms (Dijkstra, Bellman-Ford) neatly handwritten with time complexities.", "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=600&q=80", "Aarav Mehta (Rank 1 CS)", 34),
            ("Database Management Systems · Complete Normalization Guide", "CS304 · DBMS", "1NF to BCNF step-by-step canonical decomposition examples, relational algebra cheat sheet, and transaction ACID recovery rules.", "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=600&q=80", "Rhea Sharma (TA DBMS)", 28),
            ("Theory of Computation · Complete DFA/NFA & Turing Machine Notes", "CS302 · Theory of Computation", "Handcrafted state transition diagrams, Pumping Lemma proofs for regular & CFLs, and reduction techniques for undecidability.", "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80", "Ananya Deshmukh", 19),
        ]
        for t, s, d, img, author_lbl, likes in notes_data:
            sn = StudyNote(
                title=t,
                subject=s,
                description=d,
                file_url=img,
                member_id=m_default.id,
                status="approved",
                likes_count=likes,
            )
            db.session.add(sn)
        db.session.commit()
        print("  [+] Seeded Student Study Notes.")

    print("[*] All NexShelf demo data ready.")


def seed():
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_data()


if __name__ == "__main__":
    seed()
