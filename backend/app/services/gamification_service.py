from datetime import datetime
from sqlalchemy import func

from app import db
from app.models import (
    Book,
    BookReview,
    Fine,
    IssueRecord,
    Member,
    ReadingNote,
    StudentBadge,
)
from app.services.notification_service import NotificationService


BADGE_DEFINITIONS = {
    "FIRST_BORROW": {
        "title": "Scholar's First Step",
        "description": "Issued your very first library book.",
        "icon": "fa-award",
        "category": "milestone",
    },
    "PUNCTUAL_SCHOLAR": {
        "title": "Punctual Scholar",
        "description": "Returned books promptly on time without fines.",
        "icon": "fa-clock",
        "category": "discipline",
    },
    "BOOKWORM": {
        "title": "Bibliophile Master",
        "description": "Read and borrowed 5 or more titles.",
        "icon": "fa-book-open-reader",
        "category": "volume",
    },
    "LITERARY_CRITIC": {
        "title": "Literary Critic",
        "description": "Submitted a verified reader review and rating.",
        "icon": "fa-feather",
        "category": "community",
    },
    "STUDY_JOURNALIST": {
        "title": "Study Journalist",
        "description": "Logged key takeaways and quotes in your reading journal.",
        "icon": "fa-pen-nib",
        "category": "scholarship",
    },
    "KNOWLEDGE_EXPLORER": {
        "title": "Knowledge Explorer",
        "description": "Explored books across multiple academic categories.",
        "icon": "fa-compass",
        "category": "breadth",
    },
}


