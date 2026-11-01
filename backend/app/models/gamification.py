from app import db
from app.models.base import BaseModelMixin


class StudentBadge(BaseModelMixin, db.Model):
    __tablename__ = "student_badges"
    __table_args__ = (
        db.UniqueConstraint("member_id", "badge_code", name="uq_member_badge_code"),
    )

    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    badge_code = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(50), nullable=False, default="medal")
    category = db.Column(db.String(50), nullable=False, default="achievement")

    member = db.relationship("Member", backref="badges")

    def __repr__(self):
        return f"<StudentBadge {self.badge_code} member={self.member_id}>"


class ReadingNote(BaseModelMixin, db.Model):
    __tablename__ = "reading_notes"

    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    note_text = db.Column(db.Text, nullable=False)
    quote = db.Column(db.Text, nullable=True)
    page_number = db.Column(db.Integer, nullable=True)

    member = db.relationship("Member", backref="reading_notes")
    book = db.relationship("Book", back_populates="reading_notes")

    def __repr__(self):
        return f"<ReadingNote {self.title} member={self.member_id}>"

