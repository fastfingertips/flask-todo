from flask import Blueprint, render_template, request, redirect, g
from app.utils import get_referer_or_default
from app.models import Todo, Preferences
from datetime import datetime
from app import db

main = Blueprint('main', __name__)

INDEX_ROUTE = 'main.index'

def _get_prefs():
    """Fetch or initialize preferences using flask.g for request caching."""
    if 'prefs' not in g:
        prefs = Preferences.query.first()
        if not prefs:
            prefs = Preferences(theme="dark", sorting="desc")
            db.session.add(prefs)
            db.session.commit()
        g.prefs = prefs
    return g.prefs

@main.app_context_processor
def inject_preferences():
    prefs = _get_prefs()
    return {"theme": prefs.theme, "sorting": prefs.sorting}

def _redirect_to_back():
    """Redirect helper used by multiple routes."""
    return redirect(get_referer_or_default(INDEX_ROUTE))

@main.route("/")
def index(): 
    prefs = _get_prefs()
    sort_attr = Todo.created_date.desc() if prefs.sorting == "desc" else Todo.created_date.asc()
    todos = Todo.query.order_by(sort_attr).all()
    return render_template("index.html", todos=todos)

@main.route("/add/todo", methods=["POST"])
def add_todo():
    title = request.form.get("title")
    if title:
        new_todo = Todo(
            title=title, complete=False, 
            complated_date=None, created_date=datetime.now()
        )
        db.session.add(new_todo)
        db.session.commit()
        print(f"{__name__}: Added new todo with title={title}")
    return _redirect_to_back()

@main.route("/todo/<int:todo_id>/status")
def change_todo_status(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo:
        todo.complete = not todo.complete
        todo.complated_date = datetime.now() if todo.complete else None
        db.session.commit()
        print(f"{__name__}: Todo {todo.id} status changed to {todo.complete}")
    return _redirect_to_back()

@main.route("/todo/<int:todo_id>/delete")
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        print(f"{__name__}: Todo {todo.id} deleted")
    return _redirect_to_back()

@main.route("/preferences", methods=["GET"])
def update_preferences():
    prefs = _get_prefs()
    prefs.theme = request.args.get("theme") or prefs.theme
    prefs.sorting = request.args.get("sort") or prefs.sorting
    db.session.commit()
    print(f"{__name__}: Preferences updated to theme={prefs.theme}, sorting={prefs.sorting}")
    return _redirect_to_back()

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500