from flask import Blueprint, jsonify, request

from app.models import Book
from app.services.book_service import BookService
from app.utils.decorators import admin_required


book_bp = Blueprint("book_bp", __name__)


@book_bp.route("", methods=["GET"])
def get_books():
    search = request.args.get("search", "")
    category = request.args.get("category", "")
    difficulty = request.args.get("difficulty", "")
    available_only = request.args.get("available_only", "false").lower() in ["true", "1", "yes"]

    books = BookService.search_books(search, category, difficulty, available_only)
    return jsonify({
        "count": len(books),
        "books": [
            {
                "id": book.id,
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author.name if book.author else None,
                "category": book.category.name if book.category else None,
                "publisher": book.publisher,
                "publication_year": book.publication_year,
                "quantity": book.quantity,
                "available_quantity": book.available_quantity,
                "shelf_location": book.shelf_location or "Zone A · Rack 01 · Shelf 1",
                "difficulty_level": book.difficulty_level or "Intermediate",
                "accent_color": book.accent_color or "#3b82f6",
                "tags": book.tags,
                "summary": book.summary or book.description,
            }
            for book in books
        ],
    }), 200


@book_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = BookService.get_book_by_id(book_id)
    if not book:
        return jsonify({"error": "Book not found."}), 404

    return jsonify({
        "id": book.id,
        "isbn": book.isbn,
        "title": book.title,
        "author": book.author.name if book.author else None,
        "category": book.category.name if book.category else None,
        "publisher": book.publisher,
        "publication_year": book.publication_year,
        "quantity": book.quantity,
        "available_quantity": book.available_quantity,
        "description": book.description,
        "shelf_location": book.shelf_location or "Zone A · Rack 01 · Shelf 1",
        "difficulty_level": book.difficulty_level or "Intermediate",
        "accent_color": book.accent_color or "#3b82f6",
        "summary": book.summary,
        "key_takeaways": book.key_takeaways,
        "tags": book.tags,
        "barcode": book.barcode or book.isbn,
    }), 200


@book_bp.route("", methods=["POST"])
@admin_required()
def create_book():
    data = request.get_json(silent=True) or {}

    try:
        book = BookService.create_book(data)
        return jsonify({
            "message": "Book created successfully.",
            "book": {
                "id": book.id,
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author.name if book.author else None,
                "category": book.category.name if book.category else None,
                "quantity": book.quantity,
                "available_quantity": book.available_quantity,
            },
        }), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@book_bp.route("/<int:book_id>", methods=["PUT"])
@admin_required()
def update_book(book_id):
    data = request.get_json(silent=True) or {}

    try:
        book = BookService.update_book(book_id, data)
        return jsonify({
            "message": "Book updated successfully.",
            "book": {
                "id": book.id,
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author.name if book.author else None,
                "category": book.category.name if book.category else None,
                "quantity": book.quantity,
                "available_quantity": book.available_quantity,
            },
        }), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@book_bp.route("/<int:book_id>", methods=["DELETE"])
@admin_required()
def delete_book(book_id):
    try:
        BookService.delete_book(book_id)
        return jsonify({"message": "Book deleted successfully."}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404
