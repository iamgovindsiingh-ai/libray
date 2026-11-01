from datetime import datetime, timedelta

from app.models import Book, IssueRecord


class CitationService:
    @staticmethod
    def generate_citations(book_id):
        """Generates IEEE, APA 7th, MLA 9th, Chicago, and Harvard citations for a book."""
        book = Book.query.get(book_id)
        if not book:
            return None

        author_name = book.author.name if book.author else "Unknown Author"
        title = book.title
        publisher = book.publisher or "Academic Press"
        year = book.publication_year or datetime.utcnow().year
        isbn = book.isbn

        # Author parsing (First Last -> Last, F.)
        parts = author_name.split(" ")
        if len(parts) > 1:
            last_name = parts[-1]
            first_initial = parts[0][0] + "."
            apa_author = f"{last_name}, {first_initial}"
            mla_author = f"{last_name}, {' '.join(parts[:-1])}"
            ieee_author = f"{first_initial} {last_name}"
        else:
            apa_author = author_name
            mla_author = author_name
            ieee_author = author_name

        citations = {
            "book_id": book.id,
            "title": title,
            "author": author_name,
            "year": year,
            "publisher": publisher,
            "isbn": isbn,
            "ieee": f"[1] {ieee_author}, {title}. {publisher}, {year}.",
            "apa": f"{apa_author} ({year}). {title}. {publisher}.",
            "mla": f"{mla_author}. {title}. {publisher}, {year}.",
            "chicago": f"{mla_author}. {year}. {title}. {publisher}.",
            "harvard": f"{apa_author}, {year}. {title}. {publisher}.",
            "bibtex": f"""@book{{{parts[-1].lower() if parts else 'book'}{year},
  title={{{title}}},
  author={{{author_name}}},
  year={{{year}}},
  publisher={{{publisher}}},
  isbn={{{isbn}}}
}}""",
        }
        return citations

    @staticmethod
    def generate_ical_event(issue_id):
        """Generates an iCalendar (.ics) string for importing due date into Google/Apple Calendar."""
        issue = IssueRecord.query.get(issue_id)
        if not issue:
            return None

        book_title = issue.book.title if issue.book else "Library Book"
        due_dt = issue.due_date
        # Create an all-day / morning reminder on the due date
        dtstart = due_dt.strftime("%Y%m%d")
        dtend = (due_dt + timedelta(days=1)).strftime("%Y%m%d")
        created_now = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//NexShelf//Smart Library Management//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:nexshelf-loan-{issue.id}-{dtstart}@nexshelf.edu
DTSTAMP:{created_now}
DTSTART;VALUE=DATE:{dtstart}
DTEND;VALUE=DATE:{dtend}
SUMMARY:📖 Return Book: {book_title} (NexShelf Library)
DESCRIPTION:Reminder to return or renew '{book_title}' at the NexShelf Library circulation desk. Location: {issue.book.shelf_location if issue.book else 'Campus Library'}.
LOCATION:NexShelf University Library Circulation Desk
STATUS:CONFIRMED
BEGIN:VALARM
TRIGGER:-PT12H
ACTION:DISPLAY
DESCRIPTION:Book '{book_title}' is due today at NexShelf Library!
END:VALARM
END:VEVENT
END:VCALENDAR"""
        return ics_content
