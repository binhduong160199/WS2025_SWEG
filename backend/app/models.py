"""Data models and schemas for the REST API"""
from typing import Optional
from dataclasses import dataclass
import base64
import json


@dataclass
class PostCreate:
    """Schema for creating a new post"""
    user: str
    text: str
    image: Optional[str] = None  # Base64 encoded image data

    def validate(self) -> tuple[bool, Optional[str]]:
        if not self.user or not self.user.strip():
            return False, "User field is required and cannot be empty"

        if not self.text or not self.text.strip():
            return False, "Text field is required and cannot be empty"

        if len(self.user) > 50:
            return False, "Username cannot exceed 50 characters"

        if len(self.text) > 500:
            return False, "Post text cannot exceed 500 characters"

        if self.image:
            try:
                base64.b64decode(self.image)
            except Exception:
                return False, "Invalid base64 image data"

        return True, None

    def get_image_bytes(self) -> Optional[bytes]:
        """Convert base64 image to bytes"""
        if self.image:
            return base64.b64decode(self.image)
        return None


# ======================================================
# Full post response (detail view)
# ======================================================
@dataclass
class PostResponse:
    """Schema for post response (full post)"""
    id: int
    user: str
    text: str
    image: Optional[str]        # full-size base64
    thumbnail: Optional[str]    # thumbnail base64
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    generated_text: Optional[str] = None
    processing_status: str = 'pending'
    created_at: str = None

    @classmethod
    def from_db(cls, post_data: dict) -> 'PostResponse':
        image_b64 = None
        thumb_b64 = None

        if post_data.get('image'):
            image_b64 = base64.b64encode(post_data['image']).decode('utf-8')

        if post_data.get('image_thumb'):
            thumb_b64 = base64.b64encode(post_data['image_thumb']).decode('utf-8')

        return cls(
            id=post_data['id'],
            user=post_data['user'],
            text=post_data['text'],
            image=image_b64,
            thumbnail=thumb_b64,
            sentiment_score=post_data.get('sentiment_score'),
            sentiment_label=post_data.get('sentiment_label'),
            generated_text=post_data.get('generated_text'),
            processing_status=post_data.get('processing_status', 'pending'),
            created_at=post_data['created_at']
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user': self.user,
            'text': self.text,
            'image': self.image,
            'thumbnail': self.thumbnail,
            'sentiment_score': self.sentiment_score,
            'sentiment_label': self.sentiment_label,
            'generated_text': self.generated_text,
            'processing_status': self.processing_status,
            'created_at': self.created_at
        }


# ======================================================
# Post list response (feed / overview)
# ======================================================
@dataclass
class PostListResponse:
    """Schema for post list response (feed)"""
    id: int
    user: str
    text: str
    created_at: str
    has_image: bool = False
    has_thumbnail: bool = False
    thumbnail: Optional[str] = None
    sentiment_label: Optional[str] = None
    sentiment_score: Optional[float] = None
    processing_status: str = 'pending'

    @classmethod
    def from_db(cls, post_data: dict) -> 'PostListResponse':
        thumb_b64 = None

        if post_data.get('image_thumb'):
            thumb_b64 = base64.b64encode(
                post_data['image_thumb']
            ).decode('utf-8')

        return cls(
            id=post_data['id'],
            user=post_data['user'],
            text=post_data['text'],
            created_at=post_data['created_at'],
            has_image=post_data.get('image') is not None,
            has_thumbnail=post_data.get('image_thumb') is not None,
            thumbnail=thumb_b64,
            sentiment_label=post_data.get('sentiment_label'),
            sentiment_score=post_data.get('sentiment_score'),
            processing_status=post_data.get('processing_status', 'pending')
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user': self.user,
            'text': self.text,
            'created_at': self.created_at,
            'has_image': self.has_image,
            'has_thumbnail': self.has_thumbnail,
            'image_thumb': self.thumbnail,
            'sentiment_label': self.sentiment_label,
            'sentiment_score': self.sentiment_score,
            'processing_status': self.processing_status
        }