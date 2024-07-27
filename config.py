import os

APP_PATH = os.path.abspath(os.path.dirname(__file__))
DB_NAME = "todo.db"
DB_PATH = os.path.join(APP_PATH, DB_NAME)

class Config:
    """
    Configuration class for the Flask application.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): URI for the database connection.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to disable Flask-SQLAlchemy event system.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False
