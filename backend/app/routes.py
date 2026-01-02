"""REST API routes for social media application"""

from flask import Blueprint, request, jsonify, current_app
from app.database import SocialMediaDB
from app.models import PostCreate, PostResponse, PostListResponse
from app.messaging import publish_image_resize_event, publish_sentiment_analysis_event, publish_text_generation_event


api_bp = Blueprint('api', __name__)


def get_db():
    """Get database instance with current app configuration"""
    return SocialMediaDB(current_app.config['DATABASE_URL'])


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    ---
    responses:
      200:
        description: API is healthy
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Social Media API is running'
    }), 200


@api_bp.route('/posts', methods=['POST'])
def create_post():
    """
    Create a new post
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - user
              - text
            properties:
              user:
                type: string
                description: Username of the poster
              text:
                type: string
                description: Text content of the post
              image:
                type: string
                description: Base64 encoded image data (optional)
    responses:
      201:
        description: Post created successfully
      400:
        description: Invalid request data
    """
    try:
        data = request.get_json()

        # Handle empty or invalid JSON
        if data is None:
            return jsonify({'error': 'Request body is required'}), 400

        # Create and validate post
        post = PostCreate(
            user=data.get('user', ''),
            text=data.get('text', ''),
            image=data.get('image')
        )

        is_valid, error_msg = post.validate()
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        # Save to database
        db = get_db()

        image_bytes = post.get_image_bytes()

        post_id = db.add_post_with_image_data(
            user=post.user,
            text=post.text,
            image_data=image_bytes
        )

        if (
            image_bytes is not None
            and not current_app.config.get("TESTING", False)
        ):
            publish_image_resize_event(post_id)

        # Publish sentiment analysis and text generation events
        if not current_app.config.get("TESTING", False):
            publish_sentiment_analysis_event(post_id)
            publish_text_generation_event(post_id)

        created_post = db.get_post_by_id(post_id)
        response = PostResponse.from_db(created_post)

        return jsonify({
            'message': 'Post created successfully',
            'post': response.to_dict()
        }), 201

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@api_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Get a specific post by ID
    ---
    parameters:
      - name: post_id
        in: path
        required: true
        schema:
          type: integer
        description: ID of the post to retrieve
    responses:
      200:
        description: Post retrieved successfully
      404:
        description: Post not found
    """
    try:
        db = get_db()
        post_data = db.get_post_by_id(post_id)

        if not post_data:
            return jsonify({'error': 'Post not found'}), 404

        response = PostResponse.from_db(post_data)
        return jsonify(response.to_dict()), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@api_bp.route('/posts', methods=['GET'])
def get_posts():
    """
    Get all posts (with optional limit)
    ---
    parameters:
      - name: limit
        in: query
        schema:
          type: integer
        description: Maximum number of posts to return
    responses:
      200:
        description: Posts retrieved successfully
    """
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


@api_bp.route('/posts/search', methods=['GET'])
def search_posts():
    """
    Search for posts by text content or username
    ---
    parameters:
      - name: q
        in: query
        required: true
        schema:
          type: string
        description: Search query string
    responses:
      200:
        description: Search completed successfully
      400:
        description: Missing search query
    """
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


@api_bp.route('/posts/latest', methods=['GET'])
def get_latest_post():
    """
    Get the most recent post
    ---
    responses:
      200:
        description: Latest post retrieved successfully
      404:
        description: No posts found
    """
    try:
        db = get_db()
        post_data = db.get_latest_post()

        if not post_data:
            return jsonify({'error': 'No posts found'}), 404

        response = PostResponse.from_db(post_data)
        return jsonify(response.to_dict()), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@api_bp.route('/posts/generate', methods=['POST'])
def generate_text():
    """
    Generate text using GPT-2
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - prompt
            properties:
              prompt:
                type: string
                description: Text prompt for generation
              post_id:
                type: integer
                description: Optional post ID to retrieve generated text for
              max_length:
                type: integer
                description: Maximum length of generated text (default 50)
    responses:
      200:
        description: Text generated successfully
      400:
        description: Invalid request data
    """
    try:
        data = request.get_json()

        if data is None:
            return jsonify({'error': 'Request body is required'}), 400

        # If post_id is provided, try to retrieve the generated text
        if 'post_id' in data:
            post_id = data.get('post_id')
            db = get_db()
            
            # Check if text generation is complete
            generated_text = db.get_text_suggestion_for_post(post_id)

            if generated_text:
                return jsonify({
                    'post_id': post_id,
                    'generated_text': generated_text,
                    'suggestions': [generated_text],
                    'status': 'completed'
                }), 200
            else:
                return jsonify({
                    'post_id': post_id,
                    'status': 'processing',
                    'message': 'Text generation in progress'
                }), 202

        # Legacy: return placeholder for direct prompt
        prompt = data.get('prompt', '').strip()
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        return jsonify({
            'prompt': prompt,
            'generated_text': f"{prompt}... [Please create a post first to generate text]",
            'message': 'Create a post to use text generation'
        }), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


# ------------------------------------------------------
# Error handlers
# ------------------------------------------------------
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@api_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405


@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500