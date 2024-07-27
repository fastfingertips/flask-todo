from app import db

class Todo(db.Model):
    """
    Represents a to-do item in the database.

    Attributes:
        id (int): The unique identifier for the to-do item.
        title (str): The title of the to-do item, which cannot be empty.
        created_date (datetime): The date and time when the to-do item was created.
        complete (bool): A flag indicating whether the to-do item is completed.
        complated_date (datetime): The date and time when the to-do item was completed (if applicable).
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    complete = db.Column(db.Boolean)
    complated_date = db.Column(db.DateTime)

class Preferences(db.Model):
    """
    Represents user preferences for the to-do application.

    Attributes:
        id (int): The unique identifier for the preferences record.
        theme (str): The user's preferred theme (e.g., 'dark' or 'light').
        sorting (str): The user's preferred sorting order for to-do items (e.g., 'asc' for ascending, 'desc' for descending).
    """
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(80), nullable=False)
    sorting = db.Column(db.String(80), nullable=False)
