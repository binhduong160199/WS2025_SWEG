"""Social Media REST API Application"""
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint


def create_app(config=None):
    """
    Application factory pattern for Flask app
    
    Args:
        config: Optional configuration dictionary
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Load configuration
    if config:
        app.config.update(config)
    else:
        app.config['DATABASE'] = 'social_media.db'
        app.config['TESTING'] = False
    
    # Register API blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Swagger UI configuration
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/swagger.yaml'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Social Media REST API"
        }
    )
    
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # Route to serve the OpenAPI YAML file
    @app.route('/api/swagger.yaml')
    def swagger_yaml():
        return send_from_directory('../docs', 'openapi.yaml')
    
    return app
