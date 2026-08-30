from app import db
from app.models.base import BaseModelMixin


class BookRequest(BaseModelMixin, db.Model):
    __tablename__ = "book_requests"

    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    reason = db.Column(db.Text, nullable=True)
    votes_count = db.Column(db.Integer, default=1, nullable=False)
    status = db.Column(db.String(30), default="pending", nullable=False)  # pending, approved, shelved, rejected

    member = db.relationship("Member", backref="book_requests")
    upvotes = db.relationship("BookRequestUpvote", back_populates="request", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<BookRequest {self.title} - {self.status}>"


class BookRequestUpvote(BaseModelMixin, db.Model):
    __tablename__ = "book_request_upvotes"
    __table_args__ = (
        db.UniqueConstraint("request_id", "member_id", name="uq_request_member_upvote"),
    )

    request_id = db.Column(db.Integer, db.ForeignKey("book_requests.id"), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)

    request = db.relationship("BookRequest", back_populates="upvotes")
    member = db.relationship("Member", backref="upvotes")

