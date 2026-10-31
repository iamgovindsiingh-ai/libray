from app import db
from app.models import Author, Book, BookRequest, BookRequestUpvote, Category, Member
from app.services.notification_service import NotificationService


class RequestService:
    @staticmethod
    def create_request(member_id, data):
        """Student submits a book acquisition request with contact details."""
        title = (data.get("title") or "").strip()
        author = (data.get("author") or "").strip()
        category = (data.get("category") or "General").strip()
        reason = (data.get("reason") or "").strip()
        contact_phone = (data.get("contact_phone") or "").strip()
        contact_whatsapp = (data.get("contact_whatsapp") or "").strip()
        contact_email = (data.get("contact_email") or "").strip()
        urgency = (data.get("urgency") or "normal").strip()

        if not title or not author:
            raise ValueError("Book title and author are required.")

        req = BookRequest(
            member_id=member_id,
            title=title,
            author=author,
            category=category,
            reason=reason,
            contact_phone=contact_phone if contact_phone else None,
            contact_whatsapp=contact_whatsapp if contact_whatsapp else None,
            contact_email=contact_email if contact_email else None,
            urgency=urgency if urgency in ("low", "normal", "high", "urgent") else "normal",
            votes_count=1,
            status="pending",
        )
        db.session.add(req)
        db.session.commit()

        # Add initial self upvote
        upvote = BookRequestUpvote(request_id=req.id, member_id=member_id)
        db.session.add(upvote)
        db.session.commit()

        return req

    @staticmethod
    def upvote_request(request_id, member_id):
        """Upvote a book request."""
        req = BookRequest.query.get(request_id)
        if not req:
            raise ValueError("Request not found.")

        existing = BookRequestUpvote.query.filter_by(request_id=request_id, member_id=member_id).first()
        if existing:
            raise ValueError("You have already upvoted this request.")

        upvote = BookRequestUpvote(request_id=request_id, member_id=member_id)
        req.votes_count += 1
        db.session.add(upvote)
        db.session.commit()
        return req

    @staticmethod
    def get_requests(status=None):
        """Get wishlist requests sorted by upvotes."""
        query = BookRequest.query
        if status:
            query = query.filter_by(status=status)
        requests = query.order_by(BookRequest.votes_count.desc(), BookRequest.created_at.desc()).all()

        return [
            {
                "id": r.id,
                "title": r.title,
                "author": r.author,
                "category": r.category,
                "reason": r.reason,
                "votes_count": r.votes_count,
                "status": r.status,
                "urgency": r.urgency or "normal",
                "contact_phone": r.contact_phone or "",
                "contact_whatsapp": r.contact_whatsapp or "",
                "contact_email": r.contact_email or (r.member.email if r.member else ""),
                "admin_notes": r.admin_notes or "",
                "requester_name": r.member.user.full_name if r.member and r.member.user else "Student",
                "requester_dept": r.member.department if r.member else "General",
                "created_at": r.created_at.strftime("%b %d, %Y"),
            }
            for r in requests
        ]

    @staticmethod
    def update_request_status(request_id, new_status, admin_notes=None):
        """Admin updates status of request (approved, shelved, rejected, contacted)."""
        req = BookRequest.query.get(request_id)
        if not req:
            raise ValueError("Request not found.")

        req.status = new_status
        if admin_notes:
            req.admin_notes = admin_notes
        db.session.commit()

        # Send notification to requester
        status_messages = {
            "approved": f"Good news! Your request for '{req.title}' has been approved by the library administration.",
            "shelved": f"Your request for '{req.title}' has been shelved for future consideration.",
            "rejected": f"Unfortunately, your request for '{req.title}' could not be fulfilled at this time.",
            "contacted": f"The library admin wants to contact you about your request for '{req.title}'. Please check your contact details.",
        }
        if new_status in status_messages:
            NotificationService.create_notification(
                member_id=req.member_id,
                title=f"Book Request Update: {new_status.title()} 📖",
                message=status_messages[new_status],
                notif_type="wishlist_approved" if new_status == "approved" else "info",
            )
        return req

    @staticmethod
    def delete_request(request_id):
        """Admin deletes a book request."""
        req = BookRequest.query.get(request_id)
        if not req:
            raise ValueError("Request not found.")
        db.session.delete(req)
        db.session.commit()
        return True
