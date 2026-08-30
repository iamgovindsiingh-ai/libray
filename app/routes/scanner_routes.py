from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity

from app.models import Book, Member, User
from app.services.issue_service import IssueService
from app.utils.decorators import admin_required, student_required


scanner_bp = Blueprint("scanner_bp", __name__)


@scanner_bp.route("/quick-checkout", methods=["POST"])
@admin_required()
def quick_checkout():
    """Rapid desk scanner check-in/check-out endpoint."""
    data = request.get_json(silent=True) or {}
    action = data.get("action", "issue")  # "issue" or "return"
    book_code = (data.get("book_code") or "").strip()
    student_code = (data.get("student_code") or "").strip()

    if not book_code:
        return jsonify({"error": "Book barcode or ID is required."}), 400

    # Resolve book by ID, ISBN, or Barcode
    book = None
    if book_code.isdigit():
        book = Book.query.get(int(book_code))
    if not book:
        book = Book.query.filter((Book.isbn == book_code) | (Book.barcode == book_code)).first()
    if not book:
        return jsonify({"error": f"Book not found for code '{book_code}'."}), 404

    if action == "return":
        try:
            issue = IssueService.return_book({
                "book_id": book.id,
                "member_email": student_code if "@" in student_code else None,
            })
            return jsonify({
                "message": f"✓ '{book.title}' successfully returned to {book.shelf_location or 'Shelf'}.",
                "book_title": book.title,
                "action": "return",
            }), 200
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

    # Issue flow
    if not student_code:
        return jsonify({"error": "Student ID or email is required for issuing a book."}), 400

    member = None
    if "@" in student_code:
        member = Member.query.filter_by(email=student_code.lower()).first()
    else:
        member = Member.query.filter((Member.student_id == student_code) | (Member.id == int(student_code) if student_code.isdigit() else False)).first()

    if not member:
        return jsonify({"error": f"Member not found for '{student_code}'."}), 404

    try:
        issue = IssueService.issue_book({
            "book_id": book.id,
            "member_id": member.id,
            "days": int(data.get("days", 7)),
        })
        return jsonify({
            "message": f"✓ '{book.title}' successfully issued to {member.user.full_name} ({member.student_id}).",
            "book_title": book.title,
            "student_name": member.user.full_name,
            "due_date": issue.due_date.strftime("%b %d, %Y"),
            "action": "issue",
        }), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@scanner_bp.route("/digital-pass", methods=["GET"])
@student_required()
def get_digital_pass():
    """Generates verifiable digital student card pass data."""
    user_id = int(get_jwt_identity())
    member = Member.query.filter_by(user_id=user_id).first()
    if not member:
        return jsonify({"error": "Student profile not found."}), 404

    user = member.user
    qr_payload = f"NEXSHELF-PASS:{member.student_id}:{user.email}:{member.id}"

    return jsonify({
        "student_id": member.student_id,
        "full_name": user.full_name,
        "email": user.email,
        "department": member.department or "Computer Science & Engineering",
        "year": member.year or "3rd Year",
        "phone": member.phone or "—",
        "library_card_no": f"LIB-{member.id:06d}",
        "valid_until": "July 2027",
        "qr_payload": qr_payload,
        "barcode_code": member.student_id,
        "status": "Active · Good Standing" if member.is_active else "Suspended",
    }), 200

