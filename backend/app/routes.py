"""REST API routes for social media application"""

from flask import Blueprint, request, jsonify, current_app
from app.database import SocialMediaDB
from app.models import PostCreate, PostResponse, PostListResponse
from app.messaging import (
    publish_image_resize_event,
    publish_sentiment_analysis_event,
    publish_text_generation_event,  # Only uses prompt now!
)

# --- Import microservice logic at the top for clarity ---
from text_generator.app.generator import generate_text as ai_generate_text
from text_generator.app.db import save_generated_text, get_latest_generated_text

api_bp = Blueprint('api', __name__)

def get_db():
    """Get database instance with current app configuration"""
    return SocialMediaDB(current_app.config['DATABASE_URL'])

# -------------------------------------------------------------------
# Health Check
# -------------------------------------------------------------------
@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Social Media API is running'
    }), 200

# -------------------------------------------------------------------
# Create Post
# -------------------------------------------------------------------
@api_bp.route('/posts', methods=['POST'])
def create_post():
    """Create a new post"""
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Request body is required'}), 400

        post = PostCreate(
            user=data.get('user', ''),
            text=data.get('text', ''),
            image=data.get('image')
        )
        is_valid, error_msg = post.validate()
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        db = get_db()
        image_bytes = post.get_image_bytes()
        post_id = db.add_post_with_image_data(
            user=post.user,
            text=post.text,
            image_data=image_bytes
        )

        # Publish events to microservices
        if image_bytes and not current_app.config.get("TESTING", False):
            publish_image_resize_event(post_id)
        if not current_app.config.get("TESTING", False):
            publish_sentiment_analysis_event(post_id)
            # Text generation NOT tied to creating a post anymore!

        created_post = db.get_post_by_id(post_id)
        response = PostResponse.from_db(created_post)
        return jsonify({
            'message': 'Post created successfully',
            'post': response.to_dict()
        }), 201

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# -------------------------------------------------------------------
# Get a Single Post by ID
# -------------------------------------------------------------------
@api_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        db = get_db()
        post_data = db.get_post_by_id(post_id)
        if not post_data:
            return jsonify({'error': 'Post not found'}), 404
        response = PostResponse.from_db(post_data)
        return jsonify(response.to_dict()), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# -------------------------------------------------------------------
# Get All Posts (with optional limit)
# -------------------------------------------------------------------
@api_bp.route('/posts', methods=['GET'])
def get_posts():
    try:
        limit = request.args.get('limit', type=int)
        db = get_db()
        posts_data = db.get_all_posts(limit=limit)
        posts = [PostListResponse.from_db(post).to_dict() for post in posts_data]
        return jsonify({
            'count': len(posts),
            'posts': posts
        }), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# -------------------------------------------------------------------
# Search Posts by Text/User
# -------------------------------------------------------------------
@api_bp.route('/posts/search', methods=['GET'])
def search_posts():
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'Search query parameter "q" is required'}), 400
        db = get_db()
        posts_data = db.search_posts(query)
        posts = [PostListResponse.from_db(post).to_dict() for post in posts_data]
        return jsonify({
            'query': query,
            'count': len(posts),
            'posts': posts
        }), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# -------------------------------------------------------------------
# Get Latest Post
# -------------------------------------------------------------------
@api_bp.route('/posts/latest', methods=['GET'])
def get_latest_post():
    try:
        db = get_db()
        post_data = db.get_latest_post()
        if not post_data:
            return jsonify({'error': 'No posts found'}), 404
        response = PostResponse.from_db(post_data)
        return jsonify(response.to_dict()), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# -------------------------------------------------------------------
# AI Text Generation (RabbitMQ ASYNC ONLY — NO post_id)
# -------------------------------------------------------------------
@api_bp.route('/posts/generate', methods=['POST'])
def generate_text_route():
    """
    POST /posts/generate
    - Publishes prompt to RabbitMQ (async, AI microservice saves to text_suggestions)
    - No post_id, no posts table coupling
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400

        prompt = data.get('prompt', '').strip()
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        # Publish prompt to RabbitMQ text_generation queue
        publish_text_generation_event(prompt)
        return jsonify({
            'prompt': prompt,
            'status': 'processing',
            'message': 'Text generation started'
        }), 202

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# -------------------------------------------------------------------
# Get Latest Generated Text (AI Suggestion, no post_id)
# -------------------------------------------------------------------
@api_bp.route('/posts/generated-text', methods=['GET'])
def get_latest_generated_text_route():
    try:
        generated_text = get_latest_generated_text()
        if generated_text:
            return jsonify({'generated_text': generated_text}), 200
        else:
            return jsonify({'generated_text': '', 'message': 'No generated text found.'}), 200
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# -------------------------------------------------------------------
# Error Handlers
# -------------------------------------------------------------------
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@api_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500