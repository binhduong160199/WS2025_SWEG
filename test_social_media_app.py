import unittest
import os
import sqlite3
from app import SocialMediaDB

class TestSocialMediaDB(unittest.TestCase):
    """Test cases for Social Media Database"""
    
    def setUp(self):
        """Set up test database before each test"""
        self.test_db = "test_social_media.db"
        self.db = SocialMediaDB(self.test_db)
    
    def tearDown(self):
        """Clean up test database after each test"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_database_initialization(self):
        """Test that database is created successfully"""
        self.assertTrue(os.path.exists(self.test_db))
        
        # Check if posts table exists
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='posts'
        ''')
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'posts')
    
    def test_add_post_without_image(self):
        """Test adding a post without an image"""
        post_id = self.db.add_post(
            user='test_user',
            text='This is a test post',
            image_path=None
        )
        
        self.assertIsNotNone(post_id)
        self.assertGreater(post_id, 0)
    
    def test_add_multiple_posts(self):
        """Test adding multiple posts"""
        post_id1 = self.db.add_post('user1', 'Post 1')
        post_id2 = self.db.add_post('user2', 'Post 2')
        post_id3 = self.db.add_post('user3', 'Post 3')
        
        self.assertEqual(post_id1, 1)
        self.assertEqual(post_id2, 2)
        self.assertEqual(post_id3, 3)
    
    def test_get_latest_post(self):
        """Test retrieving the latest post"""
        # Add posts
        self.db.add_post('user1', 'First post')
        self.db.add_post('user2', 'Second post')
        self.db.add_post('user3', 'Third post')
        
        # Get latest post
        latest = self.db.get_latest_post()
        
        self.assertIsNotNone(latest)
        self.assertEqual(latest['user'], 'user3')
        self.assertEqual(latest['text'], 'Third post')
        self.assertEqual(latest['id'], 3)
    
    def test_get_latest_post_empty_database(self):
        """Test getting latest post from empty database"""
        latest = self.db.get_latest_post()
        self.assertIsNone(latest)
    
    def test_get_all_posts(self):
        """Test retrieving all posts"""
        # Add posts
        self.db.add_post('alice', 'Hello world')
        self.db.add_post('bob', 'Test post')
        self.db.add_post('charlie', 'Another post')
        
        # Get all posts
        all_posts = self.db.get_all_posts()
        self.assertEqual(len(all_posts), 3)
        # # Posts should be in reverse chronological order
        self.assertEqual(all_posts[0]['user'], 'charlie')
        self.assertEqual(all_posts[1]['user'], 'bob')
        self.assertEqual(all_posts[2]['user'], 'alice')
    
if __name__ == '__main__':
    unittest.main()