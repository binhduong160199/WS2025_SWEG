"""Unit tests for the REST API endpoints"""

import unittest
import json
import os
import base64
from sqlalchemy import create_engine, text
from app import create_app
from app.database import SocialMediaDB, Base

# Use the test database as in your Docker/CI/production setup
POSTGRES_TEST_DB = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/test_social_media"
)

class TestRestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # One engine for the test class
        cls.engine = create_engine(POSTGRES_TEST_DB)
        # Ensure tables are created
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()

    def setUp(self):
        # Wipe all posts before each test
        with self.engine.connect() as conn:
            conn.execute(text("TRUNCATE TABLE posts RESTART IDENTITY CASCADE;"))
            conn.commit()
        # Start app and client
        self.app = create_app({
            'TESTING': True,
            'DATABASE': POSTGRES_TEST_DB
        })
        self.client = self.app.test_client()

    # --- Utility: create post through API ---
    def create_post(self, user, text, image=None):
        payload = {"user": user, "text": text}
        if image:
            payload["image"] = image
        resp = self.client.post(
            "/api/posts",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 201)
        return json.loads(resp.data)["post"]["id"]

    # --- Tests ---

    def test_health_check(self):
        resp = self.client.get('/api/health')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data)['status'], 'healthy')

    def test_create_post_success(self):
        post_id = self.create_post("john_doe", "This is a test post")
        resp = self.client.get(f"/api/posts/{post_id}")
        data = json.loads(resp.data)
        self.assertEqual(data["user"], "john_doe")
        self.assertEqual(data["text"], "This is a test post")

    def test_create_post_with_image(self):
        img_b64 = base64.b64encode(b"\x89PNG\r\n\x1a\n").decode("utf-8")
        post_id = self.create_post("jane_doe", "Post w/ image", img_b64)
        resp = self.client.get(f"/api/posts/{post_id}")
        data = json.loads(resp.data)
        self.assertIsNotNone(data["image"])

    def test_create_post_missing_user(self):
        resp = self.client.post(
            "/api/posts",
            data=json.dumps({"text": "hello"}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', json.loads(resp.data))

    def test_create_post_missing_text(self):
        resp = self.client.post(
            "/api/posts",
            data=json.dumps({"user": "john"}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', json.loads(resp.data))

    def test_create_post_empty_body(self):
        resp = self.client.post(
            "/api/posts",
            data=json.dumps({}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

    def test_create_post_text_too_long(self):
        resp = self.client.post(
            "/api/posts",
            data=json.dumps({"user": "john", "text": "x" * 501}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

    def test_get_post_by_id(self):
        post_id = self.create_post("test_user", "Test post")
        resp = self.client.get(f"/api/posts/{post_id}")
        data = json.loads(resp.data)
        self.assertEqual(data["id"], post_id)
        self.assertEqual(data["user"], "test_user")
        self.assertEqual(data["text"], "Test post")

    def test_get_post_by_id_not_found(self):
        resp = self.client.get("/api/posts/99999")
        self.assertEqual(resp.status_code, 404)
        self.assertIn('error', json.loads(resp.data))

    def test_get_all_posts(self):
        self.create_post("user1", "Post 1")
        self.create_post("user2", "Post 2")
        self.create_post("user3", "Post 3")
        resp = self.client.get("/api/posts")
        data = json.loads(resp.data)
        self.assertEqual(data["count"], 3)
        self.assertEqual(len(data["posts"]), 3)

    def test_get_all_posts_with_limit(self):
        for i in range(10):
            self.create_post(f"user{i}", f"Post {i}")
        resp = self.client.get("/api/posts?limit=5")
        data = json.loads(resp.data)
        self.assertEqual(data["count"], 5)
        self.assertEqual(len(data["posts"]), 5)

    def test_get_all_posts_empty(self):
        resp = self.client.get("/api/posts")
        data = json.loads(resp.data)
        self.assertEqual(data["count"], 0)
        self.assertEqual(len(data["posts"]), 0)

    def test_get_latest_post(self):
        self.create_post("user1", "First")
        self.create_post("user2", "Second")
        self.create_post("user3", "Latest")
        resp = self.client.get("/api/posts/latest")
        data = json.loads(resp.data)
        self.assertEqual(data["user"], "user3")
        self.assertEqual(data["text"], "Latest")

    def test_get_latest_post_empty(self):
        resp = self.client.get("/api/posts/latest")
        self.assertEqual(resp.status_code, 404)
        self.assertIn('error', json.loads(resp.data))

    def test_search_posts(self):
        self.create_post("alice", "I love coffee")
        self.create_post("bob", "Coffee is great")
        self.create_post("charlie", "Tea time")
        resp = self.client.get("/api/posts/search?q=coffee")
        data = json.loads(resp.data)
        self.assertEqual(data["count"], 2)

    def test_search_posts_by_user(self):
        self.create_post("alice_smith", "Hello")
        self.create_post("bob_jones", "World")
        self.create_post("alice_brown", "Test")
        resp = self.client.get("/api/posts/search?q=alice")
        data = json.loads(resp.data)
        self.assertEqual(data["count"], 2)

    def test_search_posts_no_query(self):
        resp = self.client.get("/api/posts/search")
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', json.loads(resp.data))

    def test_search_posts_no_results(self):
        self.create_post("user1", "Hello world")
        resp = self.client.get("/api/posts/search?q=xxx")
        data = json.loads(resp.data)
        self.assertEqual(data["count"], 0)

    def test_invalid_endpoint(self):
        resp = self.client.get("/api/invalid")
        self.assertEqual(resp.status_code, 404)

    def test_method_not_allowed(self):
        resp = self.client.delete("/api/posts")
        self.assertEqual(resp.status_code, 405)

# ----------------------------
# Models tests remain unchanged
# ----------------------------

class TestPostModels(unittest.TestCase):
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
        self.assertEqual(post.get_image_bytes(), b'test_image_data')

    def test_post_response_from_db(self):
        from app.models import PostResponse
        db_data = {
            'id': 1,
            'user': 'john_doe',
            'text': 'Test post',
            'image': b'test_image',
            'created_at': '2025-11-23 10:30:00'
        }
        resp = PostResponse.from_db(db_data)
        self.assertEqual(resp.id, 1)
        self.assertEqual(resp.user, 'john_doe')
        self.assertIsNotNone(resp.image)

if __name__ == "__main__":
    unittest.main()