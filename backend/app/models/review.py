from app import db
from app.models.base import BaseModelMixin


class BookReview(BaseModelMixin, db.Model):
    __tablename__ = "book_reviews"

    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)
    review_text = db.Column(db.Text, nullable=True)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)

    book = db.relationship("Book", back_populates="reviews")
    member = db.relationship("Member", backref="reviews")

    def __repr__(self):
        return f"<BookReview book={self.book_id} rating={self.rating}>"

