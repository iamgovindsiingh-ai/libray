from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity

from app import db
from app.models import Member, ReadingNote, User
from app.services.gamification_service import GamificationService
from app.utils.decorators import student_required


gamification_bp = Blueprint("gamification_bp", __name__)


def _get_student_member():
    user_id = int(get_jwt_identity())
    member = Member.query.filter_by(user_id=user_id).first()
    if member:
        return member
    user = User.query.get(user_id)
    if not user:
        return None
    member = Member(
        user_id=user.id,
        student_id=f"STU-{user.id:04d}",
        email=user.email,
        department="Computer Science & Engineering" if user.role == "student" else "Library Administration",
        year="3rd Year" if user.role == "student" else "Faculty/Staff",
        is_active=True,
    )
    db.session.add(member)
    db.session.commit()
    return member


@gamification_bp.route("/gamification", methods=["GET"])
@student_required()
def get_gamification_profile():
    member = _get_student_member()
    if not member:
        return jsonify({"error": "Student profile not found."}), 404
    data = GamificationService.get_member_gamification_profile(member.id)
    return jsonify(data), 200


@gamification_bp.route("/notes", methods=["GET"])
@student_required()
def get_reading_notes():
    member = _get_student_member()
    if not member:
        return jsonify({"notes": []})
    notes = ReadingNote.query.filter_by(member_id=member.id).order_by(ReadingNote.created_at.desc()).all()
    return jsonify({
        "notes": [
            {
                "id": n.id,
                "book_id": n.book_id,
                "book_title": n.book.title if n.book else "General Note",
                "title": n.title,
                "note_text": n.note_text,
                "quote": n.quote,
                "page_number": n.page_number,
                "created_at": n.created_at.strftime("%b %d, %Y"),
            }
            for n in notes
        ]
    }), 200


@gamification_bp.route("/notes", methods=["POST"])
@student_required()
def create_reading_note():
    member = _get_student_member()
    if not member:
        return jsonify({"error": "Student profile not found."}), 404
    data = request.get_json(silent=True) or {}
    book_id = data.get("book_id")
    title = (data.get("title") or "").strip()
    note_text = (data.get("note_text") or "").strip()
    quote = (data.get("quote") or "").strip()
    page_number = data.get("page_number")

    if not book_id or not title or not note_text:
        return jsonify({"error": "Book, title, and note content are required."}), 400

    note = ReadingNote(
        member_id=member.id,
        book_id=int(book_id),
        title=title,
        note_text=note_text,
        quote=quote if quote else None,
        page_number=int(page_number) if page_number else None,
    )
    db.session.add(note)
    db.session.commit()

    GamificationService.unlock_badge(member.id, "STUDY_JOURNALIST")
    return jsonify({"message": "Reading note saved to your journal.", "id": note.id}), 201


@gamification_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@student_required()
def delete_reading_note(note_id):
    member = _get_student_member()
    if not member:
        return jsonify({"error": "Student profile not found."}), 404
    note = ReadingNote.query.filter_by(id=note_id, member_id=member.id).first()
    if not note:
        return jsonify({"error": "Note not found."}), 404
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Reading note deleted."}), 200

