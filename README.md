# Flask Todo App

This is a simple Todo application built with Flask, demonstrating the use of Flask Blueprints for modular design, SQLAlchemy for database interactions, and Bootstrap for basic styling.

## Features

- Add, update, and delete todo items
- Toggle completion status of todo items
- Persist user preferences for theme (dark/light) and sorting order (ascending/descending)

## Demo

Watch a short demo of the application in action:

https://github.com/FastFingertips/flask-todo/assets/46646991/cafaba2c-5158-4402-bfde-04a8cdf464c0

## Project Structure

- `app/__init__.py`: Initializes the Flask app and database, and registers Blueprints.
- `app/models.py`: Contains database models for Todo items and user preferences.
- `app/routes.py`: Contains route definitions for the main app functionality.
- `app/templates/`: Contains HTML templates for rendering the UI.
- `config.py`: Configuration settings for the Flask app.
- `manage.py`: Entry point for running the Flask app.
- `requirements.txt`: Lists the dependencies required to run the app.

## Setup and Installation

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/fastfingertips/flask-todo.git
   cd flask-todo
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python manage.py
   ```

## Running the App

To start the Flask development server, run:
```bash
python manage.py
```

By default, the app runs on `http://127.0.0.1:5000/`. 

### Changing the Port Number

To run the application on a different port, you can specify the port number when starting the server. For example, to run the app on port 8080, use:

```bash
python manage.py run -p 8080
```

You can also set the port number by modifying the `manage.py` file if needed. Open `manage.py` and locate the line that starts the Flask application, then add the `port` parameter:

```python
if __name__ == "__main__":
    app.run(debug=True, port=8080)
```

Replace `8080` with the port number you wish to use.