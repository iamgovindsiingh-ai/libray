from sqlalchemy import UniqueConstraint

from app import db
from app.models.base import BaseModelMixin


class Book(BaseModelMixin, db.Model):
    __tablename__ = "books"
    __table_args__ = (
        UniqueConstraint("isbn", name="uq_books_isbn"),
    )

    isbn = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    publisher = db.Column(db.String(200), nullable=True)
    publication_year = db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    available_quantity = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text, nullable=True)
    shelf_location = db.Column(db.String(100), nullable=True, default="Zone A · Rack 01 · Shelf 1")
    barcode = db.Column(db.String(100), nullable=True)
    accent_color = db.Column(db.String(30), nullable=True, default="#3b82f6")
    difficulty_level = db.Column(db.String(50), nullable=True, default="Intermediate")
    summary = db.Column(db.Text, nullable=True)
    key_takeaways = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(255), nullable=True)

    author = db.relationship("Author", back_populates="books")
    category = db.relationship("Category", back_populates="books")
    issue_records = db.relationship("IssueRecord", back_populates="book", cascade="all, delete-orphan")
    reviews = db.relationship("BookReview", back_populates="book", cascade="all, delete-orphan")
    reading_notes = db.relationship("ReadingNote", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book {self.title}>"
