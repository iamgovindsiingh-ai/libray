from sqlalchemy import func

from app.models import Book, Fine, IssueRecord, Member


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

        return {
            "total_books": total_books,
            "available_books": available_books,
            "issued_books": issued_books,
            "total_members": total_members,
            "overdue_books": overdue_books,
            "total_fines": float(total_fines),
        }
