"""Social Media REST API Application"""
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import os

def create_app(config=None):
    """
    Application factory pattern for Flask app
    Args:
        config: Optional configuration dictionary
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    CORS(app)

    # --- 1. Load config in order of priority ---
    # a) test-time override (arg)
    if config:
        app.config.update(config)

    # b) ENVIRONMENT VARIABLE override
    db_url = app.config.get(
        "DATABASE",
        os.environ.get(
            "DATABASE_URL",
            None  # set below as final fallback
        )
    )

    # c) Python Config fallback
    if not db_url:
        try:
            from backend.config import Config
        except ImportError:
            from config import Config
        db_url = getattr(Config, "DATABASE_URL", None)

    # d) final fallback: SQLite test DB (valid URL)
    if not db_url:
        db_url = "sqlite:///test_api.db"

    app.config['DATABASE_URL'] = db_url

    # --- 2. Register DB on app object (if needed by routes) ---
    # from app.database import SocialMediaDB
    # app.db = SocialMediaDB(db_url)

    # --- 3. Register API blueprints ---
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # --- 4. Swagger UI ---
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

    @app.route('/api/swagger.yaml')
    def swagger_yaml():
        return send_from_directory('../docs', 'openapi.yaml')

    return app