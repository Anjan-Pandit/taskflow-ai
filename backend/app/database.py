from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings


# ==========================================
# DATABASE URL
# ==========================================

DATABASE_URL = settings.DATABASE_URL


# ==========================================
# DATABASE ENGINE
# ==========================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# ==========================================
# DATABASE SESSION
# ==========================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ==========================================
# BASE
# ==========================================

Base = declarative_base()


# ==========================================
# MAKE PROJECT ID OPTIONAL
# ==========================================

def make_project_id_optional():
    """
    Make tasks.project_id nullable in PostgreSQL.

    This is required because existing production
    database schema was created with project_id NOT NULL.
    """

    try:

        with engine.begin() as connection:

            connection.execute(
                text(
                    """
                    ALTER TABLE tasks
                    ALTER COLUMN project_id DROP NOT NULL
                    """
                )
            )

        print(
            "Database migration successful: "
            "tasks.project_id is now optional."
        )

    except Exception as error:

        print(
            "Database migration skipped or failed:",
            error
        )


# ==========================================
# DATABASE DEPENDENCY
# ==========================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()