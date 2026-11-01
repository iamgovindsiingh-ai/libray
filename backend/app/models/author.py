from app import db
from app.models.base import BaseModelMixin


class Author(BaseModelMixin, db.Model):
    __tablename__ = "authors"

    name = db.Column(db.String(150), nullable=False, unique=True)
    bio = db.Column(db.Text, nullable=True)

    books = db.relationship("Book", back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Author {self.name}>"
