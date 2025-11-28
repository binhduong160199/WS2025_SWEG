"""Database manager for social media posts"""

from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, TIMESTAMP, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from typing import Optional, Dict, List, Any

Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    image = Column(LargeBinary)
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
        post = Post(user=user, text=text, image=image_data)
        session.add(post)
        session.commit()
        post_id = post.id
        session.close()
        return post_id

    def add_post_with_image_data(self, user: str, text: str, image_data: Optional[bytes] = None) -> int:
        session = self.Session()
        post = Post(user=user, text=text, image=image_data)
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
                'image': post.image
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
                'image': post.image
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
            SELECT id, user, text, created_at, image FROM posts
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
                'created_at': row[3],
                'image': row[4]
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
            SELECT id, user, text, created_at, image FROM posts
            WHERE text LIKE ? OR user LIKE ?
            ORDER BY id DESC
        ''', (search_pattern, search_pattern))

        posts = []
        for row in cursor.fetchall():
            posts.append({
                'id': row[0],
                'user': row[1],
                'text': row[2],
                'created_at': row[3],
                'image': row[4]
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
