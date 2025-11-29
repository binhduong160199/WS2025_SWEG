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
        self.test_db = os.environ.get(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/test_social_media"
        )
        self.app = create_app({
            'TESTING': True,
            'DATABASE': self.test_db
        })
        self.client = self.app.test_client()
        
        # Initialize database
        with self.app.app_context():
            self.db = SocialMediaDB(self.test_db)
            self.db.delete_all_posts()  # Clean up between tests (optional, if implemented)
    
    def tearDown(self):
        with self.app.app_context():
            self.db.delete_all_posts()
    
    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_create_post_success(self):
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
        post_data = {'text': 'This is a test post'}
        response = self.client.post(
            '/api/posts',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_create_post_missing_text(self):
        post_data = {'user': 'john_doe'}
        response = self.client.post(
            '/api/posts',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_create_post_empty_body(self):
        response = self.client.post(
            '/api/posts',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_create_post_text_too_long(self):
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
        response = self.client.get('/api/posts/9999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_get_all_posts(self):
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
        response = self.client.get('/api/posts')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['posts']), 0)
    
    def test_get_latest_post(self):
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
        response = self.client.get('/api/posts/latest')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_search_posts(self):
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
        response = self.client.get('/api/posts/search')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_search_posts_no_results(self):
        with self.app.app_context():
            db = SocialMediaDB(self.test_db)
            db.add_post('user1', 'Hello world')
        response = self.client.get('/api/posts/search?q=nonexistent')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 0)
    
    def test_invalid_endpoint(self):
        response = self.client.get('/api/invalid')
        self.assertEqual(response.status_code, 404)
    
    def test_method_not_allowed(self):
        response = self.client.delete('/api/posts')
        self.assertEqual(response.status_code, 405)


class TestPostModels(unittest.TestCase):
    """Test cases for post data models"""
    
    def test_post_create_validation_success(self):
        from app.models import PostCreate
        post = PostCreate(user='john_doe', text='Valid post')
        is_valid, error = post.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_post_create_validation_empty_user(self):
        from app.models import PostCreate
        post = PostCreate(user='', text='Valid post')
        is_valid, error = post.validate()
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_post_create_validation_empty_text(self):
        from app.models import PostCreate
        post = PostCreate(user='john_doe', text='')
        is_valid, error = post.validate()
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_post_create_validation_user_too_long(self):
        from app.models import PostCreate
        post = PostCreate(user='x' * 51, text='Valid post')
        is_valid, error = post.validate()
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_post_create_validation_text_too_long(self):
        from app.models import PostCreate
        post = PostCreate(user='john_doe', text='x' * 501)
        is_valid, error = post.validate()
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_post_create_get_image_bytes(self):
        from app.models import PostCreate
        image_b64 = base64.b64encode(b'test_image_data').decode('utf-8')
        post = PostCreate(user='john_doe', text='Post with image', image=image_b64)
        image_bytes = post.get_image_bytes()
        self.assertEqual(image_bytes, b'test_image_data')
    
    def test_post_response_from_db(self):
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