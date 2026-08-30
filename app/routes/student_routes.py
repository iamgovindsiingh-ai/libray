from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity

from app import db
from app.models import Book, Fine, IssueRecord, Member, User
from app.services.issue_service import IssueService
from app.services.notification_service import NotificationService
from app.utils.decorators import student_required


student_bp = Blueprint("student_bp", __name__)


def _member():
    user_id = int(get_jwt_identity())
    member = Member.query.filter_by(user_id=user_id).first()
    if member:
        return member

    # Support student accounts that were created before automatic profiles existed.
    user = User.query.get(user_id)
    if not user or user.role != "student":
        return None
    existing_email_member = Member.query.filter_by(email=user.email).first()
    if existing_email_member:
        existing_email_member.user_id = user.id
        db.session.commit()
        return existing_email_member
    member = Member(
        user_id=user.id,
        student_id=f"STU-{user.id:04d}",
        email=user.email,
        is_active=True,
    )
    db.session.add(member)
    db.session.commit()
    return member


@student_bp.route("/books", methods=["GET"])
@student_required()
def available_books():
    books = Book.query.filter(Book.available_quantity > 0).order_by(Book.title).all()
    return jsonify({
        "books": [
            {
                "id": b.id,
                "title": b.title,
                "author": b.author.name if b.author else "Unknown",
                "category": b.category.name if b.category else "General",
                "available_quantity": b.available_quantity,
                "shelf_location": b.shelf_location or "Zone A · Rack 01 · Shelf 1",
                "difficulty_level": b.difficulty_level or "Intermediate",
                "accent_color": b.accent_color or "#3b82f6",
                "summary": b.summary or b.description,
            }
            for b in books
        ]
    })


@student_bp.route("/issues", methods=["GET"])
@student_required()
def my_issues():
    member = _member()
    issues = IssueRecord.query.filter_by(member_id=member.id).order_by(IssueRecord.issue_date.desc()).all()
    now = datetime.utcnow()
    return jsonify({
        "issues": [
            {
                "id": i.id,
                "book_id": i.book_id,
                "book_title": i.book.title if i.book else "Book",
                "shelf_location": i.book.shelf_location if i.book else "Zone A",
                "issue_date": i.issue_date.isoformat(),
                "due_date": i.due_date.isoformat(),
                "return_date": i.return_date.isoformat() if i.return_date else None,
                "status": i.status,
                "is_overdue": i.status == "issued" and i.due_date < now,
                "is_renewed": bool(i.notes and "renewed" in i.notes.lower()),
                "can_renew": i.status == "issued" and i.due_date >= now and not (i.notes and "renewed" in i.notes.lower()),
            }
            for i in issues
        ]
    })


@student_bp.route("/issues", methods=["POST"])
@student_required()
def borrow_book():
    member = _member()
    try:
        issue = IssueService.issue_book({
            "book_id": (request.get_json(silent=True) or {}).get("book_id"),
            "member_id": member.id,
            "days": 7,
        })
        return jsonify({"message": "Book borrowed successfully.", "issue_id": issue.id}), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@student_bp.route("/returns/<int:issue_id>", methods=["POST"])
@student_required()
def return_my_book(issue_id):
    member = _member()
    issue = IssueRecord.query.get(issue_id)
    if not member or not issue or issue.member_id != member.id:
        return jsonify({"error": "Borrowing record not found."}), 404
    try:
        IssueService.return_book({"issue_id": issue_id})
        return jsonify({"message": "Book returned successfully."})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@student_bp.route("/renew/<int:issue_id>", methods=["POST"])
@student_required()
def renew_my_book(issue_id):
    member = _member()
    try:
        issue = IssueService.renew_loan(issue_id, member_id=member.id)
        return jsonify({
            "message": f"✓ Loan extended by 3 days! New due date: {issue.due_date.strftime('%b %d, %Y')}.",
            "new_due_date": issue.due_date.isoformat(),
        })
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@student_bp.route("/stats", methods=["GET"])
@student_required()
def my_stats():
    member = _member()
    if not member:
        return jsonify({"borrowed_books": 0, "overdue_books": 0, "fine_due": 0})
    active = IssueRecord.query.filter_by(member_id=member.id, status="issued").all()
    fines = Fine.query.filter_by(member_id=member.id, is_paid=False).all()
    return jsonify({
        "borrowed_books": len(active),
        "overdue_books": sum(i.due_date < datetime.utcnow() for i in active),
        "fine_due": sum(float(f.amount) for f in fines),
    })


@student_bp.route("/profile", methods=["GET"])
@student_required()
def my_profile():
    member = _member()
    if not member:
        return jsonify({"error": "Student profile not found."}), 404
    user = member.user
    return jsonify({
        "full_name": user.full_name,
        "email": user.email,
        "student_id": member.student_id,
        "department": member.department,
        "year": member.year,
        "phone": member.phone,
        "address": member.address,
        "is_active": member.is_active,
    })


@student_bp.route("/profile", methods=["PUT"])
@student_required()
def update_my_profile():
    member = _member()
    if not member:
        return jsonify({"error": "Student profile not found."}), 404
    data = request.get_json(silent=True) or {}
    user = member.user

    if "full_name" in data:
        full_name = (data.get("full_name") or "").strip()
        if not full_name:
            return jsonify({"error": "Full name is required."}), 400
        user.full_name = full_name
    for field in ("department", "year", "phone", "address"):
        if field in data:
            setattr(member, field, (data.get(field) or "").strip())

    db.session.commit()
    return jsonify({"message": "Profile updated successfully."})


@student_bp.route("/notifications", methods=["GET"])
@student_required()
def get_notifications():
    member = _member()
    if not member:
        return jsonify({"notifications": [], "unread_count": 0})
    return jsonify(NotificationService.get_member_notifications(member.id)), 200


@student_bp.route("/notifications/read", methods=["POST"])
@student_required()
def mark_notification_read():
    member = _member()
    if not member:
        return jsonify({"error": "Student profile not found."}), 404
    data = request.get_json(silent=True) or {}
    notif_id = data.get("notification_id", "all")
    NotificationService.mark_as_read(notif_id, member.id)
    return jsonify({"message": "Notifications marked as read."}), 200
