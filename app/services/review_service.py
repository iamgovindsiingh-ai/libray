from sqlalchemy import func

from app import db
from app.models import Book, BookReview, IssueRecord, Member
from app.services.gamification_service import GamificationService


class ReviewService:
    @staticmethod
    def add_review(member_id, book_id, rating, review_text):
        """Submit a rating and review for a book with verified reader status check."""
        member = Member.query.get(member_id)
        book = Book.query.get(book_id)
        if not member or not book:
            raise ValueError("Member or book not found.")

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                rating = 5
        except (ValueError, TypeError):
            rating = 5

        # Check if student previously borrowed this book
        has_borrowed = IssueRecord.query.filter_by(member_id=member_id, book_id=book_id).first() is not None

        # Check for existing review by this member
        existing = BookReview.query.filter_by(member_id=member_id, book_id=book_id).first()
        if existing:
            existing.rating = rating
            existing.review_text = (review_text or "").strip()
            existing.is_verified = has_borrowed
            db.session.commit()
            review = existing
        else:
            review = BookReview(
                member_id=member_id,
                book_id=book_id,
                rating=rating,
                review_text=(review_text or "").strip(),
                is_verified=has_borrowed,
            )
            db.session.add(review)
            db.session.commit()

        # Unlock gamification badge if applicable
        GamificationService.unlock_badge(member_id, "LITERARY_CRITIC")
        return review

    @staticmethod
    def get_book_reviews(book_id):
        """Fetch all reviews and compute aggregate rating for a book."""
        reviews = (
            BookReview.query.filter_by(book_id=book_id)
            .order_by(BookReview.created_at.desc())
            .all()
        )

        avg_rating = (
            db.session.query(func.avg(BookReview.rating))
            .filter(BookReview.book_id == book_id)
            .scalar()
        ) or 0.0

        return {
            "book_id": book_id,
            "average_rating": round(float(avg_rating), 1),
            "review_count": len(reviews),
            "reviews": [
                {
                    "id": r.id,
                    "student_name": r.member.user.full_name if r.member and r.member.user else "Student",
                    "rating": r.rating,
                    "review_text": r.review_text,
                    "is_verified": r.is_verified,
                    "created_at": r.created_at.strftime("%b %d, %Y"),
                }
                for r in reviews
            ],
        }

