from flask import Blueprint, jsonify

from app.services.shelf_service import ShelfService


shelf_bp = Blueprint("shelf_bp", __name__)


@shelf_bp.route("/map", methods=["GET"])
def get_library_map():
    layout = ShelfService.get_library_map_layout()
    return jsonify(layout), 200


@shelf_bp.route("/locate/<int:book_id>", methods=["GET"])
def locate_book(book_id):
    location = ShelfService.locate_book_on_shelf(book_id)
    if not location:
        return jsonify({"error": "Book not found."}), 404
    return jsonify(location), 200

