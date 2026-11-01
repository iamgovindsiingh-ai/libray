import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-nexshelf-2026")
    
    # Database Configuration:
    # 1. If DATABASE_URL is provided (Render PostgreSQL, Neon, Supabase, etc.), use it.
    # 2. Render and older clouds supply postgres://, but SQLAlchemy 1.4+ requires postgresql://
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = db_url
    else:
        # Default fallback to SQLite database inside database/ directory
        root_dir = os.path.dirname(basedir) if os.path.basename(basedir) == "backend" else basedir
        db_path = os.path.join(root_dir, "database", "library_management.db")
        
        if not os.path.exists(db_path):
            legacy_instance = os.path.join(root_dir, "instance")
            os.makedirs(legacy_instance, exist_ok=True)
            db_path = os.path.join(legacy_instance, "library_management.db")

        clean_db_path = os.path.abspath(db_path).replace("\\", "/")
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{clean_db_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-key-nexshelf-2026")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    JSON_SORT_KEYS = False
