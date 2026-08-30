"""
Seed Demo Data for NexShelf Next-Gen
Creates demo users, categorized books with shelf coordinates, initial wishlist requests, and reviews.
"""

from app import create_app, db
from app.models import Author, Book, Category, Member, User
from app.services.auth_service import AuthService
from app.services.review_service import ReviewService
from app.services.request_service import RequestService


def seed():
    app = create_app()
    with app.app_context():
        print("[*] Seeding NexShelf demo data...")

        # 1. Admin User
        admin = User.query.filter_by(email="admin@nexshelf.edu").first()
        if not admin:
            admin = AuthService.register_user({
                "email": "admin@nexshelf.edu",
                "password": "admin123",
                "full_name": "Chief Librarian Elena Vance",
                "role": "admin",
            })
            print("  [+] Created Admin: admin@nexshelf.edu (pass: admin123)")

        # 2. Student Users
        students = [
            ("student@nexshelf.edu", "student123", "Alan Turing", "Computer Science & Engineering", "3rd Year"),
            ("ada@nexshelf.edu", "ada123", "Ada Lovelace", "Information Technology", "2nd Year"),
            ("ramanujan@nexshelf.edu", "ram123", "Srinivasa Ramanujan", "Mathematics & Computing", "4th Year"),
        ]
        created_members = []
        for email, pwd, name, dept, yr in students:
            u = User.query.filter_by(email=email).first()
            if not u:
                u = AuthService.register_user({
                    "email": email,
                    "password": pwd,
                    "full_name": name,
                    "role": "student",
                })
            m = Member.query.filter_by(user_id=u.id).first()
            if m:
                m.department = dept
                m.year = yr
                db.session.commit()
                created_members.append(m)
        print("  [+] Created Student accounts (e.g. student@nexshelf.edu / student123)")

        # 3. Categories & Authors
        demo_catalog = [
            # Zone A: Computing & AI
            {
                "isbn": "978-0131103627",
                "title": "The C Programming Language",
                "author": "Brian Kernighan & Dennis Ritchie",
                "category": "Computer Science",
                "qty": 6,
                "shelf": "Zone A · Rack 01 · Shelf 1",
                "difficulty": "Intermediate",
                "color": "#3b82f6",
                "tags": "c, programming, system programming, fundamentals",
                "summary": "The definitive authoritative guide to ANSI C programming written by the designers of the language.",
                "takeaways": "Pointers and memory structures; Low-level data manipulation; System calls interface; High-speed algorithm design",
            },
            {
                "isbn": "978-0262033848",
                "title": "Introduction to Algorithms (CLRS)",
                "author": "Thomas H. Cormen",
                "category": "Computer Science",
                "qty": 8,
                "shelf": "Zone A · Rack 01 · Shelf 2",
                "difficulty": "Advanced",
                "color": "#2563eb",
                "tags": "algorithms, data structures, dynamic programming, graphs, sorting",
                "summary": "Comprehensive reference textbook covering the entire spectrum of modern algorithms and complexity analysis.",
                "takeaways": "Asymptotic notation and recurrence analysis; Greedy algorithms and dynamic programming; Graph traversal and network flow; NP-completeness proofs",
            },
            {
                "isbn": "978-0262035613",
                "title": "Deep Learning",
                "author": "Ian Goodfellow & Yoshua Bengio",
                "category": "Artificial Intelligence",
                "qty": 4,
                "shelf": "Zone A · Rack 02 · Shelf 1",
                "difficulty": "Advanced",
                "color": "#1d4ed8",
                "tags": "deep learning, ai, neural networks, machine learning, vision",
                "summary": "The definitive deep learning bible introducing mathematical fundamentals, convolutional nets, and generative models.",
                "takeaways": "Applied linear algebra and probability for AI; Convolutional & Recurrent neural networks; Optimization algorithms (Adam, RMSProp); Autoencoders and GANs",
            },
            {
                "isbn": "978-1449355739",
                "title": "Learning Python",
                "author": "Mark Lutz",
                "category": "Programming",
                "qty": 5,
                "shelf": "Zone A · Rack 03 · Shelf 1",
                "difficulty": "Beginner",
                "color": "#60a5fa",
                "tags": "python, beginner, scripting, oop, basics",
                "summary": "In-depth, hands-on tutorial for learning Python from scratch to building full applications.",
                "takeaways": "Python syntax and built-in object types; Object-oriented programming principles; Exception handling and file operations; Standard library modules",
            },
            # Zone B: Mathematics & Theory
            {
                "isbn": "978-0073383095",
                "title": "Discrete Mathematics and Its Applications",
                "author": "Kenneth H. Rosen",
                "category": "Mathematics",
                "qty": 5,
                "shelf": "Zone B · Rack 04 · Shelf 1",
                "difficulty": "Intermediate",
                "color": "#10b981",
                "tags": "discrete math, logic, sets, combinatorics, graph theory",
                "summary": "A precise and relevant introduction to mathematical concepts essential for computer scientists.",
                "takeaways": "Propositional logic and predicate calculus; Set theory, relations, and functions; Combinatorics and probability; Graph models and tree traversal",
            },
            {
                "isbn": "978-0980232714",
                "title": "Linear Algebra Done Right",
                "author": "Sheldon Axler",
                "category": "Mathematics",
                "qty": 4,
                "shelf": "Zone B · Rack 05 · Shelf 2",
                "difficulty": "Intermediate",
                "color": "#059669",
                "tags": "linear algebra, vectors, matrices, eigenvalues, transformations",
                "summary": "Clear, modern approach focusing on linear operators and vector spaces without premature determinant clutter.",
                "takeaways": "Finite-dimensional vector spaces; Linear maps and dual spaces; Eigenvalues, eigenvectors, and invariant subspaces; Inner product spaces and spectral theorem",
            },
            # Zone C: Electronics & Robotics
            {
                "isbn": "978-0198075721",
                "title": "Microelectronic Circuits",
                "author": "Adel S. Sedra & Kenneth C. Smith",
                "category": "Electronics",
                "qty": 4,
                "shelf": "Zone C · Rack 06 · Shelf 1",
                "difficulty": "Advanced",
                "color": "#f59e0b",
                "tags": "electronics, circuits, semiconductors, mosfet, op-amps",
                "summary": "The gold-standard reference on analog and digital electronic circuit analysis and design.",
                "takeaways": "Operational amplifier circuits; Diode characteristics and rectifier models; BJT and MOSFET amplifier topologies; Digital CMOS logic design",
            },
            {
                "isbn": "978-0262015356",
                "title": "Introduction to Autonomous Mobile Robots",
                "author": "Roland Siegwart",
                "category": "Robotics",
                "qty": 3,
                "shelf": "Zone C · Rack 07 · Shelf 2",
                "difficulty": "Advanced",
                "color": "#d97706",
                "tags": "robotics, autonomous, sensors, slam, navigation",
                "summary": "Comprehensive introduction to mobile robot locomotion, sensor perception, localization, and motion planning.",
                "takeaways": "Kinematics and wheel locomotion; Sensor perception (LiDAR, Vision, Sonar); Kalman filtering and SLAM localization; Path planning and obstacle avoidance",
            },
            # Zone D: General & Reference
            {
                "isbn": "978-0132350884",
                "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
                "author": "Robert C. Martin",
                "category": "Software Engineering",
                "qty": 6,
                "shelf": "Zone D · Rack 08 · Shelf 1",
                "difficulty": "Intermediate",
                "color": "#8b5cf6",
                "tags": "clean code, agile, refactoring, best practices, design",
                "summary": "Revolutionary guide on writing readable, maintainable, and elegant software systems.",
                "takeaways": "Meaningful naming and small focused functions; Error handling over return codes; Unit testing and Test-Driven Development (TDD); Code refactoring smells and heuristics",
            },
        ]

        for item in demo_catalog:
            existing = Book.query.filter_by(isbn=item["isbn"]).first()
            if not existing:
                author = Author.query.filter_by(name=item["author"]).first()
                if not author:
                    author = Author(name=item["author"]).save()
                cat = Category.query.filter_by(name=item["category"]).first()
                if not cat:
                    cat = Category(name=item["category"]).save()

                b = Book(
                    isbn=item["isbn"],
                    title=item["title"],
                    author_id=author.id,
                    category_id=cat.id,
                    quantity=item["qty"],
                    available_quantity=item["qty"],
                    shelf_location=item["shelf"],
                    difficulty_level=item["difficulty"],
                    accent_color=item["color"],
                    tags=item["tags"],
                    summary=item["summary"],
                    key_takeaways=item["takeaways"],
                ).save()
                print(f"  [+] Shelved: {b.title} ({b.shelf_location})")

        # 4. Seed Wishlist Requests
        if created_members:
            m = created_members[0]
            reqs = [
                ("Designing Data-Intensive Applications", "Martin Kleppmann", "Distributed Systems", "Essential reading for modern cloud and backend architecture class."),
                ("Cracking the Coding Interview", "Gayle Laakmann McDowell", "Computer Science", "Need this for final semester campus placement interview preparation."),
            ]
            for title, author, cat, reason in reqs:
                try:
                    RequestService.create_request(m.id, {
                        "title": title,
                        "author": author,
                        "category": cat,
                        "reason": reason,
                    })
                except Exception:
                    pass
            print("  [+] Seeded Wishlist Desk requests.")

            # Seed a sample review
            b1 = Book.query.filter_by(isbn="978-0131103627").first()
            if b1:
                try:
                    ReviewService.add_review(m.id, b1.id, 5, "An absolute timeless masterpiece. The exercises really sharpen your pointer arithmetic!")
                    print("  [+] Seeded Verified Reader review.")
                except Exception:
                    pass

        print("[*] Seeding complete! NexShelf is loaded and ready.")


if __name__ == "__main__":
    seed()
