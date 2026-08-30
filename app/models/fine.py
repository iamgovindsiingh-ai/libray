from app import db
from app.models.base import BaseModelMixin


class Fine(BaseModelMixin, db.Model):
    __tablename__ = "fines"

    issue_record_id = db.Column(db.Integer, db.ForeignKey("issue_records.id"), nullable=False, unique=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    days_overdue = db.Column(db.Integer, default=0, nullable=False)
    is_paid = db.Column(db.Boolean, default=False, nullable=False)
    paid_at = db.Column(db.DateTime, nullable=True)

    issue_record = db.relationship("IssueRecord", back_populates="fine")
    member = db.relationship("Member", back_populates="fines")

    def __repr__(self):
        return f"<Fine {self.amount}>"
