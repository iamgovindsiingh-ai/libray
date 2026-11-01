import os
from flask import Blueprint, current_app, render_template, send_from_directory

ui_bp = Blueprint("ui_bp", __name__)


def _get_react_dist():
    """Return path to compiled production React SPA."""
    return os.path.join(current_app.root_path, "static", "react")


@ui_bp.route("/assets/<path:filename>")
def react_assets(filename):
    """Serve React bundled CSS, JS, and font chunks."""
    react_dir = _get_react_dist()
    assets_dir = os.path.join(react_dir, "assets")
    if os.path.exists(os.path.join(assets_dir, filename)):
        return send_from_directory(assets_dir, filename)
    return ("Asset not found", 404)


@ui_bp.route("/vite.svg")
def vite_icon():
    react_dir = _get_react_dist()
    if os.path.exists(os.path.join(react_dir, "vite.svg")):
        return send_from_directory(react_dir, "vite.svg")
    return ("Not Found", 404)


@ui_bp.route("/", defaults={"path": ""})
@ui_bp.route("/<path:path>")
def serve_spa(path):
    """Serve modern React SPA for all browser routes with fallback to templates."""
    # Do not intercept API or static uploads
    if path.startswith("api") or path.startswith("static"):
        return ("Not Found", 404)

    react_dir = _get_react_dist()
    index_file = os.path.join(react_dir, "index.html")

    # If modern React build exists, serve it
    if os.path.exists(index_file):
        return send_from_directory(react_dir, "index.html")

    # Fallback to legacy Jinja templates if React dist is missing
    clean_path = path.strip("/")
    if clean_path in ["", "login"]:
        return render_template("auth/login.html")
    if clean_path == "register":
        return render_template("auth/register.html")
    if clean_path == "admin":
        return render_template("admin/dashboard.html")
    if clean_path == "student":
        return render_template("student/dashboard.html")
    if clean_path == "contact":
        return render_template("public/contact.html")

    return render_template("auth/login.html")
