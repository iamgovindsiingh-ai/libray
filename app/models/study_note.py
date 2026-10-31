from app import db
from app.models.base import BaseModelMixin


class StudyNote(BaseModelMixin, db.Model):
    """Study notes & exam materials shared by students."""
    __tablename__ = "study_notes"

    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=True)
    semester = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    author_name = db.Column(db.String(150), nullable=False)
    contact_whatsapp = db.Column(db.String(30), nullable=True)
    contact_phone = db.Column(db.String(30), nullable=True)
    contact_email = db.Column(db.String(150), nullable=True)
    file_url = db.Column(db.String(350), nullable=False)
    file_type = db.Column(db.String(30), default="image", nullable=False)  # image, pdf, doc
    likes_count = db.Column(db.Integer, default=0, nullable=False)
    downloads_count = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.String(30), default="active", nullable=False)  # active, pending, archived

    member = db.relationship("Member", backref="study_notes")

    def __repr__(self):
        return f"<StudyNote {self.title} by {self.author_name}>"

