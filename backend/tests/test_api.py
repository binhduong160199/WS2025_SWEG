"""Unit tests for the REST API endpoints"""
import unittest
import json
import os
import base64
from app import create_app
from app.database import SocialMediaDB


class TestRestAPI(unittest.TestCase):
    """Test cases for REST API endpoints"""
    
    def setUp(self):
        """Set up test client and test database before each test"""
        self.test_db = "test_api.db"
        self.app = create_app({
            'TESTING': True,
            'DATABASE': self.test_db
        })
        self.client = self.app.test_client()
        
        # Initialize database
        with self.app.app_context():
            self.db = SocialMediaDB(self.test_db)
    
    def tearDown(self):
        """Clean up test database after each test"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_create_post_success(self):
        """Test successfully creating a post"""
        post_data = {
            'user': 'john_doe',
            'text': 'This is a test post'
        }
        
        response = self.client.post(
            '/api/posts',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Post created successfully')
        self.assertIn('post', data)
        self.assertEqual(data['post']['user'], 'john_doe')
        self.assertEqual(data['post']['text'], 'This is a test post')
    
    def test_create_post_with_image(self):
        """Test creating a post with an image"""
        # Create a simple base64 encoded image
        image_data = base64.b64encode(b'\x89PNG\r\n\x1a\n').decode('utf-8')
        
        post_data = {
            'user': 'jane_doe',
            'text': 'Post with image',
            'image': image_data
        }
        
        response = self.client.post(
            '/api/posts',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIsNotNone(data['post']['image'])
    
    def test_create_post_missing_user(self):
        """Test creating a post without user field"""
        post_data = {
            'text': 'This is a test post'
        }
        
        response = self.client.post(
            '/api/posts',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_create_post_missing_text(self):
        """Test creating a post without text field"""
        post_data = {
            'user': 'john_doe'
        }
        
        response = self.client.post(
            '/api/posts',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_create_post_empty_body(self):
        """Test creating a post with empty request body"""
        response = self.client.post(
            '/api/posts',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_post_text_too_long(self):
        """Test creating a post with text exceeding maximum length"""
        post_data = {
            'user': 'john_doe',
            'text': 'x' * 501  # Exceeds 500 character limit
        }
        
        response = self.client.post(
            '/api/posts',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_get_post_by_id(self):
        """Test retrieving a specific post by ID"""
        # Create a post first
        with self.app.app_context():
            db = SocialMediaDB(self.test_db)
            post_id = db.add_post('test_user', 'Test post')
        
        response = self.client.get(f'/api/posts/{post_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], post_id)
        self.assertEqual(data['user'], 'test_user')
        self.assertEqual(data['text'], 'Test post')
    
    def test_get_post_by_id_not_found(self):
        """Test retrieving a non-existent post"""
        response = self.client.get('/api/posts/9999')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_get_all_posts(self):
        """Test retrieving all posts"""
        # Create multiple posts
        with self.app.app_context():
            db = SocialMediaDB(self.test_db)
            db.add_post('user1', 'Post 1')
            db.add_post('user2', 'Post 2')
            db.add_post('user3', 'Post 3')
        
        response = self.client.get('/api/posts')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 3)
        self.assertEqual(len(data['posts']), 3)
    
    def test_get_all_posts_with_limit(self):
        """Test retrieving posts with a limit"""
        # Create multiple posts
        with self.app.app_context():
            db = SocialMediaDB(self.test_db)
            for i in range(10):
                db.add_post(f'user{i}', f'Post {i}')
        
        response = self.client.get('/api/posts?limit=5')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 5)
        self.assertEqual(len(data['posts']), 5)
    
    def test_get_all_posts_empty(self):
        """Test retrieving posts when database is empty"""
        response = self.client.get('/api/posts')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['posts']), 0)
    
    def test_get_latest_post(self):
        """Test retrieving the latest post"""
        with self.app.app_context():
            db = SocialMediaDB(self.test_db)
            db.add_post('user1', 'First post')
            db.add_post('user2', 'Second post')
            db.add_post('user3', 'Latest post')
        
        response = self.client.get('/api/posts/latest')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['user'], 'user3')
        self.assertEqual(data['text'], 'Latest post')
    
    def test_get_latest_post_empty(self):
        """Test retrieving latest post when database is empty"""
        response = self.client.get('/api/posts/latest')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_search_posts(self):
        """Test searching for posts"""
        with self.app.app_context():
            db = SocialMediaDB(self.test_db)
            db.add_post('alice', 'I love coffee')
            db.add_post('bob', 'Coffee is great')
            db.add_post('charlie', 'Tea is better')
        
        response = self.client.get('/api/posts/search?q=coffee')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['query'], 'coffee')
        self.assertEqual(data['count'], 2)
    
    def test_search_posts_by_user(self):
        """Test searching for posts by username"""
        with self.app.app_context():
            db = SocialMediaDB(self.test_db)
            db.add_post('alice_smith', 'Hello')
            db.add_post('bob_jones', 'World')
            db.add_post('alice_brown', 'Test')
        
        response = self.client.get('/api/posts/search?q=alice')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 2)
    
    def test_search_posts_no_query(self):
        """Test searching without providing a query"""
        response = self.client.get('/api/posts/search')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_search_posts_no_results(self):
        """Test searching with no matching results"""
        with self.app.app_context():
            db = SocialMediaDB(self.test_db)
            db.add_post('user1', 'Hello world')
        
        response = self.client.get('/api/posts/search?q=nonexistent')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 0)
    
    def test_invalid_endpoint(self):
        """Test accessing an invalid endpoint"""
        response = self.client.get('/api/invalid')
        
        self.assertEqual(response.status_code, 404)
    
    def test_method_not_allowed(self):
        """Test using incorrect HTTP method"""
        response = self.client.delete('/api/posts')
        
        self.assertEqual(response.status_code, 405)


class TestPostModels(unittest.TestCase):
    """Test cases for post data models"""
    
    def test_post_create_validation_success(self):
        """Test successful post validation"""
        from app.models import PostCreate
        
        post = PostCreate(user='john_doe', text='Valid post')
        is_valid, error = post.validate()
        
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_post_create_validation_empty_user(self):
        """Test validation fails with empty user"""
        from app.models import PostCreate
        
        post = PostCreate(user='', text='Valid post')
        is_valid, error = post.validate()
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_post_create_validation_empty_text(self):
        """Test validation fails with empty text"""
        from app.models import PostCreate
        
        post = PostCreate(user='john_doe', text='')
        is_valid, error = post.validate()
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_post_create_validation_user_too_long(self):
        """Test validation fails with username too long"""
        from app.models import PostCreate
        
        post = PostCreate(user='x' * 51, text='Valid post')
        is_valid, error = post.validate()
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_post_create_validation_text_too_long(self):
        """Test validation fails with text too long"""
        from app.models import PostCreate
        
        post = PostCreate(user='john_doe', text='x' * 501)
        is_valid, error = post.validate()
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_post_create_get_image_bytes(self):
        """Test converting base64 image to bytes"""
        from app.models import PostCreate
        
        image_b64 = base64.b64encode(b'test_image_data').decode('utf-8')
        post = PostCreate(user='john_doe', text='Post with image', image=image_b64)
        
        image_bytes = post.get_image_bytes()
        
        self.assertEqual(image_bytes, b'test_image_data')
    
    def test_post_response_from_db(self):
        """Test creating PostResponse from database data"""
        from app.models import PostResponse
        
        db_data = {
            'id': 1,
            'user': 'john_doe',
            'text': 'Test post',
            'image': b'test_image',
            'created_at': '2025-11-23 10:30:00'
        }
        
        response = PostResponse.from_db(db_data)
        
        self.assertEqual(response.id, 1)
        self.assertEqual(response.user, 'john_doe')
        self.assertIsNotNone(response.image)


if __name__ == '__main__':
    unittest.main()
