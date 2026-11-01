from app import db
from app.models import Author, Book, Category


class BookService:
    @staticmethod
    def get_all_books():
        return Book.query.order_by(Book.created_at.desc()).all()

    @staticmethod
    def get_book_by_id(book_id):
        return Book.query.get(book_id)

    @staticmethod
    def create_book(data):
        isbn = (data.get("isbn") or "").strip()
        title = (data.get("title") or "").strip()
        author_name = (data.get("author_name") or "").strip()
        category_name = (data.get("category_name") or "").strip()
        publisher = (data.get("publisher") or "").strip()
        publication_year = data.get("publication_year")
        quantity = data.get("quantity")

        if not isbn or not title or not author_name or not category_name:
            raise ValueError("ISBN, title, author name and category are required.")

        if quantity is None or int(quantity) <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if Book.query.filter_by(isbn=isbn).first():
            raise ValueError("A book with this ISBN already exists.")

        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.flush()

        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.flush()

        # Auto generate shelf location if omitted
        shelf_loc = data.get("shelf_location")
        if not shelf_loc:
            shelf_loc = "Zone A · Rack 01 · Shelf 1"

        book = Book(
            isbn=isbn,
            title=title,
            author_id=author.id,
            category_id=category.id,
            publisher=publisher,
            publication_year=int(publication_year) if publication_year is not None else None,
            quantity=int(quantity),
            available_quantity=int(quantity),
            description=data.get("description"),
            shelf_location=shelf_loc,
            barcode=data.get("barcode") or isbn,
            accent_color=data.get("accent_color") or "#3b82f6",
            difficulty_level=data.get("difficulty_level") or "Intermediate",
            summary=data.get("summary"),
            key_takeaways=data.get("key_takeaways"),
            tags=data.get("tags"),
        )
        db.session.add(book)
        db.session.commit()
        return book

    @staticmethod
    def update_book(book_id, data):
        book = Book.query.get(book_id)
        if not book:
            raise ValueError("Book not found.")

        if "isbn" in data:
            isbn = (data.get("isbn") or "").strip()
            if not isbn:
                raise ValueError("ISBN is required.")
            if Book.query.filter(Book.isbn == isbn, Book.id != book_id).first():
                raise ValueError("Another book with this ISBN already exists.")
            book.isbn = isbn

        if "title" in data:
            title = (data.get("title") or "").strip()
            if not title:
                raise ValueError("Title is required.")
            book.title = title

        if "author_name" in data:
            author_name = (data.get("author_name") or "").strip()
            if not author_name:
                raise ValueError("Author name is required.")
            author = Author.query.filter_by(name=author_name).first()
            if not author:
                author = Author(name=author_name)
                db.session.add(author)
                db.session.flush()
            book.author_id = author.id

        if "category_name" in data:
            category_name = (data.get("category_name") or "").strip()
            if not category_name:
                raise ValueError("Category is required.")
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
                db.session.flush()
            book.category_id = category.id

        if "publisher" in data:
            book.publisher = (data.get("publisher") or "").strip()

        if "publication_year" in data:
            year = data.get("publication_year")
            book.publication_year = int(year) if year is not None else None

        if "quantity" in data:
            quantity = int(data.get("quantity"))
            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")
            delta = quantity - book.quantity
            book.quantity = quantity
            book.available_quantity += delta
            if book.available_quantity < 0:
                book.available_quantity = 0

        for attr in ["description", "shelf_location", "barcode", "accent_color", "difficulty_level", "summary", "key_takeaways", "tags"]:
            if attr in data:
                setattr(book, attr, data.get(attr))

        db.session.commit()
        return book

    @staticmethod
    def delete_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            raise ValueError("Book not found.")

        db.session.delete(book)
        db.session.commit()
        return True

    @staticmethod
    def search_books(query="", category="", difficulty="", available_only=False):
        q = (query or "").strip()
        cat = (category or "").strip()
        diff = (difficulty or "").strip()

        db_query = (
            Book.query.join(Author, Book.author_id == Author.id, isouter=True)
            .join(Category, Book.category_id == Category.id, isouter=True)
        )

        if q:
            db_query = db_query.filter(
                Book.title.ilike(f"%{q}%")
                | Book.isbn.ilike(f"%{q}%")
                | Book.shelf_location.ilike(f"%{q}%")
                | Book.tags.ilike(f"%{q}%")
                | Author.name.ilike(f"%{q}%")
                | Category.name.ilike(f"%{q}%")
            )

        if cat:
            db_query = db_query.filter(Category.name.ilike(f"%{cat}%"))

        if diff:
            db_query = db_query.filter(Book.difficulty_level.ilike(f"%{diff}%"))

        if available_only:
            db_query = db_query.filter(Book.available_quantity > 0)

        return db_query.order_by(Book.title).all()
