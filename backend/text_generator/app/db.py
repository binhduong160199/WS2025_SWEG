import os
from typing import Optional
from sqlalchemy import create_engine, text

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(os.environ["DATABASE_URL"])
    return _engine


def init_text_suggestions_table():
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS text_suggestions (
                id SERIAL PRIMARY KEY,
                generated_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))


def save_generated_text(generated_text: str) -> None:
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO text_suggestions (generated_text)
                VALUES (:text)
            """),
            {"text": generated_text}
        )


def get_latest_generated_text() -> Optional[str]:
    engine = get_engine()
    with engine.begin() as conn:
        row = conn.execute(text("""
            SELECT generated_text
            FROM text_suggestions
            ORDER BY created_at DESC
            LIMIT 1
        """)).fetchone()

    return row[0] if row else None