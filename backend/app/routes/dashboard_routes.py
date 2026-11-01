from flask import Blueprint, jsonify

from app.services.dashboard_service import DashboardService
from app.utils.decorators import admin_required


dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.route("/stats", methods=["GET"])
@admin_required()
def get_dashboard_stats():
    stats = DashboardService.get_dashboard_stats()
    return jsonify(stats), 200
