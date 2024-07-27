from flask import Blueprint, render_template, request, redirect
from app.utils import get_referer_or_default
from app.models import Todo, Preferences
from datetime import datetime
from app import db

main = Blueprint('main', __name__)

@main.route("/")
def index(): 
    defaults = {
        "theme": "dark",
        "sorting": "desc"
    }

    # fetch or create preferences
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

   # fetch todos based on sorting preference
    if sorting == "desc":
        todos = Todo.query.order_by(Todo.created_date.desc()).all()
    else:
        todos = Todo.query.order_by(Todo.created_date.asc()).all()

    # render template with context
    context = {
        "todos": todos,
        "theme": theme,
        "sorting": sorting
    }

    return render_template("index.html", **context)

@main.route("/preferences", methods=["GET"])
def update_preferences():
    theme = request.args.get("theme")
    sorting = request.args.get("sort")
    preferences = Preferences.query.first()

    if preferences:
        if theme:
            preferences.theme = theme
        if sorting:
            preferences.sorting = sorting
        db.session.commit()
        print(f"{__name__}: Preferences updated to theme={preferences.theme}, sorting={preferences.sorting}")
    else:
        print(f"{__name__}: No preferences found to update")

    return redirect(get_referer_or_default('main.index'))

@main.route("/add/todo", methods=["POST"])
def add_todo():
    title = request.form.get("title")

    if title:
        new_todo = Todo(
            title=title,
            complete=False,
            complated_date=None,
            created_date=datetime.now()
        )
        db.session.add(new_todo)
        db.session.commit()
        print(f"{__name__}: Added new todo with title={title}")
    else:
        print(f"{__name__}: No title provided for new todo")

    return redirect(get_referer_or_default('main.index'))

@main.route("/todo/<int:todo_id>/status")
def change_todo_status(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if todo:
        todo.complete = not todo.complete
        todo.complated_date = datetime.now() if todo.complete else None
        db.session.commit()
        print(f"{__name__}: Todo {todo.id} status changed to {todo.complete}")
    else:
        print(f"{__name__}: Todo {todo_id} not found")

    return redirect(get_referer_or_default('main.index'))

@main.route("/todo/<int:todo_id>/delete")
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if todo:
        db.session.delete(todo)
        db.session.commit()
        print(f"{__name__}: Todo {todo.id} deleted")
    else:
        print(f"{__name__}: Todo {todo_id} not found")

    return redirect(get_referer_or_default('main.index'))