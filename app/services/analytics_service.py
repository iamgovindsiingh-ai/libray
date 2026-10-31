import csv
import io
from datetime import datetime, timedelta
from sqlalchemy import func

from app import db
from app.models import Book, Category, Fine, IssueRecord, Member


class AnalyticsService:
    @staticmethod
    def get_chart_analytics():
        """Generates datasets tailored for Chart.js interactive rendering."""
        now = datetime.utcnow()

        # 1. Circulation Trends (Last 7 Days)
        dates = [(now - timedelta(days=i)).strftime("%Y-%m-%d") for i in reversed(range(7))]
        daily_issues = []
        daily_returns = []

        for d_str in dates:
            d_start = datetime.strptime(d_str, "%Y-%m-%d")
            d_end = d_start + timedelta(days=1)
            
            issues_count = IssueRecord.query.filter(
                IssueRecord.issue_date >= d_start,
                IssueRecord.issue_date < d_end,
            ).count()

            returns_count = IssueRecord.query.filter(
                IssueRecord.return_date >= d_start,
                IssueRecord.return_date < d_end,
            ).count()

            daily_issues.append(issues_count)
            daily_returns.append(returns_count)

        labels = [(now - timedelta(days=i)).strftime("%b %d") for i in reversed(range(7))]

        # 2. Category Distribution
        categories_data = (
            db.session.query(
                Category.name,
                func.count(Book.id).label("book_count"),
            )
            .join(Book, Book.category_id == Category.id)
            .group_by(Category.name)
            .all()
        )
        cat_labels = [c[0] for c in categories_data] or ["General", "Tech"]
        cat_counts = [c[1] for c in categories_data] or [1, 1]

        # 3. Department Borrowing Ratios
        dept_data = (
            db.session.query(
                Member.department,
                func.count(IssueRecord.id).label("loan_count"),
            )
            .join(IssueRecord, IssueRecord.member_id == Member.id)
            .filter(Member.department != None)
            .group_by(Member.department)
            .all()
        )
        dept_labels = [d[0] or "Unassigned" for d in dept_data] or ["Computer Science", "Information Tech", "Electronics"]
        dept_counts = [d[1] for d in dept_data] or [10, 6, 4]

        # 4. Fine & Recovery stats
        paid_fines = Fine.query.filter_by(is_paid=True).with_entities(func.coalesce(func.sum(Fine.amount), 0)).scalar() or 0
        unpaid_fines = Fine.query.filter_by(is_paid=False).with_entities(func.coalesce(func.sum(Fine.amount), 0)).scalar() or 0

        return {
            "circulation_trend": {
                "labels": labels,
                "issues": daily_issues,
                "returns": daily_returns,
            },
            "category_distribution": {
                "labels": cat_labels,
                "data": cat_counts,
            },
            "department_activity": {
                "labels": dept_labels,
                "data": dept_counts,
            },
            "fine_recovery": {
                "paid": float(paid_fines),
                "unpaid": float(unpaid_fines),
            },
        }

    @staticmethod
    def generate_csv_export(dataset_type="circulation"):
        """Generate formatted CSV string for audit downloads."""
        output = io.StringIO()
        writer = csv.writer(output)

        if dataset_type == "circulation":
            writer.writerow(["Issue ID", "Book Title", "Student Name", "Student ID", "Issue Date", "Due Date", "Return Date", "Status"])
            issues = IssueRecord.query.order_by(IssueRecord.issue_date.desc()).all()
            for i in issues:
                writer.writerow([
                    i.id,
                    i.book.title if i.book else "Unknown",
                    i.member.user.full_name if i.member and i.member.user else "Unknown",
                    i.member.student_id if i.member else "Unknown",
                    i.issue_date.strftime("%Y-%m-%d %H:%M"),
                    i.due_date.strftime("%Y-%m-%d %H:%M"),
                    i.return_date.strftime("%Y-%m-%d %H:%M") if i.return_date else "—",
                    i.status,
                ])
        elif dataset_type == "books":
            writer.writerow(["Book ID", "ISBN", "Title", "Author", "Category", "Shelf Location", "Total Qty", "Available Qty", "Difficulty"])
            books = Book.query.all()
            for b in books:
                writer.writerow([
                    b.id,
                    b.isbn,
                    b.title,
                    b.author.name if b.author else "Unknown",
                    b.category.name if b.category else "Unknown",
                    b.shelf_location or "Zone A",
                    b.quantity,
                    b.available_quantity,
                    b.difficulty_level or "Intermediate",
                ])
        elif dataset_type == "fines":
            writer.writerow(["Fine ID", "Student Name", "Student ID", "Amount (INR)", "Days Overdue", "Paid Status", "Paid Date"])
            fines = Fine.query.all()
            for f in fines:
                writer.writerow([
                    f.id,
                    f.member.user.full_name if f.member and f.member.user else "Unknown",
                    f.member.student_id if f.member else "Unknown",
                    f.amount,
                    f.days_overdue,
                    "PAID" if f.is_paid else "UNPAID",
                    f.paid_at.strftime("%Y-%m-%d") if f.paid_at else "—",
                ])

        return output.getvalue()

