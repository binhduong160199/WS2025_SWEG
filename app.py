import sqlite3
import base64
from datetime import datetime
from pathlib import Path

class SocialMediaDB:
    """Database manager for social media posts"""
    
    def __init__(self, db_name="social_media.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
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
    
    def add_post(self, user, text, image_path=None):
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
    
    def get_latest_post(self):
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
    
    def get_all_posts(self):
        """Retrieve all posts from the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user, text, created_at
            FROM posts
            ORDER BY id DESC
        ''')
        
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


def main():
    """Main function to demonstrate the application"""
    # Initialize database
    db = SocialMediaDB()
    
    # Define 3 posts
    posts_data = [
        {
            'user': 'alice_smith',
            'text': 'Just had an amazing coffee at the new cafe downtown!',
            'image_path': None
        },
        {
            'user': 'bob_jones',
            'text': 'Working on my Python project. Loving the progress so far!',
            'image_path': None
        },
        {
            'user': 'charlie_brown',
            'text': 'Beautiful sunset today! Nature is amazing.',
            'image_path': None
        }
    ]
    
    # Store posts in database
    print("Adding posts to database...")
    for post in posts_data:
        post_id = db.add_post(
            user=post['user'],
            text=post['text'],
            image_path=post['image_path']
        )
        print(f"Added post {post_id} by {post['user']}")
    
    # Retrieve the latest post
    print("\n" + "="*50)
    print("Latest Post:")
    print("="*50)
    latest = db.get_latest_post()
    
    if latest:
        print(f"ID: {latest['id']}")
        print(f"User: {latest['user']}")
        print(f"Text: {latest['text']}")
        print(f"Created: {latest['created_at']}")
        print(f"Has Image: {'Yes' if latest['image'] else 'No'}")
    else:
        print("No posts found in database")
    
    # Display all posts
    print("\n" + "="*50)
    print("All Posts:")
    print("="*50)
    all_posts = db.get_all_posts()
    for post in all_posts:
        print(f"\n[{post['id']}] {post['user']} - {post['created_at']}")
        print(f"  {post['text']}")


if __name__ == "__main__":
    main()