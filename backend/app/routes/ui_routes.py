from flask import Blueprint, render_template


ui_bp = Blueprint("ui_bp", __name__)


@ui_bp.route("/")
def index():
    return render_template("auth/login.html")


@ui_bp.route("/login")
def login_page():
    return render_template("auth/login.html")


@ui_bp.route("/register")
def register_page():
    return render_template("auth/register.html")


@ui_bp.route("/admin")
def admin_dashboard():
    return render_template("admin/dashboard.html")


@ui_bp.route("/student")
def student_dashboard():
    return render_template("student/dashboard.html")


@ui_bp.route("/contact")
def contact_page():
    return render_template("public/contact.html")
