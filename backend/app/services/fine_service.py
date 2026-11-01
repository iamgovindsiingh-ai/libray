from datetime import datetime

from app import db
from app.models import Fine, IssueRecord


class FineService:
    FINE_PER_DAY = 5

    @staticmethod
    def calculate_fine_for_issue(issue_record):
        if not issue_record or issue_record.status == "returned" and issue_record.return_date is not None:
            return 0

        if issue_record.status == "issued":
            current_date = datetime.utcnow()
            overdue_days = max(0, (current_date - issue_record.due_date).days)
            amount = overdue_days * FineService.FINE_PER_DAY
            return amount

        if issue_record.return_date is not None and issue_record.return_date > issue_record.due_date:
            overdue_days = (issue_record.return_date - issue_record.due_date).days
            amount = overdue_days * FineService.FINE_PER_DAY
            return amount

        return 0

    @staticmethod
    def generate_fine_for_issue(issue_id):
        issue = IssueRecord.query.get(issue_id)
        if not issue:
            raise ValueError("Issue record not found.")

        existing_fine = Fine.query.filter_by(issue_record_id=issue.id).first()
        if existing_fine:
            return existing_fine

        amount = FineService.calculate_fine_for_issue(issue)
        fine = Fine(
            issue_record_id=issue.id,
            member_id=issue.member_id,
            amount=amount,
            days_overdue=max(0, (datetime.utcnow() - issue.due_date).days) if issue.status == "issued" else 0,
            is_paid=False,
        )

        if issue.status == "returned" and issue.return_date is not None and issue.return_date > issue.due_date:
            fine.days_overdue = (issue.return_date - issue.due_date).days

        db.session.add(fine)
        db.session.commit()
        return fine

    @staticmethod
    def get_all_fines():
        return Fine.query.order_by(Fine.created_at.desc()).all()

    @staticmethod
    def get_member_fines(member_id):
        return Fine.query.filter_by(member_id=member_id).order_by(Fine.created_at.desc()).all()

    @staticmethod
    def mark_fine_paid(fine_id):
        fine = Fine.query.get(fine_id)
        if not fine:
            raise ValueError("Fine record not found.")

        fine.is_paid = True
        fine.paid_at = datetime.utcnow()
        db.session.commit()
        return fine
