from app import db
from app.models import Member, User


class MemberService:
    @staticmethod
    def get_all_members():
        return Member.query.order_by(Member.created_at.desc()).all()

    @staticmethod
    def get_member_by_id(member_id):
        return Member.query.get(member_id)

    @staticmethod
    def create_member(data):
        user_id = data.get("user_id")
        student_id = (data.get("student_id") or "").strip()
        email = (data.get("email") or "").strip().lower()
        phone = (data.get("phone") or "").strip()
        department = (data.get("department") or "").strip()
        year = (data.get("year") or "").strip()
        address = (data.get("address") or "").strip()

        if not student_id or not email:
            raise ValueError("Student ID and email are required.")

        if user_id is not None:
            user = User.query.get(user_id)
            if not user:
                raise ValueError("User not found.")
        else:
            user = User.query.filter_by(email=email).first()
            if not user:
                from werkzeug.security import generate_password_hash
                full_name = (data.get("full_name") or data.get("name") or "Student Scholar").strip()
                password = data.get("password") or "student123"
                user = User(
                    email=email,
                    password_hash=generate_password_hash(password),
                    full_name=full_name,
                    role="student",
                    is_active=True,
                )
                db.session.add(user)
                db.session.commit()

        if Member.query.filter_by(student_id=student_id).first():
            raise ValueError("A member with this student ID already exists.")

        if Member.query.filter_by(email=email).first():
            raise ValueError("A member with this email already exists.")

        member = Member(
            user_id=user.id,
            student_id=student_id,
            email=email,
            phone=phone,
            department=department,
            year=year,
            address=address,
            is_active=True,
        )
        db.session.add(member)
        db.session.commit()
        return member

    @staticmethod
    def update_member(member_id, data):
        member = Member.query.get(member_id)
        if not member:
            raise ValueError("Member not found.")

        if "student_id" in data:
            student_id = (data.get("student_id") or "").strip()
            if not student_id:
                raise ValueError("Student ID is required.")
            if Member.query.filter(Member.student_id == student_id, Member.id != member_id).first():
                raise ValueError("Another member with this student ID already exists.")
            member.student_id = student_id

        if "email" in data:
            email = (data.get("email") or "").strip().lower()
            if not email:
                raise ValueError("Email is required.")
            if Member.query.filter(Member.email == email, Member.id != member_id).first():
                raise ValueError("Another member with this email already exists.")
            member.email = email

        if "phone" in data:
            member.phone = (data.get("phone") or "").strip()

        if "department" in data:
            member.department = (data.get("department") or "").strip()

        if "year" in data:
            member.year = (data.get("year") or "").strip()

        if "address" in data:
            member.address = (data.get("address") or "").strip()

        if "is_active" in data:
            member.is_active = bool(data.get("is_active"))

        db.session.commit()
        return member

    @staticmethod
    def delete_member(member_id):
        member = Member.query.get(member_id)
        if not member:
            raise ValueError("Member not found.")

        active_issues = [i for i in getattr(member, 'issue_records', []) if getattr(i, 'status', '') == 'issued']
        if active_issues:
            raise ValueError(f"Cannot remove member #{member.student_id}. They still have {len(active_issues)} active book loans that must be returned first.")

        db.session.delete(member)
        db.session.commit()
        return True
