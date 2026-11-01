from flask import Blueprint, Response, jsonify, request

from app.services.analytics_service import AnalyticsService
from app.utils.decorators import admin_required


analytics_bp = Blueprint("analytics_bp", __name__)


@analytics_bp.route("/charts", methods=["GET"])
@admin_required()
def get_chart_data():
    data = AnalyticsService.get_chart_analytics()
    return jsonify(data), 200


@analytics_bp.route("/export/csv", methods=["GET"])
@admin_required()
def export_csv():
    dataset_type = request.args.get("type", "circulation")
    csv_content = AnalyticsService.generate_csv_export(dataset_type)
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=nexshelf_{dataset_type}_export.csv"},
    )

