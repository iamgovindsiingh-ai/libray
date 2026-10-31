from app import db
from app.models.base import BaseModelMixin


class Notification(BaseModelMixin, db.Model):
    __tablename__ = "notifications"

    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), default="info", nullable=False)  # due_soon, overdue, badge_unlocked, wishlist_approved, info
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    member = db.relationship("Member", backref="notifications")

    def __repr__(self):
        return f"<Notification {self.title} member={self.member_id}>"

