from flask_sqlalchemy import SQLAlchemy
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)
from datetime import datetime
import os

app = Flask(__name__)

# database
app_path = os.path.dirname(os.path.abspath(__file__))
db_name = "todo.db"
db_path = os.path.join(app_path, db_name)
sqlite_path = 'sqlite:///' + db_path
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_path
db = SQLAlchemy(app)

@app.route("/")
def index(): 
    defaults = {
        "theme": "dark",
        "sorting": "desc"
    }

    # get preferences
    preferences = Preferences.query.first()

    if preferences is None:
        preferences = Preferences(
            theme=defaults["theme"],
            sorting=defaults["sorting"]
        )
        db.session.add(preferences)
        db.session.commit()

    theme = preferences.theme
    sorting = preferences.sorting

    # get todos
    if sorting == "desc":
        todos = Todo.query.order_by(Todo.created_date.desc()).all()
    else:
        todos = Todo.query.order_by(Todo.created_date.asc()).all()

    # render template
    context = {
        "todos": todos,
        "theme": theme,
        "sorting": sorting
    }

    return render_template("index.html", **context)

@app.route("/preferences", methods=["GET"])
def preferences():
    theme = request.args.get("theme")
    sorting = request.args.get("sort")

    print(request.args)

    preferences = Preferences.query.first()

    if theme is not None:
        preferences.theme = theme

    if sorting is not None:
        preferences.sorting = sorting

    db.session.commit()
    print(f"{__name__}: Preferences updated")

    return redirect(url_for("index"))

@app.route("/add/todo", methods=["POST"])
def add_todo():
    title = request.form.get("title")
    new_todo = Todo(
        title=title,
        complete=False,
        complated_date=None,
        created_date=datetime.now()
    )
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/todo/<int:todo_id>/status")
def change_todo_status(todo_id):
    referer = request.headers.get("Referer")

    # change status
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    todo.complated_date = datetime.now() if todo.complete else None
    db.session.commit()
    print(f"{__name__}: Todo {todo.id} status changed to {todo.complete}")

    # redirect
    return redirect(referer or url_for("index"))

@app.route("/todo/<int:todo_id>/delete")
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    print(f"{__name__}: Todo {todo.id} deleted")
    return redirect(url_for("index"))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    complete = db.Column(db.Boolean)
    complated_date = db.Column(db.DateTime)

class Preferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(80), nullable=False)
    sorting = db.Column(db.String(80), nullable=False)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)