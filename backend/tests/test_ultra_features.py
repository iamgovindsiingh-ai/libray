import os
import pytest
from app import create_app, db
from app.models import Book, Category, Member, User, IssueRecord
from app.services.citation_service import CitationService
from app.services.book_service import BookService
from app.services.ai_service import AIService
from app.services.issue_service import IssueService
from seed_200_books import seed_200


@pytest.fixture(scope="session")
def app():
    os.environ["DATABASE_URL"] = "sqlite:///test_ultra_temp.db"
    application = create_app()
    application.config["TESTING"] = True

    with application.app_context():
        db.drop_all()
        db.create_all()

        # Run 200+ books seeder
        seed_200()

        # Create demo student & loan
        user = User(
            email="ultra_student@nexshelf.edu",
            password_hash="testhash",
            full_name="Grace Hopper",
            role="student",
            is_active=True,
        )
        db.session.add(user)
        db.session.commit()

        member = Member(
            user_id=user.id,
            student_id="STU-0999",
            email=user.email,
            department="Computer Science",
            year="4th Year",
            is_active=True,
        )
        db.session.add(member)
        db.session.commit()

        # Issue first book for calendar test
        first_book = Book.query.first()
        IssueService.issue_book({
            "book_id": first_book.id,
            "member_id": member.id,
            "days": 7,
        })

        yield application

        db.session.remove()
        db.drop_all()
        if os.path.exists("instance/test_ultra_temp.db"):
            try:
                os.remove("instance/test_ultra_temp.db")
            except Exception:
                pass


def test_200_plus_catalog_inventory(app):
    with app.app_context():
        book_count = Book.query.count()
        assert book_count >= 200, f"Expected at least 200 books, got {book_count}"

        # Verify zones are represented
        all_shelves = [b.shelf_location for b in Book.query.all()]
        assert any("Zone A" in s for s in all_shelves)
        assert any("Zone B" in s for s in all_shelves)
        assert any("Zone C" in s for s in all_shelves)
        assert any("Zone D" in s for s in all_shelves)

        # Verify difficulty levels
        difficulties = set(b.difficulty_level for b in Book.query.all())
        assert "Beginner" in difficulties
        assert "Intermediate" in difficulties
        assert "Advanced" in difficulties


def test_citation_generation(app):
    with app.app_context():
        book = Book.query.filter(Book.title.like("%Algorithms%")).first() or Book.query.first()
        assert book is not None

        c = CitationService.generate_citations(book.id)
        assert c is not None
        assert "ieee" in c
        assert "apa" in c
        assert "mla" in c
        assert "chicago" in c
        assert "harvard" in c
        assert "bibtex" in c

        assert book.title in c["ieee"]
        assert book.title in c["apa"]
        assert "@book" in c["bibtex"]


def test_icalendar_due_reminder(app):
    with app.app_context():
        issue = IssueRecord.query.first()
        assert issue is not None

        ics_str = CitationService.generate_ical_event(issue.id)
        assert ics_str is not None
        assert "BEGIN:VCALENDAR" in ics_str
        assert "END:VCALENDAR" in ics_str
        assert "BEGIN:VEVENT" in ics_str
        assert "SUMMARY:📖 Return Book:" in ics_str
        assert "BEGIN:VALARM" in ics_str


def test_book_search_and_filters(app):
    with app.app_context():
        # Category filter test
        cs_books = BookService.search_books(category="Computer Science")
        assert len(cs_books) > 0
        for b in cs_books:
            assert b.category.name == "Computer Science"

        # Difficulty filter test
        adv_books = BookService.search_books(difficulty="Advanced")
        assert len(adv_books) > 0
        for b in adv_books:
            assert b.difficulty_level == "Advanced"

        # Keyword search test
        found = BookService.search_books(query="Python")
        assert len(found) > 0


def test_voice_ai_recommendations_on_large_catalog(app):
    with app.app_context():
        result = AIService.ask_librarian("deep learning neural networks vision")
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0
        assert "response" in result
