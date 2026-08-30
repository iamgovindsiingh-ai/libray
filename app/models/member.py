from sqlalchemy import UniqueConstraint

from app import db
from app.models.base import BaseModelMixin


class Member(BaseModelMixin, db.Model):
    __tablename__ = "members"
    __table_args__ = (
        UniqueConstraint("student_id", name="uq_members_student_id"),
        UniqueConstraint("email", name="uq_members_email"),
    )

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    student_id = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    year = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    user = db.relationship("User", back_populates="member")
    issue_records = db.relationship("IssueRecord", back_populates="member", cascade="all, delete-orphan")
    fines = db.relationship("Fine", back_populates="member", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Member {self.student_id}>"
