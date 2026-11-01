from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import Member, User
from app.services.ai_service import AIService


ai_bp = Blueprint("ai_bp", __name__)


@ai_bp.route("/ask", methods=["POST"])
@jwt_required(optional=True)
def ask_librarian():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "")
    member = None

    identity = get_jwt_identity()
    if identity:
        try:
            user_id = int(identity)
            member = Member.query.filter_by(user_id=user_id).first()
        except Exception:
            pass

    result = AIService.ask_librarian(query, member)
    return jsonify(result), 200


@ai_bp.route("/blurb/<int:book_id>", methods=["GET"])
def get_smart_blurb(book_id):
    blurb = AIService.get_smart_blurb(book_id)
    if not blurb:
        return jsonify({"error": "Book not found."}), 404
    return jsonify(blurb), 200


@ai_bp.route("/recommendations", methods=["GET"])
@jwt_required()
def get_recommendations():
    identity = get_jwt_identity()
    member = None
    if identity:
        try:
            user_id = int(identity)
            member = Member.query.filter_by(user_id=user_id).first()
        except Exception:
            pass

    recommendations = AIService.get_reading_radar(member)
    return jsonify({"recommendations": recommendations}), 200

