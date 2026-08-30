from sqlalchemy import UniqueConstraint

from app import db
from app.models.base import BaseModelMixin


class User(BaseModelMixin, db.Model):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
    )

    email = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="student")
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    member = db.relationship("Member", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"
