import os
import pytest
from app import create_app, db
from app.models import Author, Book, Category, Member, User, IssueRecord
from app.services.ai_service import AIService
from app.services.shelf_service import ShelfService
from app.services.gamification_service import GamificationService
from app.services.review_service import ReviewService
from app.services.request_service import RequestService
from app.services.issue_service import IssueService
from app.services.analytics_service import AnalyticsService
from app.services.auth_service import AuthService


@pytest.fixture(scope="session")
def app():
    os.environ["DATABASE_URL"] = "sqlite:///test_unique_temp.db"
    application = create_app()
    application.config["TESTING"] = True

    with application.app_context():
        db.drop_all()
        db.create_all()

        # Seed author & category
        author = Author.query.filter_by(name="Donald Knuth").first() or Author(name="Donald Knuth").save()
        cat = Category.query.filter_by(name="Computer Science").first() or Category(name="Computer Science").save()

        # Seed book
        book = Book.query.filter_by(isbn="978-0131103627").first()
        if not book:
            book = Book(
                isbn="978-0131103627",
                title="The Art of Computer Programming",
                author_id=author.id,
                category_id=cat.id,
                quantity=5,
                available_quantity=5,
                shelf_location="Zone A · Rack 01 · Shelf 1",
                difficulty_level="Advanced",
                tags="algorithms, computing, data structures, math",
            ).save()

        # Seed student user & member
        student_user = User.query.filter_by(email="student@nexshelf.edu").first()
        if not student_user:
            student_user = AuthService.register_user({
                "email": "student@nexshelf.edu",
                "password": "student123",
                "full_name": "Alan Turing",
                "role": "student",
            })
        member = Member.query.filter_by(user_id=student_user.id).first()
        if member:
            member.department = "Computer Science"
            db.session.commit()

        # Seed admin user
        admin_user = User.query.filter_by(email="admin@nexshelf.edu").first()
        if not admin_user:
            admin_user = AuthService.register_user({
                "email": "admin@nexshelf.edu",
                "password": "admin123",
                "full_name": "Chief Librarian",
                "role": "admin",
            })

        yield application

        db.session.remove()
        db.drop_all()
        if os.path.exists("instance/test_unique_temp.db"):
            try:
                os.remove("instance/test_unique_temp.db")
            except Exception:
                pass


@pytest.fixture
def client(app):
    return app.test_client()


def test_ai_librarian_assistant(app):
    with app.app_context():
        result = AIService.ask_librarian("algorithms and computing project")
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0
        assert "The Art of Computer Programming" in [b["title"] for b in result["recommendations"]]
        assert "Zone A" in result["recommendations"][0]["shelf_location"]


def test_smart_blurb(app):
    with app.app_context():
        book = Book.query.first()
        blurb = AIService.get_smart_blurb(book.id)
        assert blurb is not None
        assert "key_takeaways" in blurb
        assert len(blurb["key_takeaways"]) > 0
        assert blurb["difficulty_level"] == "Advanced"


def test_shelf_locator_and_floor_map(app):
    with app.app_context():
        book = Book.query.first()
        # Test locate
        location = ShelfService.locate_book_on_shelf(book.id)
        assert location["zone"] == "Zone A"
        assert location["rack"] == "Rack 01"
        assert len(location["navigation_steps"]) >= 4

        # Test floor map layout
        floor_map = ShelfService.get_library_map_layout()
        assert "Zone A" in floor_map["zones"]
        assert "Rack 01" in floor_map["zones"]["Zone A"]["racks"]


def test_gamification_and_badges(app):
    with app.app_context():
        book = Book.query.first()
        member = Member.query.filter_by(email="student@nexshelf.edu").first()

        # Issue a book (should trigger FIRST_BORROW badge)
        issue = IssueService.issue_book({
            "book_id": book.id,
            "member_id": member.id,
            "days": 7,
        })
        assert issue is not None

        # Check badges
        profile = GamificationService.get_member_gamification_profile(member.id)
        assert profile["badges_count"] >= 1
        badge_codes = [b["code"] for b in profile["badges"]]
        assert "FIRST_BORROW" in badge_codes
        assert profile["reading_score"] > 0


def test_loan_renewal(app):
    with app.app_context():
        member = Member.query.filter_by(email="student@nexshelf.edu").first()
        active_issue = IssueRecord.query.filter_by(member_id=member.id, status="issued").first()
        assert active_issue is not None
        initial_due = active_issue.due_date

        # Renew loan for 3 days
        renewed_issue = IssueService.renew_loan(active_issue.id, member_id=member.id)
        assert renewed_issue.due_date > initial_due

        # Second renewal should fail (max 1 renewal)
        with pytest.raises(ValueError) as exc:
            IssueService.renew_loan(active_issue.id, member_id=member.id)
        assert "already been renewed" in str(exc.value)


def test_verified_reviews(app):
    with app.app_context():
        book = Book.query.first()
        member = Member.query.filter_by(email="student@nexshelf.edu").first()

        # Post review
        review = ReviewService.add_review(member.id, book.id, 5, "Remarkable foundational guide on algorithms!")
        assert review.rating == 5

        # Check aggregate review
        reviews_data = ReviewService.get_book_reviews(book.id)
        assert reviews_data["review_count"] >= 1
        assert reviews_data["average_rating"] == 5.0


def test_wishlist_desk(app):
    with app.app_context():
        member = Member.query.filter_by(email="student@nexshelf.edu").first()

        # Create request
        req = RequestService.create_request(member.id, {
            "title": "Clean Architecture",
            "author": "Robert C. Martin",
            "category": "Software Engineering",
            "reason": "Crucial for software design patterns class.",
        })
        assert req.status == "pending"
        assert req.votes_count == 1

        # Admin approves request
        updated_req = RequestService.update_request_status(req.id, "approved")
        assert updated_req.status == "approved"


def test_analytics_and_csv(app):
    with app.app_context():
        # Test Chart datasets
        charts = AnalyticsService.get_chart_analytics()
        assert "circulation_trend" in charts
        assert "category_distribution" in charts
        assert "department_activity" in charts

        # Test CSV export
        csv_text = AnalyticsService.generate_csv_export("books")
        assert "ISBN" in csv_text
        assert "The Art of Computer Programming" in csv_text
