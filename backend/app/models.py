"""Data models and schemas for the REST API"""
from typing import Optional
from dataclasses import dataclass
import base64


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
    thumbnail: Optional[str]    # NEW: thumbnail base64
    created_at: str

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
            created_at=post_data['created_at']
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user': self.user,
            'text': self.text,
            'image': self.image,
            'thumbnail': self.thumbnail,
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
            thumbnail=thumb_b64
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user': self.user,
            'text': self.text,
            'created_at': self.created_at,
            'has_image': self.has_image,
            'has_thumbnail': self.has_thumbnail,
            'image_thumb': self.thumbnail
        }