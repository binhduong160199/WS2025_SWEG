import os
from typing import Optional

from sqlalchemy import create_engine, text


def _get_engine():
    db_url = os.environ["DATABASE_URL"]
    return create_engine(db_url)


def get_full_image(post_id: int) -> Optional[bytes]:
    engine = _get_engine()
    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT image FROM posts WHERE id = :id"),
            {"id": post_id}
        ).fetchone()

    if not row or row[0] is None:
        return None
    return row[0]


def update_thumbnail(post_id: int, thumb_bytes: bytes) -> None:
    engine = _get_engine()
    with engine.begin() as conn:
        conn.execute(
            text("UPDATE posts SET image_thumb = :thumb WHERE id = :id"),
            {"thumb": thumb_bytes, "id": post_id}
        )