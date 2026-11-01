from flask import Blueprint, Response, jsonify

from app.services.citation_service import CitationService


citation_bp = Blueprint("citation_bp", __name__)


@citation_bp.route("/books/<int:book_id>/citations", methods=["GET"])
def get_book_citations(book_id):
    citations = CitationService.generate_citations(book_id)
    if not citations:
        return jsonify({"error": "Book not found."}), 404
    return jsonify(citations), 200


@citation_bp.route("/issues/<int:issue_id>/calendar.ics", methods=["GET"])
def get_issue_calendar(issue_id):
    ics_data = CitationService.generate_ical_event(issue_id)
    if not ics_data:
        return jsonify({"error": "Loan record not found."}), 404
    return Response(
        ics_data,
        mimetype="text/calendar",
        headers={"Content-Disposition": f"attachment; filename=nexshelf_due_reminder_{issue_id}.ics"},
    )
