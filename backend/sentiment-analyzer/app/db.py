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


def update_sentiment(post_id: int, sentiment_label: str, sentiment_score: str) -> None:
    """Update post with sentiment analysis results"""
    engine = _get_engine()
    with engine.begin() as conn:
        conn.execute(
            text("UPDATE posts SET sentiment_label = :label, sentiment_score = :score WHERE id = :id"),
            {"label": sentiment_label, "score": sentiment_score, "id": post_id}
        )
