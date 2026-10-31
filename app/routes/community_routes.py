import os
import uuid
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename

from app.models import Member
from app.services.book_offer_service import BookOfferService
from app.services.contact_service import ContactService
from app.services.request_service import RequestService
from app.services.review_service import ReviewService
from app.services.study_note_service import StudyNoteService
from app.utils.decorators import admin_required, student_required

community_bp = Blueprint("community_bp", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif", "pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _get_student_member():
    user_id = int(get_jwt_identity())
    return Member.query.filter_by(user_id=user_id).first()


# --- File & Picture Upload API ---
@community_bp.route("/upload", methods=["POST"])
def upload_file():
    """Single picture or document upload endpoint."""
    if "file" not in request.files and "image" not in request.files:
        return jsonify({"error": "No file uploaded. Please attach an image or document."}), 400
    file = request.files.get("file") or request.files.get("image")
    if not file or file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if file and allowed_file(file.filename):
        ext = file.filename.rsplit(".", 1)[1].lower()
        base_name = secure_filename(file.filename.rsplit(".", 1)[0])[:30] or "upload"
        filename = f"{uuid.uuid4().hex[:10]}_{base_name}.{ext}"
        upload_folder = os.path.join(current_app.root_path, "static", "uploads")
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        file_url = f"/static/uploads/{filename}"
        return jsonify({
            "message": "File uploaded successfully!",
            "url": file_url,
            "filename": filename
        }), 201

    return jsonify({"error": "File type not supported. Please upload a PNG, JPG, JPEG, WEBP, or PDF."}), 400


# --- Reviews ---
@community_bp.route("/reviews/<int:book_id>", methods=["GET"])
def get_book_reviews(book_id):
    reviews_data = ReviewService.get_book_reviews(book_id)
    return jsonify(reviews_data), 200


@community_bp.route("/reviews/<int:book_id>", methods=["POST"])
@student_required()
def submit_book_review(book_id):
    member = _get_student_member()
    if not member:
        return jsonify({"error": "Student profile not found."}), 404
    data = request.get_json(silent=True) or {}
    rating = data.get("rating", 5)
    review_text = data.get("review_text", "")

    try:
        review = ReviewService.add_review(member.id, book_id, rating, review_text)
        return jsonify({
            "message": "Review submitted successfully.",
            "review": {
                "id": review.id,
                "rating": review.rating,
                "review_text": review.review_text,
                "reviewer_name": member.user.full_name if member.user else "Student",
                "is_verified": review.is_verified,
                "created_at": review.created_at.strftime("%b %d, %Y"),
            },
        }), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


# --- Student Book Requests (Wishlist) ---
@community_bp.route("/requests", methods=["GET"])
def get_requests():
    requests = RequestService.get_requests()
    return jsonify({"requests": requests, "count": len(requests)}), 200


@community_bp.route("/requests", methods=["POST"])
@student_required()
def create_book_request():
    member = _get_student_member()
    if not member:
        return jsonify({"error": "Student profile not found."}), 404
    data = request.get_json(silent=True) or {}
    try:
        req = RequestService.create_request(member.id, data)
        return jsonify({"message": "Book request submitted to the Wishlist Desk.", "id": req.id}), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@community_bp.route("/requests/<int:request_id>/upvote", methods=["POST"])
@student_required()
def upvote_book_request(request_id):
    member = _get_student_member()
    if not member:
        return jsonify({"error": "Student profile not found."}), 404
    try:
        req = RequestService.upvote_request(request_id, member.id)
        return jsonify({"message": "Request upvoted!", "votes_count": req.votes_count}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@community_bp.route("/requests/<int:request_id>/status", methods=["PUT"])
@admin_required()
def update_request_status(request_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    admin_notes = data.get("admin_notes")
    if not status or status not in ["approved", "shelved", "rejected", "contacted", "pending"]:
        return jsonify({"error": "Valid status is required."}), 400
    try:
        req = RequestService.update_request_status(request_id, status, admin_notes)
        return jsonify({"message": f"Request marked as {status}.", "status": req.status}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@community_bp.route("/requests/<int:request_id>", methods=["DELETE"])
@admin_required()
def delete_book_request(request_id):
    try:
        RequestService.delete_request(request_id)
        return jsonify({"message": "Book request deleted successfully."}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404


# --- Peer-to-Peer Book Exchange, Selling & Donation ---
@community_bp.route("/offers", methods=["GET"])
def get_book_offers():
    status = request.args.get("status", "available")
    category = request.args.get("category")
    offer_type = request.args.get("offer_type")
    offers = BookOfferService.get_offers(status=status, category=category, offer_type=offer_type)
    return jsonify({"offers": offers, "count": len(offers)}), 200


@community_bp.route("/offers", methods=["POST"])
@jwt_required(optional=True)
def create_book_offer():
    """Students can list a book to sell, donate, lend, or exchange."""
    data = request.get_json(silent=True) or {}
    member_id = None
    identity = get_jwt_identity()
    if identity:
        try:
            user_id = int(identity)
            member = Member.query.filter_by(user_id=user_id).first()
            if member:
                member_id = member.id
        except Exception:
            pass

    try:
        offer = BookOfferService.create_offer(data, member_id=member_id)
        action_name = "sale listing" if offer.offer_type == "sell" else "offer"
        return jsonify({
            "message": f"Your book {action_name} has been published successfully!",
            "id": offer.id,
        }), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@community_bp.route("/offers/<int:offer_id>/status", methods=["PUT"])
@admin_required()
def update_book_offer_status(offer_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    if not status or status not in ["available", "sold", "claimed", "archived"]:
        return jsonify({"error": "Valid status is required."}), 400
    try:
        offer = BookOfferService.update_offer_status(offer_id, status)
        return jsonify({"message": f"Book offer marked as {status}.", "status": offer.status}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@community_bp.route("/offers/<int:offer_id>", methods=["DELETE"])
@admin_required()
def delete_book_offer(offer_id):
    try:
        BookOfferService.delete_offer(offer_id)
        return jsonify({"message": "Book offer removed."}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404


# --- Study Notes Hub (Notes Upload & Sharing) ---
@community_bp.route("/notes", methods=["GET"])
def get_study_notes():
    status = request.args.get("status", "active")
    subject = request.args.get("subject")
    search = request.args.get("search")
    notes = StudyNoteService.get_notes(status=status, subject=subject, search=search)
    return jsonify({"notes": notes, "count": len(notes)}), 200


@community_bp.route("/notes", methods=["POST"])
@jwt_required(optional=True)
def create_study_note():
    data = request.get_json(silent=True) or {}
    member_id = None
    identity = get_jwt_identity()
    if identity:
        try:
            user_id = int(identity)
            member = Member.query.filter_by(user_id=user_id).first()
            if member:
                member_id = member.id
        except Exception:
            pass
    try:
        note = StudyNoteService.create_note(data, member_id=member_id)
        return jsonify({
            "message": "Study notes uploaded successfully!",
            "id": note.id,
            "title": note.title,
            "subject": note.subject,
            "file_url": note.file_url,
        }), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@community_bp.route("/notes/<int:note_id>/like", methods=["POST"])
def like_study_note(note_id):
    try:
        likes = StudyNoteService.like_note(note_id)
        return jsonify({"message": "Note upvoted!", "likes_count": likes}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404


@community_bp.route("/notes/<int:note_id>/status", methods=["PUT"])
@admin_required()
def update_study_note_status(note_id):
    data = request.get_json(silent=True) or {}
    new_status = data.get("status")
    if not new_status or new_status not in ["active", "pending", "archived"]:
        return jsonify({"error": "Valid status is required."}), 400
    try:
        note = StudyNoteService.update_note_status(note_id, new_status)
        return jsonify({"message": f"Note marked as {new_status}.", "status": note.status}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404


@community_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@admin_required()
def delete_study_note(note_id):
    try:
        StudyNoteService.delete_note(note_id)
        return jsonify({"message": "Study note removed."}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404


# --- Public Contact Messages ---
@community_bp.route("/contact", methods=["POST"])
def submit_contact_message():
    data = request.get_json(silent=True) or {}
    try:
        msg = ContactService.create_message(data)
        return jsonify({
            "message": "Your message has been sent to the library. We'll get back to you soon!",
            "id": msg.id,
        }), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@community_bp.route("/contact/messages", methods=["GET"])
@admin_required()
def get_contact_messages():
    status = request.args.get("status")
    messages = ContactService.get_all_messages(status)
    return jsonify({"messages": messages, "count": len(messages)}), 200


@community_bp.route("/contact/messages/<int:message_id>/status", methods=["PUT"])
@admin_required()
def update_contact_message_status(message_id):
    data = request.get_json(silent=True) or {}
    new_status = data.get("status")
    admin_reply = data.get("admin_reply")
    if not new_status or new_status not in ["unread", "read", "replied", "archived"]:
        return jsonify({"error": "Valid status is required."}), 400
    try:
        msg = ContactService.update_message_status(message_id, new_status, admin_reply)
        return jsonify({"message": f"Message marked as {new_status}.", "status": msg.status}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@community_bp.route("/contact/messages/<int:message_id>", methods=["DELETE"])
@admin_required()
def delete_contact_message(message_id):
    try:
        ContactService.delete_message(message_id)
        return jsonify({"message": "Contact message deleted."}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
