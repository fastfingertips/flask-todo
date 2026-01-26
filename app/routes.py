from flask import Blueprint, render_template, request, g, flash
from app.utils import redirect_back
from app.models import Todo, Preferences
from datetime import datetime
from app import db

main = Blueprint('main', __name__)

@main.before_app_request
def load_preferences():
    """Load or initialize user preferences."""
    if 'prefs' not in g:
        prefs = Preferences.query.first()
        if not prefs:
            prefs = Preferences(theme="dark", sorting="desc")
            db.session.add(prefs)
            db.session.commit()
        g.prefs = prefs

@main.app_context_processor
def inject_preferences():
    return {"theme": g.prefs.theme, "sorting": g.prefs.sorting}

@main.route("/")
def index(): 
    todos = Todo.query.order_by(getattr(Todo.created_date, g.prefs.sorting)()).all()
    return render_template("index.html", todos=todos)

@main.route("/add/todo", methods=["POST"])
def add_todo():
    title = request.form.get("title")
    if title:
        new_todo = Todo(
            title=title, 
            created_date=datetime.now(),
            complete=False,
            completed_date=None
        )
        db.session.add(new_todo)
        db.session.commit()
        flash(f"Task '{title}' has been added!", "success")
    return redirect_back()

@main.route("/todo/<int:todo_id>/status")
def change_todo_status(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.complete = not todo.complete
    todo.completed_date = datetime.now() if todo.complete else None
    db.session.commit()
    
    status = "completed" if todo.complete else "re-opened"
    flash(f"Task status updated to {status}.", "info")
    return redirect_back()

@main.route("/todo/<int:todo_id>/delete")
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    title = todo.title
    db.session.delete(todo)
    db.session.commit()
    flash(f"Task '{title}' has been deleted.", "danger")
    return redirect_back()

@main.route("/preferences", methods=["GET"])
def update_preferences():
    g.prefs.theme = request.args.get("theme") or g.prefs.theme
    g.prefs.sorting = request.args.get("sort") or g.prefs.sorting
    db.session.commit()
    flash("Preferences updated.", "secondary")
    return redirect_back()

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500