from app import db
from app.models.study_note import StudyNote
from app.models.member import Member


class StudyNoteService:
    @staticmethod
    def create_note(data, member_id=None):
        title = (data.get("title") or "").strip()
        subject = (data.get("subject") or "").strip()
        department = (data.get("department") or "").strip()
        semester = (data.get("semester") or "").strip()
        description = (data.get("description") or "").strip()
        author_name = (data.get("author_name") or "").strip()
        contact_whatsapp = (data.get("contact_whatsapp") or "").strip()
        contact_phone = (data.get("contact_phone") or "").strip()
        contact_email = (data.get("contact_email") or "").strip()
        file_url = (data.get("file_url") or "").strip()
        file_type = (data.get("file_type") or "image").strip()

        if not title:
            raise ValueError("Note title is required.")
        if not subject:
            raise ValueError("Subject / Course code is required.")
        if not file_url:
            raise ValueError("Please upload a picture or file for the notes.")

        if member_id and not author_name:
            member = Member.query.get(member_id)
            if member:
                author_name = member.user.full_name if member.user else "Scholar"
                if not department:
                    department = member.department or ""
                if not contact_email:
                    contact_email = member.email
                if not contact_phone:
                    contact_phone = member.phone or ""

        if not author_name:
            author_name = "Anonymous Scholar"

        note = StudyNote(
            member_id=member_id,
            title=title,
            subject=subject,
            department=department if department else None,
            semester=semester if semester else None,
            description=description if description else None,
            author_name=author_name,
            contact_whatsapp=contact_whatsapp if contact_whatsapp else None,
            contact_phone=contact_phone if contact_phone else None,
            contact_email=contact_email if contact_email else None,
            file_url=file_url,
            file_type=file_type,
            status="active",
        )
        db.session.add(note)
        db.session.commit()
        return note

    @staticmethod
    def get_notes(status="active", subject=None, search=None):
        query = StudyNote.query
        if status and status != "all":
            query = query.filter_by(status=status)
        if subject:
            query = query.filter(StudyNote.subject.ilike(f"%{subject}%"))
        if search:
            query = query.filter(
                (StudyNote.title.ilike(f"%{search}%")) |
                (StudyNote.subject.ilike(f"%{search}%")) |
                (StudyNote.description.ilike(f"%{search}%")) |
                (StudyNote.author_name.ilike(f"%{search}%"))
            )

        notes = query.order_by(StudyNote.created_at.desc()).all()
        return [
            {
                "id": n.id,
                "title": n.title,
                "subject": n.subject,
                "department": n.department or "",
                "semester": n.semester or "",
                "description": n.description or "",
                "author_name": n.author_name,
                "contact_whatsapp": n.contact_whatsapp or "",
                "contact_phone": n.contact_phone or "",
                "contact_email": n.contact_email or "",
                "file_url": n.file_url,
                "file_type": n.file_type,
                "likes_count": n.likes_count,
                "downloads_count": n.downloads_count,
                "status": n.status,
                "created_at": n.created_at.strftime("%b %d, %Y"),
            }
            for n in notes
        ]

    @staticmethod
    def like_note(note_id):
        note = StudyNote.query.get(note_id)
        if not note:
            raise ValueError("Study note not found.")
        note.likes_count += 1
        db.session.commit()
        return note.likes_count

    @staticmethod
    def update_note_status(note_id, new_status):
        note = StudyNote.query.get(note_id)
        if not note:
            raise ValueError("Study note not found.")
        note.status = new_status
        db.session.commit()
        return note

    @staticmethod
    def delete_note(note_id):
        note = StudyNote.query.get(note_id)
        if not note:
            raise ValueError("Study note not found.")
        db.session.delete(note)
        db.session.commit()

