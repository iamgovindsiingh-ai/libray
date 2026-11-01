import re
from sqlalchemy import or_

from app.models import Book, IssueRecord, Member


class AIService:
    @staticmethod
    def ask_librarian(query_text, member=None):
        """Conversational AI book advisor for students."""
        query = (query_text or "").strip().lower()
        if not query:
            return {
                "response": "Hello! I am your AI NexLibrarian. Tell me what subject, topic, exam, or project you're working on, and I'll find the best titles on our shelves for you.",
                "recommendations": [],
            }

        # Tokenize query
        keywords = [w for w in re.findall(r"\w+", query) if len(w) > 2]

        all_books = Book.query.all()
        scored_books = []

        # Intent detection
        is_beginner = any(k in query for k in ["beginner", "basic", "intro", "starting", "easy", "foundation", "freshman"])
        is_advanced = any(k in query for k in ["advanced", "deep", "master", "expert", "complex", "research", "final year"])
        is_exam = any(k in query for k in ["exam", "semester", "syllabus", "midterm", "quiz", "test", "gate", "interview"])
        is_project = any(k in query for k in ["project", "build", "practical", "mini project", "capstone", "code", "implementation"])

        for book in all_books:
            score = 0
            title_lower = (book.title or "").lower()
            author_lower = (book.author.name if book.author else "").lower()
            cat_lower = (book.category.name if book.category else "").lower()
            desc_lower = (book.description or "").lower()
            tags_lower = (book.tags or "").lower()

            # Exact phrase matches
            if query in title_lower or query in desc_lower:
                score += 15

            # Keyword matching
            for kw in keywords:
                if kw in title_lower:
                    score += 8
                if kw in tags_lower:
                    score += 6
                if kw in cat_lower:
                    score += 5
                if kw in desc_lower:
                    score += 3
                if kw in author_lower:
                    score += 4

            # Intent adjustments
            if is_beginner and book.difficulty_level and book.difficulty_level.lower() in ["beginner", "introductory"]:
                score += 5
            if is_advanced and book.difficulty_level and book.difficulty_level.lower() in ["advanced", "expert"]:
                score += 5
            if is_exam and ("guide" in title_lower or "concepts" in desc_lower or "fundamentals" in title_lower):
                score += 4
            if is_project and ("practical" in desc_lower or "hands-on" in desc_lower or "cookbook" in title_lower or "programming" in cat_lower):
                score += 5

            # Department synergy
            if member and member.department:
                dept = member.department.lower()
                if "computer" in dept or "cse" in dept or "it" in dept:
                    if any(c in cat_lower for c in ["computer", "programming", "software", "tech", "data", "ai", "algorithm"]):
                        score += 3
                elif "mechanical" in dept or "mech" in dept:
                    if any(c in cat_lower for c in ["mechanical", "physics", "thermo", "engineering"]):
                        score += 3
                elif "electric" in dept or "ece" in dept:
                    if any(c in cat_lower for c in ["electronic", "circuit", "digital", "electrical"]):
                        score += 3

            if score > 0:
                scored_books.append((score, book))

        scored_books.sort(key=lambda x: x[0], reverse=True)
        top_matches = [b for _, b in scored_books[:5]]

        # Fallback if no direct keyword match
        if not top_matches:
            top_matches = Book.query.filter(Book.available_quantity > 0).order_by(Book.title).limit(3).all()
            response_text = (
                f"I couldn't find an exact keyword match for '{query_text}', but here are some highly recommended "
                "core reference titles available right now in our catalog."
            )
        else:
            reasons = []
            if is_beginner:
                reasons.append("beginner-friendly resources")
            elif is_advanced:
                reasons.append("in-depth masteries")
            if is_exam:
                reasons.append("exam preparation guides")
            if is_project:
                reasons.append("hands-on project implementation books")
            
            reason_str = f" emphasizing {', '.join(reasons)}" if reasons else ""
            response_text = (
                f"I found {len(top_matches)} great match{'es' if len(top_matches) > 1 else ''} for your inquiry '{query_text}'{reason_str}. "
                "Here are my top recommendations with their shelf coordinates:"
            )

        return {
            "query": query_text,
            "response": response_text,
            "recommendations": [
                {
                    "id": b.id,
                    "title": b.title,
                    "author": b.author.name if b.author else "Unknown",
                    "category": b.category.name if b.category else "General",
                    "available_quantity": b.available_quantity,
                    "shelf_location": b.shelf_location or "Zone A · Rack 01",
                    "difficulty_level": b.difficulty_level or "Intermediate",
                    "accent_color": b.accent_color or "#3b82f6",
                    "summary": b.summary or b.description or "Comprehensive study material.",
                    "tags": [t.strip() for t in (b.tags or "").split(",") if t.strip()],
                }
                for b in top_matches
            ],
        }

    @staticmethod
    def get_smart_blurb(book_id):
        """Generate smart takeaways, difficulty level, and study prerequisites for a book."""
        book = Book.query.get(book_id)
        if not book:
            return None

        # Generate intelligent synopsis & key concepts if not stored
        takeaways = []
        if book.key_takeaways:
            takeaways = [t.strip() for t in book.key_takeaways.split(";") if t.strip()]
        else:
            cat = book.category.name if book.category else "General Study"
            takeaways = [
                f"Core foundations of {cat} with applied case studies",
                "Step-by-step analytical problem solving techniques",
                "Industry best practices and university syllabus alignment",
                "Includes review questions and hands-on exercises",
            ]

        summary = book.summary or book.description or (
            f"An essential academic reference on {book.title} authored by {book.author.name if book.author else 'distinguished faculty'}, "
            "designed for conceptual clarity and deep domain mastery."
        )

        return {
            "book_id": book.id,
            "title": book.title,
            "author": book.author.name if book.author else None,
            "category": book.category.name if book.category else None,
            "difficulty_level": book.difficulty_level or "Intermediate",
            "shelf_location": book.shelf_location or "Zone A · Rack 01 · Shelf 1",
            "summary": summary,
            "key_takeaways": takeaways,
            "estimated_read_time": "6 - 8 hours",
            "prerequisites": "Basic understanding of " + (book.category.name if book.category else "the subject"),
        }

    @staticmethod
    def get_reading_radar(member):
        """Recommend books based on student department & past borrowing history."""
        if not member:
            return []

        # Find categories of books previously borrowed
        past_issues = IssueRecord.query.filter_by(member_id=member.id).all()
        borrowed_book_ids = [i.book_id for i in past_issues]
        borrowed_categories = set(i.book.category_id for i in past_issues if i.book and i.book.category_id)

        query = Book.query.filter(Book.available_quantity > 0)
        if borrowed_book_ids:
            query = query.filter(~Book.id.in_(borrowed_book_ids))

        # Prefer books in same categories or department keywords
        candidates = query.all()
        ranked = []

        dept_lower = (member.department or "").lower()
        for b in candidates:
            score = 0
            if b.category_id in borrowed_categories:
                score += 5
            cat_lower = (b.category.name if b.category else "").lower()
            if "cs" in dept_lower or "computer" in dept_lower:
                if any(c in cat_lower for c in ["computer", "programming", "software", "data", "algorithm"]):
                    score += 4
            elif "mech" in dept_lower:
                if any(c in cat_lower for c in ["mech", "physics", "design"]):
                    score += 4
            elif "ee" in dept_lower or "ec" in dept_lower:
                if any(c in cat_lower for c in ["elect", "circuit"]):
                    score += 4
            ranked.append((score, b))

        ranked.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "id": b.id,
                "title": b.title,
                "author": b.author.name if b.author else "Unknown",
                "category": b.category.name if b.category else "General",
                "shelf_location": b.shelf_location or "Zone A · Rack 01",
                "difficulty_level": b.difficulty_level or "Intermediate",
                "accent_color": b.accent_color or "#3b82f6",
                "available_quantity": b.available_quantity,
            }
            for _, b in ranked[:6]
        ]

