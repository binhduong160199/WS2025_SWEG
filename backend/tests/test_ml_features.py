"""Tests for ML features and new routes"""

import pytest
import json
from app import create_app
from app.database import SocialMediaDB


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['DATABASE_URL'] = 'sqlite:///:memory:'
    
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def db(app):
    """Create database instance"""
    with app.app_context():
        return SocialMediaDB(app.config['DATABASE_URL'])


class TestSentimentEndpoints:
    """Test sentiment analysis endpoints"""
    
    def test_get_sentiment_post_not_found(self, client):
        """Test getting sentiment for non-existent post"""
        response = client.get('/api/posts/999/sentiment')
        assert response.status_code == 404
        assert 'Post not found' in response.get_json()['error']
    
    def test_get_sentiment_post_exists(self, client, db):
        """Test getting sentiment for existing post"""
        post_id = db.add_post_with_image_data(
            user='testuser',
            text='Great post!'
        )
        
        # Manually set sentiment (since consumer won't run in tests)
        db.update_post_sentiment(post_id, 0.95, 'POSITIVE')
        
        response = client.get(f'/api/posts/{post_id}/sentiment')
        assert response.status_code == 200
        data = response.get_json()
        assert data['post_id'] == post_id
        assert data['sentiment_label'] == 'POSITIVE'
        assert data['sentiment_score'] == 0.95


class TestGeneratedTextEndpoints:
    """Test text generation endpoints"""
    
    def test_get_generated_text_post_not_found(self, client):
        """Test getting generated text for non-existent post"""
        response = client.get('/api/posts/999/generated-text')
        assert response.status_code == 404
        assert 'Post not found' in response.get_json()['error']
    
    def test_get_generated_text_post_exists(self, client, db):
        """Test getting generated text for existing post"""
        post_id = db.add_post_with_image_data(
            user='testuser',
            text='This is a great post'
        )
        
        # Manually set generated text
        generated = json.dumps({'suggestions': ['Suggestion 1', 'Suggestion 2']})
        db.update_post_generated_text(post_id, generated)
        
        response = client.get(f'/api/posts/{post_id}/generated-text')
        assert response.status_code == 200
        data = response.get_json()
        assert data['post_id'] == post_id
        assert data['generated_text'] == generated


class TestMLAnalysisEndpoints:
    """Test combined ML analysis endpoints"""
    
    def test_get_ml_analysis_post_not_found(self, client):
        """Test getting ML analysis for non-existent post"""
        response = client.get('/api/posts/999/ml-analysis')
        assert response.status_code == 404
    
    def test_get_ml_analysis_post_exists(self, client, db):
        """Test getting complete ML analysis"""
        post_id = db.add_post_with_image_data(
            user='testuser',
            text='Awesome content!'
        )
        
        # Set both sentiment and generated text
        db.update_post_sentiment(post_id, 0.88, 'POSITIVE')
        generated = json.dumps({'suggestions': ['More awesome!']})
        db.update_post_generated_text(post_id, generated)
        
        response = client.get(f'/api/posts/{post_id}/ml-analysis')
        assert response.status_code == 200
        data = response.get_json()
        assert data['post_id'] == post_id
        assert data['sentiment']['label'] == 'POSITIVE'
        assert data['sentiment']['score'] == 0.88
        assert data['generated_text'] == generated


class TestReAnalyzeEndpoint:
    """Test re-analysis triggering"""
    
    def test_re_analyze_post_not_found(self, client):
        """Test re-analyzing non-existent post"""
        response = client.post('/api/posts/999/re-analyze')
        assert response.status_code == 404
    
    def test_re_analyze_post_exists(self, client, db):
        """Test re-analyzing existing post"""
        post_id = db.add_post_with_image_data(
            user='testuser',
            text='Test post for re-analysis'
        )
        
        response = client.post(f'/api/posts/{post_id}/re-analyze')
        assert response.status_code == 200
        data = response.get_json()
        assert data['post_id'] == post_id
        assert 'Analysis re-triggered' in data['message']


class TestPostResponseWithMLFields:
    """Test that post responses include ML fields"""
    
    def test_create_post_response_includes_ml_fields(self, client, db):
        """Test that created post response includes ML fields"""
        response = client.post('/api/posts', json={
            'user': 'testuser',
            'text': 'Test post with ML'
        })
        
        assert response.status_code == 201
        post_data = response.get_json()['post']
        assert 'sentiment_score' in post_data
        assert 'sentiment_label' in post_data
        assert 'generated_text' in post_data
        assert 'processing_status' in post_data
    
    def test_get_post_response_includes_ml_fields(self, client, db):
        """Test that fetched post response includes ML fields"""
        post_id = db.add_post_with_image_data(
            user='testuser',
            text='Test post'
        )
        
        response = client.get(f'/api/posts/{post_id}')
        assert response.status_code == 200
        post_data = response.get_json()
        assert 'sentiment_score' in post_data
        assert 'sentiment_label' in post_data
        assert 'generated_text' in post_data
        assert 'processing_status' in post_data


class TestProcessingStatus:
    """Test processing status tracking"""
    
    def test_set_processing_status(self, db):
        """Test setting processing status"""
        post_id = db.add_post_with_image_data(
            user='testuser',
            text='Test post'
        )
        
        # Check default status
        post = db.get_post_by_id(post_id)
        assert post['processing_status'] == 'pending'
        
        # Set to processing
        db.set_post_processing_status(post_id, 'processing')
        post = db.get_post_by_id(post_id)
        assert post['processing_status'] == 'processing'


class TestDatabaseMLUpdates:
    """Test database update methods for ML fields"""
    
    def test_update_sentiment(self, db):
        """Test updating sentiment"""
        post_id = db.add_post_with_image_data(
            user='testuser',
            text='Test sentiment'
        )
        
        result = db.update_post_sentiment(post_id, 0.75, 'POSITIVE')
        assert result is True
        
        post = db.get_post_by_id(post_id)
        assert post['sentiment_score'] == 0.75
        assert post['sentiment_label'] == 'POSITIVE'
    
    def test_update_generated_text(self, db):
        """Test updating generated text"""
        post_id = db.add_post_with_image_data(
            user='testuser',
            text='Test generation'
        )
        
        text = json.dumps({'suggestions': ['Generated 1']})
        result = db.update_post_generated_text(post_id, text)
        assert result is True
        
        post = db.get_post_by_id(post_id)
        assert post['generated_text'] == text
