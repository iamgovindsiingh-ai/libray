from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import Member, User


class AuthService:
    @staticmethod
    def register_user(data, allow_admin_role=False):
        email = (data.get("email") or "").strip().lower()
        password = data.get("password")
        full_name = (data.get("full_name") or "").strip()

        if not email or not password or not full_name:
            raise ValueError("Email, password and full name are required.")

        # Security lock: Public self-registration ALWAYS creates a student.
        # Only internal seeding or elevated calls can create an admin.
        if allow_admin_role and (data.get("role") or "").strip().lower() == "admin":
            role = "admin"
        else:
            role = "student"

        if User.query.filter_by(email=email).first():
            raise ValueError("User with this email already exists.")

        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            role=role,
            is_active=True,
        )
        db.session.add(user)
        db.session.commit()

        # Every student account needs a member profile before it can borrow books.
        if user.role == "student":
            member = Member(
                user_id=user.id,
                student_id=f"STU-{user.id:04d}",
                email=user.email,
                is_active=True,
            )
            db.session.add(member)
            db.session.commit()
        return user

    @staticmethod
    def login_user(data):
        email = (data.get("email") or "").strip().lower()
        password = data.get("password")

        if not email or not password:
            raise ValueError("Email and password are required.")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            raise ValueError("Invalid email or password.")

        if not user.is_active:
            raise ValueError("User account is inactive.")

        return user
