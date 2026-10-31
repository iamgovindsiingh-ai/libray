from flask import Blueprint, jsonify, request

from app.services.issue_service import IssueService
from app.utils.decorators import admin_required


library_bp = Blueprint("library_bp", __name__)


@library_bp.route("/issues", methods=["POST"])
@admin_required()
def issue_book():
    data = request.get_json(silent=True) or {}

    try:
        issue = IssueService.issue_book(data)
        return jsonify({
            "message": "Book issued successfully.",
            "issue": {
                "id": issue.id,
                "book_id": issue.book_id,
                "member_id": issue.member_id,
                "issue_date": issue.issue_date.isoformat(),
                "due_date": issue.due_date.isoformat(),
                "status": issue.status,
            },
        }), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@library_bp.route("/returns", methods=["POST"])
@admin_required()
def return_book():
    data = request.get_json(silent=True) or {}

    try:
        issue = IssueService.return_book(data)
        return jsonify({
            "message": "Book returned successfully.",
            "issue": {
                "id": issue.id,
                "book_id": issue.book_id,
                "member_id": issue.member_id,
                "return_date": issue.return_date.isoformat() if issue.return_date else None,
                "status": issue.status,
            },
        }), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@library_bp.route("/issues", methods=["GET"])
@admin_required()
def get_issues():
    issues = IssueService.get_all_issues()
    return jsonify({
        "count": len(issues),
        "issues": [
            {
                "id": issue.id,
                "book_id": issue.book_id,
                "member_id": issue.member_id,
                "book_title": issue.book.title if issue.book else None,
                "member_name": issue.member.user.full_name if issue.member and issue.member.user else None,
                "issue_date": issue.issue_date.isoformat(),
                "due_date": issue.due_date.isoformat(),
                "return_date": issue.return_date.isoformat() if issue.return_date else None,
                "status": issue.status,
            }
            for issue in issues
        ],
    }), 200


@library_bp.route("/issues/overdue", methods=["GET"])
@admin_required()
def get_overdue_books():
    overdue = IssueService.get_overdue_issues()
    return jsonify({
        "count": len(overdue),
        "overdue": [
            {
                "id": issue.id,
                "book_id": issue.book_id,
                "member_id": issue.member_id,
                "book_title": issue.book.title if issue.book else None,
                "member_name": issue.member.user.full_name if issue.member and issue.member.user else None,
                "issue_date": issue.issue_date.isoformat(),
                "due_date": issue.due_date.isoformat(),
            }
            for issue in overdue
        ],
    }), 200


@library_bp.route("/members/<int:member_id>/history", methods=["GET"])
@admin_required()
def member_history(member_id):
    issues = IssueService.get_member_history(member_id)
    return jsonify({
        "count": len(issues),
        "history": [
            {
                "id": issue.id,
                "book_id": issue.book_id,
                "book_title": issue.book.title if issue.book else None,
                "issue_date": issue.issue_date.isoformat(),
                "due_date": issue.due_date.isoformat(),
                "return_date": issue.return_date.isoformat() if issue.return_date else None,
                "status": issue.status,
            }
            for issue in issues
        ],
    }), 200
