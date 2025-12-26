"""Database connection for text generator"""

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
    
    def update_generated_text(self, post_id: int, generated_text: str) -> bool:
        """Update post with generated text suggestions"""
        session = self.Session()
        try:
            post = session.query(Post).filter_by(id=post_id).first()
            if not post:
                return False
            
            post.generated_text = generated_text
            session.commit()
            logger.info(f"Updated generated text for post {post_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating generated text for post {post_id}: {e}")
            session.rollback()
            return False
        finally:
            session.close()
