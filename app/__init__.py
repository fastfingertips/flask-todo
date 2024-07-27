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

    # Create database tables and import models
    with app.app_context():
        # Import models after creating the app context
        from app import models
        # Create all database tables based on the models
        db.create_all()

    return app
