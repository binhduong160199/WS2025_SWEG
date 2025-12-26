"""Database manager for social media posts"""

from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, TIMESTAMP, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from typing import Optional, Dict, List, Any

Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String, nullable=False)
    text = Column(Text, nullable=False)

    # full-size image (existing)
    image = Column(LargeBinary)

    # NEW: reduced-size / thumbnail image
    image_thumb = Column(LargeBinary)

    # ML Features
    sentiment_score = Column(Float, nullable=True)  # 0.0-1.0 for positive sentiment
    sentiment_label = Column(String, nullable=True)  # 'POSITIVE', 'NEGATIVE'
    generated_text = Column(Text, nullable=True)  # Generated text suggestions
    processing_status = Column(String, default='pending')  # pending, processing, completed, failed

    created_at = Column(TIMESTAMP, server_default=func.now())


class SocialMediaDB:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def add_post(self, user: str, text: str, image_path: Optional[str] = None) -> int:
        session = self.Session()
        image_data = None
        if image_path:
            with open(image_path, 'rb') as f:
                image_data = f.read()

        post = Post(user=user, text=text, image=image_data, image_thumb=None)
        session.add(post)
        session.commit()
        post_id = post.id
        session.close()
        return post_id

    def add_post_with_image_data(self, user: str, text: str, image_data: Optional[bytes] = None) -> int:
        session = self.Session()
        post = Post(user=user, text=text, image=image_data, image_thumb=None)
        session.add(post)
        session.commit()
        post_id = post.id
        session.close()
        return post_id

    def get_post_by_id(self, post_id: int) -> Optional[Dict[str, Any]]:
        session = self.Session()
        post = session.query(Post).filter_by(id=post_id).first()
        session.close()
        if post:
            return {
                'id': post.id,
                'user': post.user,
                'text': post.text,
                'image': post.image,
                'image_thumb': post.image_thumb,
                'sentiment_score': post.sentiment_score,
                'sentiment_label': post.sentiment_label,
                'generated_text': post.generated_text,
                'processing_status': post.processing_status,
                'created_at': post.created_at
            }
        return None

    def get_latest_post(self) -> Optional[Dict[str, Any]]:
        session = self.Session()
        post = session.query(Post).order_by(Post.id.desc()).first()
        session.close()
        if post:
            return {
                'id': post.id,
                'user': post.user,
                'text': post.text,
                'image': post.image,
                'image_thumb': post.image_thumb,
                'sentiment_score': post.sentiment_score,
                'sentiment_label': post.sentiment_label,
                'generated_text': post.generated_text,
                'processing_status': post.processing_status,
                'created_at': post.created_at
            }
        return None

    def get_all_posts(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        session = self.Session()
        query = session.query(Post).order_by(Post.id.desc())
        if limit:
            query = query.limit(limit)

        posts = [
            {
                'id': post.id,
                'user': post.user,
                'text': post.text,
                'created_at': post.created_at,
                'image': post.image,
                'image_thumb': post.image_thumb,
                'sentiment_score': post.sentiment_score,
                'sentiment_label': post.sentiment_label,
                'generated_text': post.generated_text,
                'processing_status': post.processing_status
            }
            for post in query.all()
        ]
        session.close()
        return posts

    def search_posts(self, query: str) -> List[Dict[str, Any]]:
        session = self.Session()
        posts = session.query(Post).filter(
            (Post.text.ilike(f'%{query}%')) | (Post.user.ilike(f'%{query}%'))
        ).order_by(Post.id.desc()).all()

        result = [
            {
                'id': post.id,
                'user': post.user,
                'text': post.text,
                'created_at': post.created_at,
                'image': post.image,
                'image_thumb': post.image_thumb,
                'sentiment_score': post.sentiment_score,
                'sentiment_label': post.sentiment_label,
                'generated_text': post.generated_text,
                'processing_status': post.processing_status
            }
            for post in posts
        ]
        session.close()
        return result

    def delete_all_posts(self) -> None:
        session = self.Session()
        session.query(Post).delete()
        session.commit()
        session.close()

    def get_full_image_by_post_id(self, post_id: int) -> Optional[bytes]:
        session = self.Session()
        post = session.query(Post).filter_by(id=post_id).first()
        session.close()

        if post:
            return post.image
        return None        

    def update_post_thumbnail(self, post_id: int, thumbnail_data: bytes) -> bool:
        session = self.Session()
        post = session.query(Post).filter_by(id=post_id).first()

        if not post:
            session.close()
            return False

        post.image_thumb = thumbnail_data
        session.commit()
        session.close()
        return True
    
    def update_post_sentiment(self, post_id: int, sentiment_score: float, sentiment_label: str) -> bool:
        """Update post with sentiment analysis results"""
        session = self.Session()
        post = session.query(Post).filter_by(id=post_id).first()

        if not post:
            session.close()
            return False

        post.sentiment_score = sentiment_score
        post.sentiment_label = sentiment_label
        post.processing_status = 'completed'
        session.commit()
        session.close()
        return True
    
    def update_post_generated_text(self, post_id: int, generated_text: str) -> bool:
        """Update post with generated text suggestions"""
        session = self.Session()
        post = session.query(Post).filter_by(id=post_id).first()

        if not post:
            session.close()
            return False

        post.generated_text = generated_text
        session.commit()
        session.close()
        return True
    
    def set_post_processing_status(self, post_id: int, status: str) -> bool:
        """Set post processing status"""
        session = self.Session()
        post = session.query(Post).filter_by(id=post_id).first()

        if not post:
            session.close()
            return False

        post.processing_status = status
        session.commit()
        session.close()
        return True