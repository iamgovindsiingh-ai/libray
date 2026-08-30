from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import Member
from app.services.request_service import RequestService
from app.services.review_service import ReviewService
from app.utils.decorators import admin_required, student_required


community_bp = Blueprint("community_bp", __name__)


def _get_student_member():
    user_id = int(get_jwt_identity())
    return Member.query.filter_by(user_id=user_id).first()


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
            "is_verified": review.is_verified,
            "rating": review.rating,
        }), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


# --- Wishlist Requests ---
@community_bp.route("/requests", methods=["GET"])
def get_requests():
    status = request.args.get("status")
    reqs = RequestService.get_requests(status)
    return jsonify({"requests": reqs}), 200


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
    if not status or status not in ["approved", "shelved", "rejected", "pending"]:
        return jsonify({"error": "Valid status is required."}), 400
    try:
        req = RequestService.update_request_status(request_id, status)
        return jsonify({"message": f"Request marked as {status}.", "status": req.status}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

