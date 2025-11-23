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
        """
        Validate post creation data
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not self.user or not self.user.strip():
            return False, "User field is required and cannot be empty"
        
        if not self.text or not self.text.strip():
            return False, "Text field is required and cannot be empty"
        
        if len(self.user) > 50:
            return False, "Username cannot exceed 50 characters"
        
        if len(self.text) > 500:
            return False, "Post text cannot exceed 500 characters"
        
        # Validate base64 image if provided
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


@dataclass
class PostResponse:
    """Schema for post response"""
    id: int
    user: str
    text: str
    image: Optional[str]  # Base64 encoded or None
    created_at: str
    
    @classmethod
    def from_db(cls, post_data: dict) -> 'PostResponse':
        """
        Create PostResponse from database row
        
        Args:
            post_data: Dictionary from database query
        
        Returns:
            PostResponse instance
        """
        image_b64 = None
        if post_data.get('image'):
            image_b64 = base64.b64encode(post_data['image']).decode('utf-8')
        
        return cls(
            id=post_data['id'],
            user=post_data['user'],
            text=post_data['text'],
            image=image_b64,
            created_at=post_data['created_at']
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'user': self.user,
            'text': self.text,
            'image': self.image,
            'created_at': self.created_at
        }


@dataclass
class PostListResponse:
    """Schema for post list response (without image data)"""
    id: int
    user: str
    text: str
    created_at: str
    has_image: bool = False
    
    @classmethod
    def from_db(cls, post_data: dict) -> 'PostListResponse':
        """
        Create PostListResponse from database row
        
        Args:
            post_data: Dictionary from database query
        
        Returns:
            PostListResponse instance
        """
        return cls(
            id=post_data['id'],
            user=post_data['user'],
            text=post_data['text'],
            created_at=post_data['created_at'],
            has_image='image' in post_data and post_data['image'] is not None
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'user': self.user,
            'text': self.text,
            'created_at': self.created_at,
            'has_image': self.has_image
        }
