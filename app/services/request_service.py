from app import db
from app.models import Author, Book, BookRequest, BookRequestUpvote, Category, Member
from app.services.notification_service import NotificationService


class RequestService:
    @staticmethod
    def create_request(member_id, data):
        """Student submits a book acquisition request."""
        title = (data.get("title") or "").strip()
        author = (data.get("author") or "").strip()
        category = (data.get("category") or "General").strip()
        reason = (data.get("reason") or "").strip()

        if not title or not author:
            raise ValueError("Book title and author are required.")

        req = BookRequest(
            member_id=member_id,
            title=title,
            author=author,
            category=category,
            reason=reason,
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
                "requester_name": r.member.user.full_name if r.member and r.member.user else "Student",
                "requester_dept": r.member.department if r.member else "General",
                "created_at": r.created_at.strftime("%b %d, %Y"),
            }
            for r in requests
        ]

    @staticmethod
    def update_request_status(request_id, new_status):
        """Admin updates status of request (approved, shelved, rejected)."""
        req = BookRequest.query.get(request_id)
        if not req:
            raise ValueError("Request not found.")

        req.status = new_status
        db.session.commit()

        # Send notification to requester
        if new_status in ["approved", "shelved"]:
            NotificationService.create_notification(
                member_id=req.member_id,
                title="Wishlist Book Approved! 📖✨",
                message=f"Good news! Your request for '{req.title}' has been {new_status} by the library administration.",
                notif_type="wishlist_approved",
            )
        return req

