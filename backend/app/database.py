"""Database manager for social media posts"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any


class SocialMediaDB:
    """Database manager for social media posts"""
    
    def __init__(self, db_name: str = "social_media.db"):
        """
        Initialize database connection
        
        Args:
            db_name: Name of the SQLite database file
        """
        self.db_name = db_name
        self.init_database()
    
    def init_database(self) -> None:
        """Initialize the database with posts table"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                text TEXT NOT NULL,
                image BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_post(self, user: str, text: str, image_path: Optional[str] = None) -> int:
        """
        Add a new post to the database
        
        Args:
            user: Username of the poster
            text: Text content of the post
            image_path: Path to image file (optional)
        
        Returns:
            int: ID of the inserted post
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        image_data = None
        if image_path and Path(image_path).exists():
            with open(image_path, 'rb') as f:
                image_data = f.read()
        
        cursor.execute('''
            INSERT INTO posts (user, text, image)
            VALUES (?, ?, ?)
        ''', (user, text, image_data))
        
        post_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return post_id
    
    def add_post_with_image_data(self, user: str, text: str, image_data: Optional[bytes] = None) -> int:
        """
        Add a new post to the database with raw image data
        
        Args:
            user: Username of the poster
            text: Text content of the post
            image_data: Raw image data as bytes (optional)
        
        Returns:
            int: ID of the inserted post
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO posts (user, text, image)
            VALUES (?, ?, ?)
        ''', (user, text, image_data))
        
        post_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return post_id
    
    def get_post_by_id(self, post_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific post by ID
        
        Args:
            post_id: ID of the post to retrieve
        
        Returns:
            dict: Dictionary containing post data or None if not found
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user, text, image, created_at
            FROM posts
            WHERE id = ?
        ''', (post_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'user': row[1],
                'text': row[2],
                'image': row[3],
                'created_at': row[4]
            }
        return None
    
    def get_latest_post(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve the latest post from the database
        
        Returns:
            dict: Dictionary containing post data or None if no posts exist
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user, text, image, created_at
            FROM posts
            ORDER BY id DESC
            LIMIT 1
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'user': row[1],
                'text': row[2],
                'image': row[3],
                'created_at': row[4]
            }
        return None
    
    def get_all_posts(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all posts from the database
        
        Args:
            limit: Optional limit on number of posts to return
        
        Returns:
            list: List of dictionaries containing post data
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query = '''
            SELECT id, user, text, created_at
            FROM posts
            ORDER BY id DESC
        '''
        
        if limit:
            query += f' LIMIT {limit}'
        
        cursor.execute(query)
        
        posts = []
        for row in cursor.fetchall():
            posts.append({
                'id': row[0],
                'user': row[1],
                'text': row[2],
                'created_at': row[3]
            })
        
        conn.close()
        return posts
    
    def search_posts(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for posts by text content or username
        
        Args:
            query: Search query string
        
        Returns:
            list: List of matching posts
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        search_pattern = f'%{query}%'
        cursor.execute('''
            SELECT id, user, text, created_at
            FROM posts
            WHERE text LIKE ? OR user LIKE ?
            ORDER BY id DESC
        ''', (search_pattern, search_pattern))
        
        posts = []
        for row in cursor.fetchall():
            posts.append({
                'id': row[0],
                'user': row[1],
                'text': row[2],
                'created_at': row[3]
            })
        
        conn.close()
        return posts
    
    def delete_all_posts(self) -> None:
        """Delete all posts from the database (useful for testing)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM posts')
        conn.commit()
        conn.close()
