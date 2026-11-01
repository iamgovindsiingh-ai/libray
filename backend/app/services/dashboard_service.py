from sqlalchemy import func

from app.models import Book, Fine, IssueRecord, Member, StudyNote
from app.models.request import BookOffer, BookRequest, ContactMessage


class DashboardService:
    @staticmethod
    def get_dashboard_stats():
        total_books = Book.query.count()
        available_books = Book.query.filter(Book.available_quantity > 0).count()
        issued_books = Book.query.filter(Book.available_quantity < Book.quantity).count()
        total_members = Member.query.count()
        overdue_books = IssueRecord.query.filter(
            IssueRecord.status == "issued",
            IssueRecord.due_date < func.now(),
        ).count()
        total_fines = Fine.query.filter(Fine.is_paid == False).with_entities(
            func.coalesce(func.sum(Fine.amount), 0)
        ).scalar() or 0

        pending_requests = BookRequest.query.filter_by(status="pending").count()
        total_requests = BookRequest.query.count()
        available_offers = BookOffer.query.filter_by(status="available").count()
        total_for_sale = BookOffer.query.filter_by(offer_type="sell", status="available").count()
        total_study_notes = StudyNote.query.filter_by(status="active").count()
        unread_messages = ContactMessage.query.filter_by(status="unread").count()

        return {
            "total_books": total_books,
            "available_books": available_books,
            "issued_books": issued_books,
            "total_members": total_members,
            "overdue_books": overdue_books,
            "total_fines": float(total_fines),
            "pending_requests": pending_requests,
            "total_requests": total_requests,
            "available_offers": available_offers,
            "total_for_sale": total_for_sale,
            "total_study_notes": total_study_notes,
            "unread_messages": unread_messages,
        }
