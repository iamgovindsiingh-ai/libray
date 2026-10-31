from app import db
from app.models.request import ContactMessage


class ContactService:
    @staticmethod
    def create_message(data):
        """Public visitor submits a contact message."""
        sender_name = (data.get("sender_name") or "").strip()
        sender_email = (data.get("sender_email") or "").strip()
        sender_phone = (data.get("sender_phone") or "").strip()
        subject = (data.get("subject") or "").strip()
        message = (data.get("message") or "").strip()
        message_type = (data.get("message_type") or "general").strip()

        if not sender_name or not sender_email or not subject or not message:
            raise ValueError("Name, email, subject, and message are required.")

        msg = ContactMessage(
            sender_name=sender_name,
            sender_email=sender_email,
            sender_phone=sender_phone if sender_phone else None,
            subject=subject,
            message=message,
            message_type=message_type,
            status="unread",
        )
        db.session.add(msg)
        db.session.commit()
        return msg

    @staticmethod
    def get_all_messages(status=None):
        """Get all contact messages, optionally filtered by status."""
        query = ContactMessage.query
        if status:
            query = query.filter_by(status=status)
        messages = query.order_by(ContactMessage.created_at.desc()).all()

        return [
            {
                "id": m.id,
                "sender_name": m.sender_name,
                "sender_email": m.sender_email,
                "sender_phone": m.sender_phone or "—",
                "subject": m.subject,
                "message": m.message,
                "message_type": m.message_type,
                "status": m.status,
                "admin_reply": m.admin_reply,
                "created_at": m.created_at.strftime("%b %d, %Y %I:%M %p"),
            }
            for m in messages
        ]

    @staticmethod
    def update_message_status(message_id, new_status, admin_reply=None):
        """Admin updates contact message status and optionally adds a reply."""
        msg = ContactMessage.query.get(message_id)
        if not msg:
            raise ValueError("Message not found.")

        msg.status = new_status
        if admin_reply:
            msg.admin_reply = admin_reply
        db.session.commit()
        return msg

    @staticmethod
    def delete_message(message_id):
        """Admin deletes a contact message."""
        msg = ContactMessage.query.get(message_id)
        if not msg:
            raise ValueError("Message not found.")
        db.session.delete(msg)
        db.session.commit()

