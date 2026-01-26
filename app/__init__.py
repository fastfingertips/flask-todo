from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Global SQLAlchemy instance
db = SQLAlchemy()

def create_app():
    """
    Factory function to create and configure a Flask application instance.

    :return: The Flask application instance.
    """
    # Create a Flask application instance
    app = Flask(__name__)
    
    # Load configuration from the Config class
    app.config.from_object(Config)

    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)

    # Register Blueprints
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.after_request
    def add_security_headers(response):
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data:; "
            "connect-src 'self' https://cdn.jsdelivr.net; "
            "frame-ancestors 'none';"
        )
        response.headers['Content-Security-Policy'] = csp
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        return response

    # Create database tables and import models
    with app.app_context():
        # Import models after creating the app context
        from app import models  # noqa: F401
        # Create all database tables based on the models
        db.create_all()

    return app
