"""Unit tests for the database module"""
import unittest
import os
from app.database import SocialMediaDB


class TestSocialMediaDB(unittest.TestCase):
    """Test cases for Social Media Database"""
    
    def setUp(self):
        """Set up test database before each test"""
        # self.test_db = "test_social_media.db"  # Removed SQLite test DB
        self.db = SocialMediaDB(self.test_db)
    
    def tearDown(self):
        """Clean up test database after each test"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_database_initialization(self):
        """Test that database is created successfully"""
        self.assertTrue(os.path.exists(self.test_db))
    
    def test_add_post_without_image(self):
        """Test adding a post without an image"""
        post_id = self.db.add_post(
            user='test_user',
            text='This is a test post',
            image_path=None
        )
        
        self.assertIsNotNone(post_id)
        self.assertGreater(post_id, 0)
    
    def test_add_post_with_image_data(self):
        """Test adding a post with raw image data"""
        image_data = b'\x89PNG\r\n\x1a\n'  # PNG header
        post_id = self.db.add_post_with_image_data(
            user='test_user',
            text='Post with image',
            image_data=image_data
        )
        
        self.assertGreater(post_id, 0)
        
        # Verify image was stored
        post = self.db.get_post_by_id(post_id)
        self.assertEqual(post['image'], image_data)
    
    def test_get_post_by_id(self):
        """Test retrieving a specific post by ID"""
        post_id = self.db.add_post('user1', 'Test post')
        
        post = self.db.get_post_by_id(post_id)
        
        self.assertIsNotNone(post)
        self.assertEqual(post['id'], post_id)
        self.assertEqual(post['user'], 'user1')
        self.assertEqual(post['text'], 'Test post')
    
    def test_get_post_by_id_not_found(self):
        """Test retrieving a non-existent post"""
        post = self.db.get_post_by_id(9999)
        self.assertIsNone(post)
    
    def test_get_latest_post(self):
        """Test retrieving the latest post"""
        self.db.add_post('user1', 'First post')
        self.db.add_post('user2', 'Second post')
        self.db.add_post('user3', 'Third post')
        
        latest = self.db.get_latest_post()
        
        self.assertIsNotNone(latest)
        self.assertEqual(latest['user'], 'user3')
        self.assertEqual(latest['text'], 'Third post')
    
    def test_get_latest_post_empty_database(self):
        """Test getting latest post from empty database"""
        latest = self.db.get_latest_post()
        self.assertIsNone(latest)
    
    def test_get_all_posts(self):
        """Test retrieving all posts"""
        self.db.add_post('alice', 'Hello world')
        self.db.add_post('bob', 'Test post')
        self.db.add_post('charlie', 'Another post')
        
        all_posts = self.db.get_all_posts()
        
        self.assertEqual(len(all_posts), 3)
        # Posts should be in reverse chronological order
        self.assertEqual(all_posts[0]['user'], 'charlie')
        self.assertEqual(all_posts[1]['user'], 'bob')
        self.assertEqual(all_posts[2]['user'], 'alice')
    
    def test_get_all_posts_with_limit(self):
        """Test retrieving posts with a limit"""
        for i in range(10):
            self.db.add_post(f'user{i}', f'Post {i}')
        
        limited_posts = self.db.get_all_posts(limit=5)
        
        self.assertEqual(len(limited_posts), 5)
    
    def test_search_posts_by_text(self):
        """Test searching posts by text content"""
        self.db.add_post('alice', 'I love coffee')
        self.db.add_post('bob', 'Coffee is great')
        self.db.add_post('charlie', 'Tea is better')
        
        results = self.db.search_posts('coffee')
        
        self.assertEqual(len(results), 2)
        self.assertTrue(any('coffee' in post['text'].lower() for post in results))
    
    def test_search_posts_by_user(self):
        """Test searching posts by username"""
        self.db.add_post('alice_smith', 'Hello')
        self.db.add_post('bob_jones', 'World')
        self.db.add_post('alice_brown', 'Test')
        
        results = self.db.search_posts('alice')
        
        self.assertEqual(len(results), 2)
        self.assertTrue(all('alice' in post['user'].lower() for post in results))
    
    def test_search_posts_no_results(self):
        """Test searching with no matching results"""
        self.db.add_post('user1', 'Hello')
        
        results = self.db.search_posts('nonexistent')
        
        self.assertEqual(len(results), 0)
    
    def test_delete_all_posts(self):
        """Test deleting all posts"""
        self.db.add_post('user1', 'Post 1')
        self.db.add_post('user2', 'Post 2')
        
        self.db.delete_all_posts()
        
        all_posts = self.db.get_all_posts()
        self.assertEqual(len(all_posts), 0)


if __name__ == '__main__':
    unittest.main()
