from datetime import datetime, timedelta

from app import db
from app.models import IssueRecord, Member, Notification


class NotificationService:
    @staticmethod
    def create_notification(member_id, title, message, notif_type="info"):
        """Create an in-app notification for a member."""
        if not member_id:
            return None
        notif = Notification(
            member_id=member_id,
            title=title,
            message=message,
            type=notif_type,
            is_read=False,
        )
        db.session.add(notif)
        db.session.commit()
        return notif

    @staticmethod
    def get_member_notifications(member_id):
        """Fetch all notifications for a member, with auto due-check."""
        NotificationService.check_due_dates_for_member(member_id)
        notifs = (
            Notification.query.filter_by(member_id=member_id)
            .order_by(Notification.created_at.desc())
            .limit(20)
            .all()
        )
        unread_count = Notification.query.filter_by(member_id=member_id, is_read=False).count()
        return {
            "unread_count": unread_count,
            "notifications": [
                {
                    "id": n.id,
                    "title": n.title,
                    "message": n.message,
                    "type": n.type,
                    "is_read": n.is_read,
                    "created_at": n.created_at.strftime("%b %d, %H:%M"),
                }
                for n in notifs
            ],
        }

    @staticmethod
    def mark_as_read(notif_id, member_id):
        """Mark a single or all notifications as read."""
        if notif_id == "all":
            Notification.query.filter_by(member_id=member_id, is_read=False).update({"is_read": True})
            db.session.commit()
            return True
        notif = Notification.query.filter_by(id=notif_id, member_id=member_id).first()
        if notif:
            notif.is_read = True
            db.session.commit()
            return True
        return False

    @staticmethod
    def check_due_dates_for_member(member_id):
        """Auto-generate reminder if a book is due in <= 48 hours or overdue."""
        now = datetime.utcnow()
        two_days_later = now + timedelta(days=2)

        active_issues = IssueRecord.query.filter_by(member_id=member_id, status="issued").all()
        for issue in active_issues:
            # Overdue alert
            if issue.due_date < now:
                existing_overdue = Notification.query.filter(
                    Notification.member_id == member_id,
                    Notification.type == "overdue",
                    Notification.message.like(f"%{issue.book.title}%"),
                ).first()
                if not existing_overdue:
                    NotificationService.create_notification(
                        member_id=member_id,
                        title=f"⚠️ Overdue Alert: {issue.book.title}",
                        message=f"'{issue.book.title}' was due on {issue.due_date.strftime('%b %d')}. Please return it to avoid additional late fines.",
                        notif_type="overdue",
                    )
            # Due soon alert (within 48 hours)
            elif issue.due_date <= two_days_later:
                existing_soon = Notification.query.filter(
                    Notification.member_id == member_id,
                    Notification.type == "due_soon",
                    Notification.message.like(f"%{issue.book.title}%"),
                ).first()
                if not existing_soon:
                    NotificationService.create_notification(
                        member_id=member_id,
                        title=f"⏳ Due Soon: {issue.book.title}",
                        message=f"'{issue.book.title}' is due in less than 48 hours ({issue.due_date.strftime('%b %d')}). You can renew it for 3 days if needed!",
                        notif_type="due_soon",
                    )

