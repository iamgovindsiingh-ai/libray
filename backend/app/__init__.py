from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

from config import Config


db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        if error.code == 404:
            return jsonify({"error": "Resource not found."}), 404
        if error.code == 405:
            return jsonify({"error": "Method not allowed."}), 405
        return jsonify({"error": error.description or "Request error."}), error.code or 400

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception("Unhandled API exception: %s", error)
        return jsonify({"error": "Internal server error."}), 500

    with app.app_context():
        # Import routes here to avoid circular imports
        from app.routes.ai_routes import ai_bp
        from app.routes.analytics_routes import analytics_bp
        from app.routes.auth_routes import auth_bp
        from app.routes.book_routes import book_bp
        from app.routes.citation_routes import citation_bp
        from app.routes.community_routes import community_bp
        from app.routes.dashboard_routes import dashboard_bp
        from app.routes.fine_routes import fine_bp
        from app.routes.gamification_routes import gamification_bp
        from app.routes.library_routes import library_bp
        from app.routes.member_routes import member_bp
        from app.routes.scanner_routes import scanner_bp
        from app.routes.shelf_routes import shelf_bp
        from app.routes.student_routes import student_bp
        from app.routes.ui_routes import ui_bp

        app.register_blueprint(auth_bp, url_prefix="/api/auth")
        app.register_blueprint(book_bp, url_prefix="/api/books")
        app.register_blueprint(citation_bp, url_prefix="/api")
        app.register_blueprint(member_bp, url_prefix="/api/members")
        app.register_blueprint(library_bp, url_prefix="/api")
        app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
        app.register_blueprint(fine_bp, url_prefix="/api/fines")
        app.register_blueprint(student_bp, url_prefix="/api/student")
        app.register_blueprint(ai_bp, url_prefix="/api/ai")
        app.register_blueprint(shelf_bp, url_prefix="/api/shelf")
        app.register_blueprint(gamification_bp, url_prefix="/api/student")
        app.register_blueprint(community_bp, url_prefix="/api")
        app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
        app.register_blueprint(scanner_bp, url_prefix="/api/scanner")
        app.register_blueprint(ui_bp)

        # Try to create database tables, but don't fail if database is unavailable
        try:
            db.create_all()
            # Safe SQLite migration helper for new columns on existing database
            from sqlalchemy import text
            with db.engine.connect() as conn:
                new_book_cols = [
                    ("shelf_location", "VARCHAR(100) DEFAULT 'Zone A · Rack 01 · Shelf 1'"),
                    ("barcode", "VARCHAR(100)"),
                    ("accent_color", "VARCHAR(30) DEFAULT '#3b82f6'"),
                    ("difficulty_level", "VARCHAR(50) DEFAULT 'Intermediate'"),
                    ("summary", "TEXT"),
                    ("key_takeaways", "TEXT"),
                    ("tags", "VARCHAR(255)"),
                ]
                for col_name, col_type in new_book_cols:
                    try:
                        conn.execute(text(f"ALTER TABLE books ADD COLUMN {col_name} {col_type}"))
                        conn.commit()
                    except Exception:
                        pass

                # Migration for BookRequest contact fields
                new_request_cols = [
                    ("contact_phone", "VARCHAR(30)"),
                    ("contact_whatsapp", "VARCHAR(30)"),
                    ("contact_email", "VARCHAR(150)"),
                    ("urgency", "VARCHAR(20) DEFAULT 'normal'"),
                    ("admin_notes", "TEXT"),
                ]
                for col_name, col_type in new_request_cols:
                    try:
                        conn.execute(text(f"ALTER TABLE book_requests ADD COLUMN {col_name} {col_type}"))
                        conn.commit()
                    except Exception:
                        pass

                # Migration for BookOffer price and image_url fields
                new_offer_cols = [
                    ("price", "FLOAT DEFAULT 0.0"),
                    ("image_url", "VARCHAR(350)"),
                ]
                for col_name, col_type in new_offer_cols:
                    try:
                        conn.execute(text(f"ALTER TABLE book_offers ADD COLUMN {col_name} {col_type}"))
                        conn.commit()
                    except Exception:
                        pass

            import os
            os.makedirs(os.path.join(app.root_path, "static", "uploads"), exist_ok=True)
            app.logger.info("Database tables created and verified.")

            # Auto-seed initial records on fresh cloud deployments (e.g. Render)
            try:
                from app.models import User
                if User.query.filter_by(email="admin@nexshelf.edu").first() is None:
                    try:
                        from database.seed_demo_data import seed_data
                    except ImportError:
                        from seed_demo_data import seed_data
                    seed_data()
                    app.logger.info("Initial cloud database seeded successfully.")
            except Exception as seed_err:
                app.logger.info(f"Auto-seed check note: {seed_err}")
        except Exception as e:
            app.logger.warning(f"Could not initialize database: {e}")
            app.logger.warning("The app will still run, but API routes requiring database will fail.")

    return app
