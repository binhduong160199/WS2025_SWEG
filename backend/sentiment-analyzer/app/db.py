"""Database connection for sentiment analyzer"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from typing import Optional, Dict, Any
import logging
import os

logger = logging.getLogger(__name__)
Base = declarative_base()

class Post(Base):
    """Post model (mirror of backend Post model)"""
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    image = Column(None)  # Not used here
    image_thumb = Column(None)  # Not used here
    sentiment_score = Column(Float, nullable=True)
    sentiment_label = Column(String, nullable=True)
    generated_text = Column(Text, nullable=True)
    processing_status = Column(String, default='pending')
    created_at = Column(TIMESTAMP, server_default=func.now())

class DatabaseConnection:
    def __init__(self, database_url: Optional[str] = None):
        """Initialize database connection"""
        db_url = database_url or os.getenv('DATABASE_URL')
        if not db_url:
            raise ValueError("DATABASE_URL environment variable not set")
        
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        logger.info("Database connection initialized")
    
    def get_post_by_id(self, post_id: int) -> Optional[Dict[str, Any]]:
        """Get post by ID"""
        session = self.Session()
        try:
            post = session.query(Post).filter_by(id=post_id).first()
            if post:
                return {
                    'id': post.id,
                    'user': post.user,
                    'text': post.text,
                    'processing_status': post.processing_status
                }
            return None
        finally:
            session.close()
    
    def update_sentiment(self, post_id: int, sentiment_label: str, sentiment_score: float) -> bool:
        """Update post with sentiment analysis results"""
        session = self.Session()
        try:
            post = session.query(Post).filter_by(id=post_id).first()
            if not post:
                return False
            
            post.sentiment_label = sentiment_label
            post.sentiment_score = sentiment_score
            post.processing_status = 'completed'
            session.commit()
            logger.info(f"Updated sentiment for post {post_id}: {sentiment_label} ({sentiment_score})")
            return True
        except Exception as e:
            logger.error(f"Error updating sentiment for post {post_id}: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    def set_processing_status(self, post_id: int, status: str) -> bool:
        """Set post processing status"""
        session = self.Session()
        try:
            post = session.query(Post).filter_by(id=post_id).first()
            if not post:
                return False
            
            post.processing_status = status
            session.commit()
            return True
        except Exception as e:
            logger.error(f"Error setting status for post {post_id}: {e}")
            session.rollback()
            return False
        finally:
            session.close()
