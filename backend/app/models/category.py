from app import db
from app.models.base import BaseModelMixin


class Category(BaseModelMixin, db.Model):
    __tablename__ = "categories"

    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

    books = db.relationship("Book", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category {self.name}>"
