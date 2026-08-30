from datetime import datetime, timedelta

from app import db
from app.models import Book, IssueRecord, Member


class IssueService:
    @staticmethod
    def issue_book(data):
        book_id = data.get("book_id")
        member_id = data.get("member_id")
        member_email = (data.get("member_email") or "").strip().lower()
        days = int(data.get("days", 7))

        if not book_id or (not member_id and not member_email):
            raise ValueError("Book ID and student email are required.")

        book = Book.query.get(book_id)
        if not book:
            raise ValueError("Book not found.")

        if book.available_quantity <= 0:
            raise ValueError("This book is currently unavailable.")

        member = Member.query.get(member_id) if member_id else Member.query.filter_by(email=member_email).first()
        if not member:
            raise ValueError("Member not found for this email.")

        active_issues = IssueRecord.query.filter_by(member_id=member.id, status="issued").count()
        if active_issues >= 3:
            raise ValueError("This member has reached the maximum borrowing limit.")

        issue_record = IssueRecord(
            book_id=book.id,
            member_id=member.id,
            issue_date=datetime.utcnow(),
            due_date=datetime.utcnow() + timedelta(days=days),
            status="issued",
        )

        book.available_quantity -= 1
        db.session.add(issue_record)
        db.session.commit()

        # Gamification trigger
        try:
            from app.services.gamification_service import GamificationService
            GamificationService.unlock_badge(member.id, "FIRST_BORROW")
        except Exception:
            pass

        return issue_record

    @staticmethod
    def return_book(data):
        issue_id = data.get("issue_id")
        member_email = (data.get("member_email") or "").strip().lower()
        book_id = data.get("book_id")
        if not issue_id and (not member_email or not book_id):
            raise ValueError("Provide an issue ID, or both book ID and student email.")

        if issue_id:
            issue = IssueRecord.query.get(issue_id)
        else:
            member = Member.query.filter_by(email=member_email).first()
            issue = IssueRecord.query.filter_by(
                member_id=member.id if member else None,
                book_id=book_id,
                status="issued",
            ).first()
        if not issue:
            raise ValueError("Active issue record not found.")

        if issue.status == "returned":
            raise ValueError("This book has already been returned.")

        issue.return_date = datetime.utcnow()
        issue.status = "returned"

        book = Book.query.get(issue.book_id)
        if book:
            book.available_quantity += 1

        db.session.commit()
        # A fine is only created for a late return.
        if issue.return_date > issue.due_date:
            from app.services.fine_service import FineService
            FineService.generate_fine_for_issue(issue.id)

        # Gamification trigger for on-time return
        try:
            from app.services.gamification_service import GamificationService
            GamificationService.evaluate_member_badges(issue.member_id)
        except Exception:
            pass

        return issue

    @staticmethod
    def renew_loan(issue_id, member_id=None):
        """Extend an active loan by 3 days."""
        issue = IssueRecord.query.get(issue_id)
        if not issue or issue.status != "issued":
            raise ValueError("Active loan record not found.")

        if member_id and issue.member_id != member_id:
            raise ValueError("Unauthorized to renew this book.")

        now = datetime.utcnow()
        if issue.due_date < now:
            raise ValueError("Cannot renew an overdue book. Please return it and settle outstanding fines.")

        # Check if already renewed (store note or tag)
        if issue.notes and "renewed" in issue.notes.lower():
            raise ValueError("This loan has already been renewed once. Maximum 1 renewal allowed.")

        issue.due_date = issue.due_date + timedelta(days=3)
        issue.notes = (issue.notes or "") + " [Renewed +3 Days]"
        db.session.commit()
        return issue

    @staticmethod
    def get_all_issues():
        return IssueRecord.query.order_by(IssueRecord.issue_date.desc()).all()

    @staticmethod
    def get_overdue_issues():
        now = datetime.utcnow()
        return IssueRecord.query.filter(IssueRecord.status == "issued", IssueRecord.due_date < now).all()

    @staticmethod
    def get_member_history(member_id):
        return IssueRecord.query.filter_by(member_id=member_id).order_by(IssueRecord.issue_date.desc()).all()