class GamificationService:
    @staticmethod
    def unlock_badge(member_id, badge_code):
        """Unlock a badge for a member if not already awarded."""
        if badge_code not in BADGE_DEFINITIONS:
            return None

        existing = StudentBadge.query.filter_by(member_id=member_id, badge_code=badge_code).first()
        if existing:
            return None

        defn = BADGE_DEFINITIONS[badge_code]
        badge = StudentBadge(
            member_id=member_id,
            badge_code=badge_code,
            title=defn["title"],
            description=defn["description"],
            icon=defn["icon"],
            category=defn["category"],
        )
        db.session.add(badge)
        db.session.commit()

        # Send in-app notification
        NotificationService.create_notification(
            member_id=member_id,
            title=f"Badge Unlocked: {defn['title']}! 🏅",
            message=defn["description"],
            notif_type="badge_unlocked",
        )
        return badge

    @staticmethod
    def evaluate_member_badges(member_id):
        """Check all possible badge conditions and unlock earned badges."""
        member = Member.query.get(member_id)
        if not member:
            return []

        all_issues = IssueRecord.query.filter_by(member_id=member_id).all()
        returned_issues = [i for i in all_issues if i.status == "returned"]
        unlocked = []

        # 1. First Borrow
        if len(all_issues) >= 1:
            b = GamificationService.unlock_badge(member_id, "FIRST_BORROW")
            if b:
                unlocked.append(b)

        # 2. Bookworm (5+ issues)
        distinct_books = set(i.book_id for i in all_issues)
        if len(distinct_books) >= 5 or len(all_issues) >= 5:
            b = GamificationService.unlock_badge(member_id, "BOOKWORM")
            if b:
                unlocked.append(b)

        # 3. Punctual Scholar (at least 2 returned books with zero overdue)
        on_time_returns = [i for i in returned_issues if i.return_date and i.return_date <= i.due_date]
        if len(on_time_returns) >= 2:
            b = GamificationService.unlock_badge(member_id, "PUNCTUAL_SCHOLAR")
            if b:
                unlocked.append(b)

        # 4. Literary Critic (reviews posted)
        review_count = BookReview.query.filter_by(member_id=member_id).count()
        if review_count >= 1:
            b = GamificationService.unlock_badge(member_id, "LITERARY_CRITIC")
            if b:
                unlocked.append(b)

        # 5. Study Journalist (notes logged)
        notes_count = ReadingNote.query.filter_by(member_id=member_id).count()
        if notes_count >= 1:
            b = GamificationService.unlock_badge(member_id, "STUDY_JOURNALIST")
            if b:
                unlocked.append(b)

        # 6. Knowledge Explorer (multiple categories)
        categories = set(i.book.category_id for i in all_issues if i.book and i.book.category_id)
        if len(categories) >= 2:
            b = GamificationService.unlock_badge(member_id, "KNOWLEDGE_EXPLORER")
            if b:
                unlocked.append(b)

        return unlocked

    @staticmethod
    def get_member_gamification_profile(member_id):
        """Compute score, rank, reading streak, badges, and department leaderboard."""
        GamificationService.evaluate_member_badges(member_id)

        member = Member.query.get(member_id)
        if not member:
            return {}

        badges = StudentBadge.query.filter_by(member_id=member_id).all()
        all_issues = IssueRecord.query.filter_by(member_id=member_id).all()
        returned_issues = [i for i in all_issues if i.status == "returned"]
        notes_count = ReadingNote.query.filter_by(member_id=member_id).count()
        reviews_count = BookReview.query.filter_by(member_id=member_id).count()

        # Score Formula: 50 pts per completed loan + 20 pts per review + 15 pts per journal note + 100 pts per badge
        reading_score = (
            (len(returned_issues) * 50)
            + (len(all_issues) * 20)
            + (reviews_count * 25)
            + (notes_count * 15)
            + (len(badges) * 100)
        )

        # Title / Rank
        if reading_score >= 800:
            rank_title = "Grand Research Fellow"
            rank_tier = "Diamond"
        elif reading_score >= 450:
            rank_title = "Master Bibliophile"
            rank_tier = "Gold"
        elif reading_score >= 200:
            rank_title = "Scholar Apprentice"
            rank_tier = "Silver"
        else:
            rank_title = "Freshman Reader"
            rank_tier = "Bronze"

        # Reading Streak (simulated active days / borrowed cycle)
        streak_days = max(len(all_issues) * 3, 1)

        # Department Leaderboard
        dept_leaderboard = (
            db.session.query(
                Member.department,
                func.count(IssueRecord.id).label("total_loans"),
                func.count(func.distinct(Member.id)).label("active_students"),
            )
            .join(IssueRecord, IssueRecord.member_id == Member.id)
            .filter(Member.department != None)
            .group_by(Member.department)
            .order_by(func.count(IssueRecord.id).desc())
            .limit(5)
            .all()
        )

        # Student Leaderboard
        student_leaderboard = (
            db.session.query(
                Member.id,
                Member.student_id,
                Member.department,
                func.count(IssueRecord.id).label("loans_count"),
            )
            .join(IssueRecord, IssueRecord.member_id == Member.id)
            .group_by(Member.id)
            .order_by(func.count(IssueRecord.id).desc())
            .limit(5)
            .all()
        )

        top_students = []
        for s in student_leaderboard:
            m = Member.query.get(s.id)
            top_students.append({
                "student_id": s.student_id,
                "name": m.user.full_name if m and m.user else "Student",
                "department": s.department or "CSE",
                "score": s.loans_count * 50 + 100,
                "books_borrowed": s.loans_count,
            })

        return {
            "reading_score": reading_score,
            "rank_title": rank_title,
            "rank_tier": rank_tier,
            "streak_days": streak_days,
            "badges_count": len(badges),
            "badges": [
                {
                    "code": b.badge_code,
                    "title": b.title,
                    "description": b.description,
                    "icon": b.icon,
                    "category": b.category,
                    "unlocked_at": b.created_at.strftime("%b %d, %Y"),
                }
                for b in badges
            ],
            "all_available_badges": [
                {
                    "code": code,
                    "title": data["title"],
                    "description": data["description"],
                    "icon": data["icon"],
                    "unlocked": any(b.badge_code == code for b in badges),
                }
                for code, data in BADGE_DEFINITIONS.items()
            ],
            "department_leaderboard": [
                {
                    "department": d.department or "General",
                    "total_loans": d.total_loans,
                    "active_students": d.active_students,
                }
                for d in dept_leaderboard
            ],
            "top_students": top_students,
        }

