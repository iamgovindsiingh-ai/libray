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
    status = db.Column(db.String(30), default="pending", nullable=False)  # pending, approved, shelved, rejected, contacted

    # Contact details so admin & peers can reach the student
    contact_phone = db.Column(db.String(30), nullable=True)
    contact_whatsapp = db.Column(db.String(30), nullable=True)
    contact_email = db.Column(db.String(150), nullable=True)
    urgency = db.Column(db.String(20), default="normal", nullable=False)  # low, normal, high, urgent
    admin_notes = db.Column(db.Text, nullable=True)

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


class BookOffer(BaseModelMixin, db.Model):
    """Peer-to-peer book sharing & donation model.
    Students or donors can offer books they want to give/lend to others."""
    __tablename__ = "book_offers"

    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    condition = db.Column(db.String(50), default="Good", nullable=False)  # Brand New, Like New, Good, Fair
    offer_type = db.Column(db.String(50), default="free_giveaway", nullable=False)  # free_giveaway, lend_share, exchange, sell
    price = db.Column(db.Float, default=0.0, nullable=True)  # Set price if selling book (₹)
    image_url = db.Column(db.String(350), nullable=True)  # Uploaded picture of book cover / condition
    donor_name = db.Column(db.String(150), nullable=False)
    contact_phone = db.Column(db.String(30), nullable=True)
    contact_whatsapp = db.Column(db.String(30), nullable=True)
    contact_email = db.Column(db.String(150), nullable=False)
    pickup_location = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default="available", nullable=False)  # available, claimed, archived

    member = db.relationship("Member", backref="book_offers")

    def __repr__(self):
        return f"<BookOffer {self.title} by {self.donor_name} - {self.status}>"


class ContactMessage(BaseModelMixin, db.Model):
    """Public contact form - anyone can message the library without logging in."""
    __tablename__ = "contact_messages"

    sender_name = db.Column(db.String(150), nullable=False)
    sender_email = db.Column(db.String(150), nullable=False)
    sender_phone = db.Column(db.String(30), nullable=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(30), default="general", nullable=False)  # general, book_inquiry, feedback, complaint, other
    status = db.Column(db.String(20), default="unread", nullable=False)  # unread, read, replied, archived
    admin_reply = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<ContactMessage {self.subject} from {self.sender_name}>"
