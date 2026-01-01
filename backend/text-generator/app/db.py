import os
from typing import Optional
from sqlalchemy import create_engine, text


def _get_engine():
    db_url = os.environ["DATABASE_URL"]
    return create_engine(db_url)


def get_post_text(post_id: int) -> Optional[str]:
    """Get post text by ID"""
    engine = _get_engine()
    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT text FROM posts WHERE id = :id"),
            {"id": post_id}
        ).fetchone()

    if not row or row[0] is None:
        return None
    return row[0]


def save_generated_text(post_id: int, generated_text: str) -> None:
    """Save generated text suggestion for a post"""
    engine = _get_engine()
    
    # First ensure the table exists
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS text_suggestions (
                id SERIAL PRIMARY KEY,
                post_id INTEGER REFERENCES posts(id),
                generated_text TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """))
        
        # Insert the suggestion
        conn.execute(
            text("INSERT INTO text_suggestions (post_id, generated_text) VALUES (:post_id, :text)"),
            {"post_id": post_id, "text": generated_text}
        )
