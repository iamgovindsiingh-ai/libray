from flask import Blueprint, jsonify, request

from app.services.member_service import MemberService
from app.utils.decorators import admin_required


member_bp = Blueprint("member_bp", __name__)


@member_bp.route("", methods=["GET"])
@admin_required()
def get_members():
    members = MemberService.get_all_members()
    return jsonify({
        "count": len(members),
        "members": [
            {
                "id": member.id,
                "user_id": member.user_id,
                "student_id": member.student_id,
                "email": member.email,
                "full_name": member.user.full_name if member.user else None,
                "department": member.department,
                "year": member.year,
                "phone": member.phone,
                "is_active": member.is_active,
            }
            for member in members
        ],
    }), 200


@member_bp.route("/<int:member_id>", methods=["GET"])
@admin_required()
def get_member(member_id):
    member = MemberService.get_member_by_id(member_id)
    if not member:
        return jsonify({"error": "Member not found."}), 404

    return jsonify({
        "id": member.id,
        "user_id": member.user_id,
        "student_id": member.student_id,
        "email": member.email,
        "full_name": member.user.full_name if member.user else None,
        "department": member.department,
        "year": member.year,
        "phone": member.phone,
        "address": member.address,
        "is_active": member.is_active,
    }), 200


@member_bp.route("", methods=["POST"])
@admin_required()
def create_member():
    data = request.get_json(silent=True) or {}

    try:
        member = MemberService.create_member(data)
        return jsonify({
            "message": "Member created successfully.",
            "member": {
                "id": member.id,
                "user_id": member.user_id,
                "student_id": member.student_id,
                "email": member.email,
                "department": member.department,
                "year": member.year,
            },
        }), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@member_bp.route("/<int:member_id>", methods=["PUT"])
@admin_required()
def update_member(member_id):
    data = request.get_json(silent=True) or {}

    try:
        member = MemberService.update_member(member_id, data)
        return jsonify({
            "message": "Member updated successfully.",
            "member": {
                "id": member.id,
                "student_id": member.student_id,
                "email": member.email,
                "department": member.department,
                "year": member.year,
            },
        }), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@member_bp.route("/<int:member_id>", methods=["DELETE"])
@admin_required()
def delete_member(member_id):
    try:
        MemberService.delete_member(member_id)
        return jsonify({"message": "Member deleted successfully."}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404
