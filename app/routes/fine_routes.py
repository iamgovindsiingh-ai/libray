from flask import Blueprint, jsonify, request

from app.services.fine_service import FineService
from app.utils.decorators import admin_required


fine_bp = Blueprint("fine_bp", __name__)


@fine_bp.route("", methods=["GET"])
@admin_required()
def get_fines():
    fines = FineService.get_all_fines()
    return jsonify({
        "count": len(fines),
        "fines": [
            {
                "id": fine.id,
                "issue_record_id": fine.issue_record_id,
                "member_id": fine.member_id,
                "amount": float(fine.amount),
                "days_overdue": fine.days_overdue,
                "is_paid": fine.is_paid,
                "paid_at": fine.paid_at.isoformat() if fine.paid_at else None,
            }
            for fine in fines
        ],
    }), 200


@fine_bp.route("/member/<int:member_id>", methods=["GET"])
@admin_required()
def get_member_fines(member_id):
    fines = FineService.get_member_fines(member_id)
    return jsonify({
        "count": len(fines),
        "fines": [
            {
                "id": fine.id,
                "issue_record_id": fine.issue_record_id,
                "amount": float(fine.amount),
                "days_overdue": fine.days_overdue,
                "is_paid": fine.is_paid,
                "paid_at": fine.paid_at.isoformat() if fine.paid_at else None,
            }
            for fine in fines
        ],
    }), 200


@fine_bp.route("/<int:fine_id>/pay", methods=["POST"])
@admin_required()
def pay_fine(fine_id):
    try:
        fine = FineService.mark_fine_paid(fine_id)
        return jsonify({
            "message": "Fine marked as paid.",
            "fine": {
                "id": fine.id,
                "amount": float(fine.amount),
                "is_paid": fine.is_paid,
                "paid_at": fine.paid_at.isoformat() if fine.paid_at else None,
            },
        }), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404
