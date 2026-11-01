from datetime import datetime

from app import db
from app.models.base import BaseModelMixin


class IssueRecord(BaseModelMixin, db.Model):
    __tablename__ = "issue_records"

    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(30), default="issued", nullable=False)
    notes = db.Column(db.Text, nullable=True)

    book = db.relationship("Book", back_populates="issue_records")
    member = db.relationship("Member", back_populates="issue_records")
    fine = db.relationship("Fine", back_populates="issue_record", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<IssueRecord {self.id}>"
